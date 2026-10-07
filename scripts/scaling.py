"""Scaling study (M6), reporting solver exit conditions honestly.

Two things this gets right that the first version did not.

CREW COUNT. There are two capacity dimensions: faults per crew (m*Q >= n) and
crew-hours (m*H >= total work). Scaling only the first -- m = ceil(n/Q), as an
earlier draft did -- makes m*Q exactly equal n while ignoring the workload, which
pushed utilisation above 100% at every size and made the instances genuinely
infeasible rather than merely hard. The rule here respects both and holds crew
utilisation at the published instance's level.

SOLVER STATUS. PuLP reports LpStatus 'Optimal' whenever CBC returns a feasible
solution, including when CBC stopped on its time limit having proved nothing.
src.solver now reads CBC's own log and distinguishes the two, so this table can
say "proven optimal" only where the search actually completed, and report the
remaining gap where it did not.
"""
from __future__ import annotations

import json
import math
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from src.config import Params
from src.data import job_times, priority_weights, zone_floors
from src.generate import generate_faults
from src.solver import enumerate_columns, solve
from src.verify import check_solution

OUT = pathlib.Path("result/sensitivity")
OUT.mkdir(parents=True, exist_ok=True)

TARGET_UTILISATION = 0.951     # crew utilisation of the published n=15 instance
TIME_LIMIT = 600
SIZES = (15, 24, 30, 45, 60)

P0 = Params()
rows = []

print("=" * 86)
print("SCALING STUDY")
print("=" * 86)
print(f"crew rule: m = max( ceil(n/Q), ceil(total_work / (H * u)) ),  u = {TARGET_UTILISATION}")
print(f"solver budget: {TIME_LIMIT} s per instance\n")

for n in SIZES:
    f = generate_faults(n, seed=2000 + n)
    tr = f["Travel_time_hours"].tolist()
    rp = f["Repair_time_hours"].tolist()
    z = f["Zone"].tolist()
    fl = zone_floors(f)
    w = priority_weights(f, P0.high_priority_weight)
    s = job_times(f, round_trip=P0.round_trip)
    work = sum(s)
    m = max(math.ceil(n / P0.capacity),
            math.ceil(work / (P0.shift_hours * TARGET_UTILISATION)))
    P = Params(n_crews=m)

    t0 = time.time()
    cols = enumerate_columns(tr, s, z, w, P.capacity, P.shift_hours)
    enum_s = time.time() - t0

    sol = solve(tr, rp, z, fl, w, P, columns=cols, time_limit=TIME_LIMIT)
    meta = sol.columns
    possible = sum(math.perm(n, k) for k in range(1, P.capacity + 1))
    util = 100 * work / (m * P.shift_hours)

    mean_txt, verified = "—", False
    if sol.schedule:
        rc = check_solution(
            sol.schedule, sol.reported, travel=tr, job_time=s, zones=z, floors=fl,
            weights=w, n_faults=n, status=sol.status,
            shift_hours=P.shift_hours, capacity=P.capacity)
        mean_txt = f"{rc.weighted_mean_response:.4f} h"
        verified = True

    if meta.get("search_completed"):
        verdict = "proven optimal"
    elif meta.get("hit_time_limit"):
        g = meta.get("final_gap")
        verdict = (f"incumbent, gap {g:.2f}% at {TIME_LIMIT}s"
                   if g is not None else f"incumbent at {TIME_LIMIT}s")
    else:
        verdict = sol.status

    print(f"  n={n:<3} m={m:<3} util {util:5.1f}% | cols {len(cols):>6}/{possible:<9}"
          f" | enum {enum_s:5.2f}s | solve {meta['solve_seconds']:7.2f}s"
          f" | {verdict:<32} | mean {mean_txt}")

    rows.append({
        "n": n, "m": m, "utilisation_pct": util, "total_work_h": work,
        "n_columns": len(cols), "total_possible": possible,
        "enumerate_seconds": enum_s, "solve_seconds": meta["solve_seconds"],
        "pulp_status": sol.status,
        "search_completed": meta.get("search_completed"),
        "hit_time_limit": meta.get("hit_time_limit"),
        "final_gap_pct": meta.get("final_gap"),
        "proven_optimal": bool(meta.get("search_completed")),
        "verified": verified,
        "mean_response": (None if mean_txt == "—" else float(mean_txt.split()[0])),
    })

json.dump(rows, open(OUT / "scaling.json", "w"), indent=1)
proven = [r["n"] for r in rows if r["proven_optimal"]]
unproven = [r["n"] for r in rows if not r["proven_optimal"]]
print()
print(f"  proven optimal at n = {proven}")
if unproven:
    print(f"  incumbent only at n = {unproven} within the {TIME_LIMIT}s budget")
    print("  -- report these as 'solved to within x% in y seconds', never as optima")
print(f"\nwritten to {OUT / 'scaling.json'}")
print("=" * 86)
