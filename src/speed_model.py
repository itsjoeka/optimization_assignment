"""Travel-time model fitted to the 23 field-measured depot-to-town legs.

CORRECTION M7.

The first audit flagged the implied road speeds -- distance divided by travel
time -- as spanning 1.0 to 47.2 km/h and called it a data-quality problem. It is
mostly not. Fitting travel time on distance recovers a fixed overhead plus a
roughly constant cruise speed:

    t = 0.1595 + 0.02059 * d        R^2 = 0.896, LOOCV Q^2 = 0.874

The intercept is about ten minutes -- the time to clear Hohoe town and reach the
trunk road -- and the slope is 1/48.6 km/h. Dividing a FIXED overhead by a SHORT
distance is what produces an apparently slow town, so Wli at 47 km/h and
Gbi-Kledzo at 18 km/h are the same vehicle on the same road model.

That turns the dataset's most reviewer-visible oddity into a one-paragraph
finding in the Data section, and it is a result the paper should report rather
than an assumption it should defend.

A note on what is NOT claimed here. A Near/Far step dummy added to the linear
model appears significant (p = 0.039 on the committed zone column). It does not
survive scrutiny: the apparent break is a competing parameterisation of the same
fixed overhead, the threshold that fits best is 16 km rather than the 20 km the
optimisation model uses, and at 20 km itself the dummy is not significant
(p = 0.057). Searching 29 candidate thresholds and reporting the best would be a
specification search. See `threshold_placebo()`, which exists so that this can be
checked rather than taken on trust.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats

from .config import SUSPECT_TOWNS


@dataclass
class SpeedFit:
    n: int
    intercept_h: float
    intercept_se: float
    intercept_p: float
    slope_h_per_km: float
    slope_p: float
    cruise_kmh: float
    r2: float
    loocv_q2: float
    loocv_mae_min: float
    rmse_min: float
    excluded: list

    @property
    def overhead_min(self) -> float:
        return self.intercept_h * 60.0

    def predict(self, distance_km):
        return self.intercept_h + self.slope_h_per_km * np.asarray(distance_km)

    def summary(self) -> str:
        return (f"t = {self.intercept_h:.4f} + {self.slope_h_per_km:.5f} d   "
                f"(n={self.n}, R2={self.r2:.4f}, LOOCV Q2={self.loocv_q2:.4f})\n"
                f"  fixed overhead {self.overhead_min:.1f} min, "
                f"cruise {self.cruise_kmh:.2f} km/h, "
                f"LOOCV MAE {self.loocv_mae_min:.2f} min")


def _clean(towns):
    """Drop towns with a documented data-quality flag before fitting."""
    mask = ~towns["service_town"].isin(SUSPECT_TOWNS)
    return towns[mask], sorted(set(towns["service_town"]) & set(SUSPECT_TOWNS))


def fit(towns) -> SpeedFit:
    """Ordinary least squares with leave-one-out cross-validation.

    LOOCV uses the hat-matrix shortcut, which is exact for simple OLS and avoids
    refitting n times.
    """
    clean, excluded = _clean(towns)
    d = clean["distance_in_km"].to_numpy(float)
    t = clean["travel_time_in_hours"].to_numpy(float)
    n = len(d)

    reg = stats.linregress(d, t)
    resid = t - (reg.intercept + reg.slope * d)
    ss_res = float((resid ** 2).sum())
    ss_tot = float(((t - t.mean()) ** 2).sum())

    sxx = float(((d - d.mean()) ** 2).sum())
    h = 1.0 / n + (d - d.mean()) ** 2 / sxx          # leverage
    loo_err = resid / (1.0 - h)
    press = float((loo_err ** 2).sum())

    t_int = reg.intercept / reg.intercept_stderr
    return SpeedFit(
        n=n,
        intercept_h=float(reg.intercept),
        intercept_se=float(reg.intercept_stderr),
        intercept_p=float(2 * (1 - stats.t.cdf(abs(t_int), n - 2))),
        slope_h_per_km=float(reg.slope),
        slope_p=float(reg.pvalue),
        cruise_kmh=float(1.0 / reg.slope),
        r2=1.0 - ss_res / ss_tot,
        loocv_q2=1.0 - press / ss_tot,
        loocv_mae_min=float(np.abs(loo_err).mean() * 60),
        rmse_min=float(np.sqrt(ss_res / n) * 60),
        excluded=excluded,
    )


def power_law(towns) -> dict:
    """Fit t = c * d^k. Constant speed would mean k = 1.

    An independent route to the same conclusion as the intercept: if k < 1,
    effective speed rises with distance, which is what a fixed overhead does.
    """
    clean, _ = _clean(towns)
    d = clean["distance_in_km"].to_numpy(float)
    t = clean["travel_time_in_hours"].to_numpy(float)
    n = len(d)
    reg = stats.linregress(np.log(d), np.log(t))
    tstat = (reg.slope - 1.0) / reg.stderr
    crit = stats.t.ppf(0.975, n - 2)
    return {
        "k": float(reg.slope),
        "ci95": (float(reg.slope - crit * reg.stderr),
                 float(reg.slope + crit * reg.stderr)),
        "r2": float(reg.rvalue ** 2),
        "t_vs_constant_speed": float(tstat),
        "p_vs_constant_speed": float(2 * (1 - stats.t.cdf(abs(tstat), n - 2))),
    }


def threshold_placebo(towns, candidates=range(5, 36)) -> dict:
    """Test a step dummy at EVERY candidate threshold, not just the chosen one.

    A single significant threshold means little when many were tried. This
    reports the whole search so the reader can see how much of it is noise, and
    applies a Bonferroni correction.

    It exists because the Near/Far dummy looks significant at p = 0.039 in the
    linear model, and the question "is 20 km special?" has to be answered with
    evidence rather than with the one test that happened to be run.
    """
    clean, _ = _clean(towns)
    d = clean["distance_in_km"].to_numpy(float)
    t = clean["travel_time_in_hours"].to_numpy(float)
    n = len(d)
    base = np.column_stack([np.ones(n), d])
    beta, *_ = np.linalg.lstsq(base, t, rcond=None)
    rss_base = float(((t - base @ beta) ** 2).sum())

    rows = []
    for thr in candidates:
        dummy = (d <= thr).astype(float)
        if dummy.sum() < 3 or dummy.sum() > n - 3:
            continue
        full = np.column_stack([base, dummy])
        bf, *_ = np.linalg.lstsq(full, t, rcond=None)
        rss_full = float(((t - full @ bf) ** 2).sum())
        f = ((rss_base - rss_full) / 1) / (rss_full / (n - 3))
        rows.append({
            "threshold_km": float(thr),
            "n_below": int(dummy.sum()),
            "F": float(f),
            "p": float(1 - stats.f.cdf(f, 1, n - 3)),
            "step_minutes": float(bf[2] * 60),
        })
    alpha = 0.05 / len(rows) if rows else float("nan")
    return {
        "tests": rows,
        "n_tests": len(rows),
        "n_significant_uncorrected": sum(1 for r in rows if r["p"] < 0.05),
        "bonferroni_alpha": alpha,
        "surviving_bonferroni": [r["threshold_km"] for r in rows if r["p"] < alpha],
        "best": min(rows, key=lambda r: r["p"]) if rows else None,
    }


def outlier_report(towns, fit_result: SpeedFit) -> list:
    """Flagged towns measured against the fitted model.

    Reports what the model expects and what distance the recorded TIME would
    imply, so the direction of a suspected transcription error can be argued.
    """
    out = []
    for _, row in towns.iterrows():
        if row["service_town"] not in SUSPECT_TOWNS:
            continue
        d = float(row["distance_in_km"])
        t = float(row["travel_time_in_hours"])
        out.append({
            "town": row["service_town"],
            "recorded_km": d,
            "recorded_hours": t,
            "implied_speed_kmh": d / t,
            "model_predicts_hours": float(fit_result.predict(d)),
            "distance_implied_by_time_km": float(
                (t - fit_result.intercept_h) / fit_result.slope_h_per_km),
            "residual_sd": float((t - fit_result.predict(d))
                                 / (fit_result.rmse_min / 60)),
            "note": SUSPECT_TOWNS[row["service_town"]],
        })
    return out
