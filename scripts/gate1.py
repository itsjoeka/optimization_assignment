"""Gate 1 -- run before generating any number that will appear in the paper.

Four checks. All four must pass. Check 4 is the one that catches the defect
class that has twice nearly sunk this project.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from src.config import Params
from src.data import load_faults, job_times, priority_weights, zone_floors
from src.solver import enumerate_columns, solve
from src.verify import VerificationError, check_solution, objective_varies

f = load_faults()
tr = f["Travel_time_hours"].tolist()
rp = f["Repair_time_hours"].tolist()
z = f["Zone"].tolist()
fl = zone_floors(f)
w = priority_weights(f, 1.0)          # CORRECTION M3: confound control
P = Params()
jt = job_times(f, round_trip=P.round_trip)
V = dict(travel=tr, job_time=jt, zones=z, floors=fl, weights=w,
         n_faults=len(f), shift_hours=P.shift_hours, capacity=P.capacity)
cols = enumerate_columns(tr, jt, z, w, P.capacity, P.shift_hours)
R = {}

print("=" * 72)
print("GATE 1")
print("=" * 72)
print(f"\ncolumns: {len(cols)} shift-feasible of "
      f"{15 + 15 * 14 + 15 * 14 * 13} possible")

# --- 4. Does the model's own arithmetic survive recomputation? --------------
base = solve(tr, rp, z, fl, w, P, columns=cols)
print(f"\nbase solve: {base.status}  obj={base.objective:.6f}  "
      f"{base.solve_seconds:.2f}s")
try:
    rc = check_solution(base.schedule, base.reported, status=base.status, **V)
    print("  [4] VERIFICATION PASSED at 1e-6")
    print(f"      mean response {rc.weighted_mean_response:.4f} h | "
          f"makespan {rc.makespan:.4f} h | worst wait {rc.max_response:.4f} h")
    print(f"      excess wait: Near {rc.zone_excess['Near']:.4f} h, "
          f"Far {rc.zone_excess['Far']:.4f} h, gap {rc.equity_gap:.4f} h")
    R["verification"] = True
except VerificationError as e:
    print(f"  [4] VERIFICATION FAILED: {e}")
    R["verification"] = False

# --- 1. Does the objective vary over the feasible set? ----------------------
eff = Params(alpha=1.0, beta=0.0)
lo = solve(tr, rp, z, fl, w, eff, sense="min", columns=cols)
hi = solve(tr, rp, z, fl, w, eff, sense="max", columns=cols)
lo_v = lo.reported["weighted_mean_response"]
hi_v = hi.reported["weighted_mean_response"]
ok1, spread = objective_varies([lo_v, hi_v])
print(f"\n  [1] NON-DEGENERACY")
print(f"      min mean response {lo_v:.4f} h | max {hi_v:.4f} h "
      f"| spread {spread:.1f}%  -> {'PASS' if ok1 else 'FAIL'}")
print(f"      the OLD travel objective scores {sum(tr):.3f} h for BOTH "
      f"-- 0.0% spread, which is the defect")
R["non_degenerate"], R["spread_pct"] = ok1, spread

# --- 2. Does the equity constraint bind? ------------------------------------
print("\n  [2] EQUITY -- theta sweep")
prev, binds, sweep = None, False, []
for th in (2.0, 1.6, 1.4, 1.2, 1.1, 1.05, 1.0):
    s2 = solve(tr, rp, z, fl, w, Params(theta=th), columns=cols)
    if s2.status == "Optimal":
        r2 = check_solution(s2.schedule, s2.reported, status=s2.status, **V)
        tag = ""
        if prev is not None and abs(r2.weighted_mean_response - prev) > 1e-6:
            tag, binds = "   <- solution CHANGED", True
        print(f"      theta={th:<5} mean {r2.weighted_mean_response:.4f} h   "
              f"gap {r2.equity_gap:.4f} h{tag}")
        sweep.append({"theta": th, "mean_response": r2.weighted_mean_response,
                      "gap": r2.equity_gap, "status": s2.status})
        prev = r2.weighted_mean_response
    else:
        print(f"      theta={th:<5} {s2.status}"
              f"   <- infeasible through the decision variables")
        sweep.append({"theta": th, "status": s2.status})
        binds = True
print(f"      -> {'PASS' if binds else 'FAIL'}")
R["equity_binds"], R["theta_sweep"] = binds, sweep

# --- 3. Do different alpha/beta give different solutions? -------------------
print("\n  [3] WEIGHTS -- alpha/beta sweep")
plans, ab = {}, []
for b in (0.0, 0.3, 0.5, 0.7, 1.0):
    s3 = solve(tr, rp, z, fl, w, Params(alpha=1 - b, beta=b), columns=cols)
    if s3.status == "Optimal":
        r3 = check_solution(s3.schedule, s3.reported, status=s3.status, **V)
        key = tuple(sorted(tuple(v) for v in s3.schedule.values()))
        plans.setdefault(key, []).append(b)
        print(f"      beta={b:<4} mean {r3.weighted_mean_response:.4f} h   "
              f"gap {r3.equity_gap:.4f} h")
        ab.append({"beta": b, "mean_response": r3.weighted_mean_response,
                   "gap": r3.equity_gap})
ok3 = len(plans) > 1
print(f"      -> {len(plans)} distinct plans across 5 weightings: "
      f"{'PASS' if ok3 else 'FAIL'}")
if len(plans) < len(ab):
    print("      NOTE: the weighted sum recovers only supported Pareto points.")
    print("      Use the epsilon-constraint for the frontier figure.")
R["weights_matter"], R["alpha_beta_sweep"] = ok3, ab

passed = all(R.get(k) for k in
             ("verification", "non_degenerate", "equity_binds", "weights_matter"))
print("\n" + "=" * 72)
print("GATE 1: " + ("PASSED -- safe to generate paper numbers"
                    if passed else "FAILED -- do not proceed"))
print("=" * 72)
R["passed"] = passed
R["n_columns"] = len(cols)
pathlib.Path("result").mkdir(exist_ok=True)
json.dump(R, open("result/gate1.json", "w"), indent=1)
