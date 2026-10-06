"""Single source of truth for every model parameter.

Every notebook and script imports from here. Nothing is redefined locally --
that is what allowed theta to drift to 1.6 in notebook 02 and 1.5 in notebook 03.
"""
from dataclasses import dataclass, field


# --- Zone classification -------------------------------------------------
# CORRECTION M1. The original code used ceil(max(distance))/2 = 19.5 km, which
# is a function of the farthest town in the dataset: adding one distant town
# silently reclassifies others. The README stated 20 km. The two disagree on
# Liati, at exactly 20.0 km.
#
# Resolution: fix an EXOGENOUS threshold. 20 km is the README's stated rule and
# is a round, defensible, data-independent number. Report the sensitivity.
ZONE_THRESHOLD_KM = 20.0
ZONE_THRESHOLD_SENSITIVITY = (19.5, 20.0, 25.0)


@dataclass(frozen=True)
class Params:
    """Model parameters. Frozen so an experiment cannot mutate them midway."""

    n_crews: int = 5            # m -- technician groups (3 technicians each)
    capacity: int = 3           # Q -- max faults per crew per shift
    shift_hours: float = 8.0    # H
    theta: float = 1.6          # equity tolerance; defined on [1, inf) only
    alpha: float = 0.7          # efficiency weight
    beta: float = 0.3           # equity weight
    round_trip: bool = True     # crews dispatch from base and return (scope decision)
    high_priority_weight: float = 1.0  # CORRECTION M3: keep at 1.0 for equity runs
    sla_hours: float | None = None     # optional hard cap on high-priority response

    def __post_init__(self):
        if self.theta < 1.0:
            raise ValueError(
                f"theta={self.theta} < 1. The two-sided equity cap is identically "
                "infeasible below 1: E_F <= t*E_N and E_N <= t*E_F imply E_F <= t^2*E_F. "
                "Use the epsilon-constraint to explore sub-parity."
            )
        if abs(self.alpha + self.beta - 1.0) > 1e-9:
            raise ValueError(f"alpha+beta must equal 1, got {self.alpha + self.beta}")


DEFAULT = Params()

# --- Known data-quality issues (CORRECTION M7) ---------------------------
# Documented, never silently patched. See docs/data_quality.md.
SUSPECT_TOWNS = {
    "Fodome": "0.65 km in 0.65 h implies 1.0 km/h. Near-certain transcription "
              "error; likely 6.5 km. Excluded from the speed-model calibration. "
              "No fault in the published instance occurs here.",
}
