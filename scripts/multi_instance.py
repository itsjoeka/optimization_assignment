"""Multi-instance study, restructured around a finding the first version exposed.

CORRECTION M5, revised.

The first version drew 15 random fault days and solved each with the
establishment of m = 5 crews. Thirteen of the fifteen came back INFEASIBLE --
not hard, but provably unservable: 5 crews x 8 h = 40 crew-hours cannot cover
the work a typical simulated day generates. That left two instances and no
statistical power.

That infeasibility is itself the most useful operational result in the study,
so this script reports it as a finding rather than working around it, and then
runs the efficiency comparison on a footing where every instance contributes:

  Part A -- Can the current establishment serve a typical day?
            Feasibility of m = 5 across instances, with a binomial CI.
  Part B -- How many crews would be needed?
            The minimum feasible m per instance, which is a direct answer to a
            question ECG can act on.
  Part C -- Optimum vs heuristics, with m set per instance to its minimum
            feasible value, so the comparison is like-for-like and every
            instance contributes a paired observation.

Part C's selection rule is stated explicitly because it matters: comparing only
on instances that happen to be feasible at m = 5 would condition on the outcome.
"""
from __future__ import annotations

import json
import math
import pathlib
import statistics as st
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from src import baselines as B
from src.config import Params
from src.data import job_times, priority_weights, zone_floors
from src.generate import generate_faults
from src.solver import enumerate_columns, solve
from src.verify import check_solution

OUT = pathlib.Path("result")
OUT.mkdir(exist_ok=True)

N_INST = 15
N_RAND = 2000
ESTABLISHMENT = 5          # crews ECG Hohoe actually fields
MAX_CREWS = 12


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p, d = k / n, 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def prep(faults, params):
    return {
        "travel": faults["Travel_time_hours"].tolist(),
        "repair": faults["Repair_time_hours"].tolist(),
        "zones": faults["Zone"].tolist(),
        "prio": faults["Priority"].tolist(),
        "floors": zone_floors(faults),
        "weights": priority_weights(faults, params.high_priority_weight),
        "job_time": job_times(faults, round_trip=params.round_trip),
        "n": len(faults),
    }


def attempt(d, params, columns=None):
    cols = columns if columns is not None else enumerate_columns(
        d["travel"], d["job_time"], d["zones"], d["weights"],
        params.capacity, params.shift_hours)
    s = solve(d["travel"], d["repair"], d["zones"], d["floors"], d["weights"],
              params, columns=cols)
    if s.status != "Optimal":
        return s, None, cols
    rc = check_solution(
        s.schedule, s.reported, travel=d["travel"], job_time=d["job_time"],
        zones=d["zones"], floors=d["floors"], weights=d["weights"],
        n_faults=d["n"], status=s.status, shift_hours=params.shift_hours,
        capacity=params.capacity)
    return s, rc, cols


print("=" * 78)
print("MULTI-INSTANCE STUDY")
print("=" * 78)
print(f"{N_INST} independently drawn 15-fault days against the real town network")
print(f"establishment: m = {ESTABLISHMENT} crews, Q = 3, H = 8 h\n")

rows = []
for k in range(N_INST):
    f = generate_faults(15, seed=1000 + k)
    P5 = Params(n_crews=ESTABLISHMENT)
    d = prep(f, P5)
    work = sum(d["job_time"])

    # Part A: feasible with the current establishment?
    s5, rc5, cols = attempt(d, P5)
    feasible5 = rc5 is not None

    # Part B: smallest crew count that admits a feasible plan.
    m_min, rc_min, s_min = None, None, None
    lower = max(math.ceil(d["n"] / P5.capacity), math.ceil(work / P5.shift_hours))
    for m in range(lower, MAX_CREWS + 1):
        Pm = Params(n_crews=m)
        sm, rcm, _ = attempt(d, Pm, columns=cols)
        if rcm is not None:
            m_min, rc_min, s_min = m, rcm, sm
            break

    row = {
        "seed": 1000 + k,
        "total_work_h": work,
        "utilisation_at_establishment": 100 * work / (ESTABLISHMENT * P5.shift_hours),
        "feasible_at_establishment": feasible5,
        "min_crews": m_min,
        "n_columns": len(cols),
    }
    if rc5:
        row["opt5_mean"] = rc5.weighted_mean_response
        row["opt5_gap"] = rc5.equity_gap
    print(f"  seed {1000+k}: work {work:6.2f} h "
          f"({row['utilisation_at_establishment']:5.1f}% of establishment) | "
          f"m=5 {'FEASIBLE' if feasible5 else 'infeasible'} | min crews "
          f"{m_min if m_min else '>' + str(MAX_CREWS)}")
    rows.append(row)

# ---------------------------------------------------------------- Part A
print("\n" + "-" * 78)
print("A. CAN THE CURRENT ESTABLISHMENT SERVE A TYPICAL DAY?")
print("-" * 78)
nf = sum(1 for r in rows if r["feasible_at_establishment"])
lo, hi = wilson(nf, len(rows))
util = [r["utilisation_at_establishment"] for r in rows]
print(f"\n  feasible with m = {ESTABLISHMENT}: {nf} of {len(rows)} days "
      f"({100*nf/len(rows):.1f}%, Wilson 95% CI [{100*lo:.1f}%, {100*hi:.1f}%])")
print(f"  required crew-time: mean {st.mean([r['total_work_h'] for r in rows]):.2f} h, "
      f"range [{min(r['total_work_h'] for r in rows):.2f}, "
      f"{max(r['total_work_h'] for r in rows):.2f}] h")
print(f"  available crew-time: {ESTABLISHMENT * 8} h")
print(f"  utilisation implied: mean {st.mean(util):.1f}%, "
      f"range [{min(util):.1f}%, {max(util):.1f}%]")
print(f"\n  On most simulated days the work required EXCEEDS the crew-hours")
print(f"  available, so no assignment exists -- this is a statement about")
print(f"  resourcing, not about the solver.")

# ---------------------------------------------------------------- Part B
print("\n" + "-" * 78)
print("B. HOW MANY CREWS WOULD BE NEEDED?")
print("-" * 78)
mins = [r["min_crews"] for r in rows if r["min_crews"]]
print(f"\n  minimum crews to serve the day, over {len(mins)} instances:")
print(f"    mean {st.mean(mins):.2f} | median {st.median(mins)} | "
      f"range [{min(mins)}, {max(mins)}]")
dist = {m: mins.count(m) for m in sorted(set(mins))}
print(f"\n  | Crews required | Days | Cumulative coverage |")
print(f"  |---|---|---|")
cum = 0
for m, c in dist.items():
    cum += c
    print(f"  | {m} | {c} | {100*cum/len(mins):.1f}% |")
print(f"\n  {ESTABLISHMENT} crews cover {100*sum(c for m,c in dist.items() if m<=ESTABLISHMENT)/len(mins):.1f}% "
      f"of days; {max(mins)} crews cover all of them.")

# ---------------------------------------------------------------- Part C
print("\n" + "-" * 78)
print("C. OPTIMUM vs HEURISTICS (crews set per instance to the minimum feasible)")
print("-" * 78)
print("\n  Selection rule stated explicitly: comparing only on days that happen to")
print("  be feasible at m = 5 would condition on the outcome and bias the result.")
print("  Each instance is instead solved at its own minimum feasible crew count,")
print("  so every instance contributes one paired observation.\n")

paired = []
for r in rows:
    if not r["min_crews"]:
        continue
    f = generate_faults(15, seed=r["seed"])
    Pm = Params(n_crews=r["min_crews"])
    d = prep(f, Pm)
    sm, rcm, cols = attempt(d, Pm)
    if rcm is None:
        continue
    bl = B.run_all(d["n"], Pm, d["travel"], d["job_time"], d["zones"],
                   d["floors"], d["weights"], d["prio"], n_random=N_RAND)
    bl.pop("_schedules")
    ls = bl["local_search"]
    bfd = bl["greedy_bfd_repair"]
    rr = bl["random_round_robin"]
    opt_obj = Pm.alpha * rcm.weighted_mean_response + Pm.beta * rcm.equity_gap
    r.update({
        "cmp_crews": r["min_crews"],
        "opt_mean": rcm.weighted_mean_response, "opt_gap": rcm.equity_gap,
        "opt_objective": opt_obj,
        "far_near": (rcm.zone_mean["Far"] / rcm.zone_mean["Near"]
                     if "Far" in rcm.zone_mean and "Near" in rcm.zone_mean else None),
        "random_feasibility_rate": rr["feasibility_rate"],
        "ls_mean": ls["weighted_mean_response"] if ls else None,
        "ls_gap": ls["equity_gap"] if ls else None,
        "ls_objective": ls["objective"] if ls else None,
        "bfd_objective": bfd["objective"] if bfd else None,
    })
    if ls:
        paired.append((opt_obj, ls["objective"], rcm.weighted_mean_response,
                       ls["weighted_mean_response"], rcm.equity_gap, ls["equity_gap"]))
    print(f"  seed {r['seed']} (m={r['min_crews']}): opt obj {opt_obj:.4f} "
          f"mean {rcm.weighted_mean_response:.4f} gap {rcm.equity_gap:.4f} | "
          f"LS obj {ls['objective']:.4f}" if ls else
          f"  seed {r['seed']} (m={r['min_crews']}): opt obj {opt_obj:.4f} | LS failed")

if len(paired) >= 6:
    from scipy.stats import wilcoxon
    oo = [p[0] for p in paired]; lo_ = [p[1] for p in paired]
    om = [p[2] for p in paired]; lm = [p[3] for p in paired]
    og = [p[4] for p in paired]; lg = [p[5] for p in paired]
    d_obj = [100 * (b - a) / a for a, b in zip(oo, lo_)]
    d_mean = [100 * (b - a) / a for a, b in zip(om, lm)]
    d_gap = [b - a for a, b in zip(og, lg)]
    print(f"\n  paired comparison on {len(paired)} instances\n")
    print("  | Measure | Median difference (heuristic - optimum) | Wilcoxon W | p |")
    print("  |---|---|---|---|")
    for label, a, b, diffs, unit in (
        ("Objective", oo, lo_, d_obj, "%"),
        ("Mean response", om, lm, d_mean, "%"),
        ("Equity gap", og, lg, d_gap, " h"),
    ):
        try:
            W, p = wilcoxon(a, b)
            print(f"  | {label} | {st.median(diffs):+.4f}{unit} | {W:.1f} | {p:.5f} |")
        except ValueError as e:
            print(f"  | {label} | {st.median(diffs):+.4f}{unit} | n/a | {e} |")
    print("\n  Wilcoxon signed-rank rather than a t-test: these paired differences")
    print("  are not normally distributed and the sample is small.")
    print()
    print("  READ THE MAGNITUDE, NOT THE p-VALUE. The optimum minimises the very")
    print("  objective being compared, so it can never lose to a heuristic: the sign")
    print("  of every difference is fixed by construction and W = 0 simply confirms")
    print("  that. Significance here is close to automatic and is NOT evidence that")
    print("  the improvement is large. The median difference is the honest number,")
    print("  and the paper should lead with it.")
else:
    print(f"\n  only {len(paired)} paired observations -- too few for a signed-rank test")

json.dump(rows, open(OUT / "multi_instance.json", "w"), indent=1, default=str)
print(f"\nwritten to {OUT / 'multi_instance.json'}")
print("=" * 78)
