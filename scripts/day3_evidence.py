"""Day 3 evidence suite: baselines, sensitivity, multi-instance, scaling.

Corrections B5, M3, M4, M5, M6.

Every solve goes through src.verify.check_solution before its numbers are kept.
Results are written to result/ section by section, so a later failure does not
lose earlier work.
"""
from __future__ import annotations

import json
import math
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from src import baselines as B
from src.config import Params, ZONE_THRESHOLD_SENSITIVITY
from src.data import job_times, load_faults, priority_weights, zone_floors
from src.generate import generate_faults
from src.solver import enumerate_columns, solve
from src.verify import check_solution

OUT = pathlib.Path("result")
OUT.mkdir(exist_ok=True)
(OUT / "sensitivity").mkdir(exist_ok=True)


def instance(faults, params, high_weight=1.0):
    """Everything a run needs, derived once."""
    tr = faults["Travel_time_hours"].tolist()
    rp = faults["Repair_time_hours"].tolist()
    z = faults["Zone"].tolist()
    return {
        "travel": tr, "repair": rp, "zones": z,
        "floors": zone_floors(faults),
        "weights": priority_weights(faults, high_weight),
        "job_time": job_times(faults, round_trip=params.round_trip),
        "priorities": faults["Priority"].tolist(),
        "n": len(faults),
    }


def solved(inst, params, *, columns=None, verify=True, **kw):
    """Solve and verify. Returns (solution, recomputed) or (solution, None)."""
    s = solve(inst["travel"], inst["repair"], inst["zones"], inst["floors"],
              inst["weights"], params, columns=columns, **kw)
    if s.status != "Optimal" or not verify:
        return s, None
    rc = check_solution(
        s.schedule, s.reported, travel=inst["travel"], job_time=inst["job_time"],
        zones=inst["zones"], floors=inst["floors"], weights=inst["weights"],
        n_faults=inst["n"], status=s.status, shift_hours=params.shift_hours,
        capacity=params.capacity,
    )
    return s, rc


def wilson(k, n, z=1.96):
    """Wilson score interval -- correct for proportions near 0 or 1, unlike normal."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, centre - half), min(1.0, centre + half))


P = Params()
faults = load_faults()
inst = instance(faults, P)
cols = enumerate_columns(inst["travel"], inst["job_time"], inst["zones"],
                         inst["weights"], P.capacity, P.shift_hours)
results = {}

print("=" * 74)
print("DAY 3 EVIDENCE SUITE")
print("=" * 74)
print(f"published instance: n={inst['n']}, m={P.n_crews}, Q={P.capacity}, "
      f"H={P.shift_hours} h | {len(cols)} feasible columns")

# =====================================================================
# 1. BASELINES (B5)
# =====================================================================
print("\n" + "-" * 74)
print("1. BASELINES -- feasibility-aware")
print("-" * 74)
opt, opt_rc = solved(inst, P, columns=cols)
opt_mean = opt_rc.weighted_mean_response
opt_gap = opt_rc.equity_gap
opt_obj = P.alpha * opt_mean + P.beta * opt_gap
print(f"OPTIMUM            mean {opt_mean:.4f} h | gap {opt_gap:.4f} h | "
      f"objective {opt_obj:.4f} | makespan {opt_rc.makespan:.3f} h | {opt.solve_seconds:.2f}s")

bl = B.run_all(inst["n"], P, inst["travel"], inst["job_time"], inst["zones"],
               inst["floors"], inst["weights"], inst["priorities"], n_random=5000)
sched_store = bl.pop("_schedules")

print()
for name in ("random_round_robin", "random_best_order"):
    r = bl[name]
    print(f"{name:20s} feasible {r['n_feasible']:>5}/{r['n_trials']} "
          f"({100 * r['feasibility_rate']:5.2f}%)", end="")
    if r["n_feasible"]:
        lo, hi = wilson(r["n_feasible"], r["n_trials"])
        print(f" | mean-of-feasible {r['mean_of_feasible']:.4f} h"
              f" | best-of-N {r['best_of_n']:.4f} h"
              f" | 95% CI [{100*lo:.2f}%, {100*hi:.2f}%]")
    else:
        print(" | NO FEASIBLE DRAW")

print()
for name in ("greedy_bfd_repair", "greedy_longest_job", "greedy_shortest_job",
             "greedy_nearest", "greedy_priority", "zone_clustered", "local_search"):
    r = bl[name]
    if r is None:
        print(f"{name:20s} FAILED to produce a feasible plan")
        continue
    delta = 100 * (r["weighted_mean_response"] - opt_mean) / opt_mean
    dobj = 100 * (r["objective"] - opt_obj) / opt_obj
    print(f"{name:20s} mean {r['weighted_mean_response']:.4f} h ({delta:+6.2f}%)"
          f" | gap {r['equity_gap']:.4f} h"
          f" | objective {r['objective']:.4f} ({dobj:+6.2f}% vs optimum)")

results["baselines"] = {"optimum": {"mean_response": opt_mean, "gap": opt_gap,
                                    "objective": opt_obj, "makespan": opt_rc.makespan,
                                    "solve_seconds": opt.solve_seconds},
                        "policies": bl}
json.dump(results["baselines"], open(OUT / "baselines.json", "w"), indent=1)

# =====================================================================
# 2. PRIORITY: the confound, and the SLA sweep (M3)
# =====================================================================
print("\n" + "-" * 74)
print("2. PRIORITY")
print("-" * 74)
print("\n2a. priority/zone confound -- 4 of 5 High-priority faults are Far,")
print("    so weighting alone moves the ratio with no equity mechanism working")
conf = []
for wh in (1.0, 1.5, 2.0, 3.0):
    i2 = instance(faults, P, high_weight=wh)
    c2 = enumerate_columns(i2["travel"], i2["job_time"], i2["zones"],
                           i2["weights"], P.capacity, P.shift_hours)
    s2, r2 = solved(i2, P, columns=c2)
    if r2:
        hi_idx = [j for j, p in enumerate(i2["priorities"]) if p == "High"]
        hi_mean = sum(r2.response[j] for j in hi_idx) / len(hi_idx)
        ratio = r2.zone_mean["Far"] / r2.zone_mean["Near"]
        print(f"    w_High={wh:<4} mean {r2.weighted_mean_response:.4f} h | "
              f"Far/Near {ratio:.4f} | mean High-priority arrival {hi_mean:.4f} h")
        conf.append({"w_high": wh, "mean_response": r2.weighted_mean_response,
                     "far_near_ratio": ratio, "high_mean_arrival": hi_mean,
                     "gap": r2.equity_gap})

print("\n2b. SLA sweep -- hard cap on high-priority response (w_High = 1)")
hi_idx = [j for j, p in enumerate(inst["priorities"]) if p == "High"]
sla = []
for D in (None, 3.0, 2.5, 2.0, 1.5, 1.2, 1.0, 0.8):
    Pd = Params(sla_hours=D)
    cD = enumerate_columns(inst["travel"], inst["job_time"], inst["zones"],
                           inst["weights"], Pd.capacity, Pd.shift_hours,
                           sla_hours=D, sla_faults=hi_idx)
    sD, rD = solved(inst, Pd, columns=cD, sla_faults=hi_idx)
    label = "none" if D is None else f"{D} h"
    if rD:
        hm = sum(rD.response[j] for j in hi_idx) / len(hi_idx)
        pen = 100 * (rD.weighted_mean_response - opt_mean) / opt_mean
        print(f"    D={label:<6} cols {len(cD):>5} | mean {rD.weighted_mean_response:.4f} h "
              f"({pen:+6.2f}%) | mean High arrival {hm:.4f} h | {sD.status}")
        sla.append({"D": D, "n_columns": len(cD),
                    "mean_response": rD.weighted_mean_response,
                    "high_mean_arrival": hm, "penalty_pct": pen,
                    "status": sD.status})
    else:
        print(f"    D={label:<6} cols {len(cD):>5} | {sD.status}")
        sla.append({"D": D, "n_columns": len(cD), "status": sD.status})

results["priority"] = {"confound": conf, "sla_sweep": sla}
json.dump(results["priority"], open(OUT / "sensitivity" / "priority.json", "w"), indent=1)

# =====================================================================
# 3. SENSITIVITY (M4)
# =====================================================================
print("\n" + "-" * 74)
print("3. SENSITIVITY")
print("-" * 74)
sens = {}

print("\n3a. epsilon-constraint frontier (the weighted sum recovers only")
print("    supported Pareto points, so the frontier figure must use this)")
eff_only, eff_rc = solved(inst, Params(alpha=1.0, beta=0.0), columns=cols)
z_eff = eff_rc.weighted_mean_response
front = []
for eps in (0.0, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20, 0.30):
    se, re = solved(inst, P, columns=cols, epsilon_budget=z_eff * (1 + eps))
    if re:
        print(f"    eps={eps:<5} budget {z_eff*(1+eps):.4f} h | "
              f"mean {re.weighted_mean_response:.4f} h | gap {re.equity_gap:.4f} h")
        front.append({"epsilon": eps, "mean_response": re.weighted_mean_response,
                      "gap": re.equity_gap, "max_response": re.max_response})
sens["epsilon_frontier"] = front
sens["efficiency_only"] = {"mean_response": z_eff, "gap": eff_rc.equity_gap}

print("\n3b. capacity Q")
qs = []
for Q in (2, 3, 4, 5):
    Pq = Params(capacity=Q)
    cq = enumerate_columns(inst["travel"], inst["job_time"], inst["zones"],
                           inst["weights"], Q, Pq.shift_hours)
    sq, rq = solved(inst, Pq, columns=cq)
    if rq:
        loads = sorted((len(v) for v in sq.schedule.values()), reverse=True)
        print(f"    Q={Q} cols {len(cq):>6} | mean {rq.weighted_mean_response:.4f} h | "
              f"gap {rq.equity_gap:.4f} | loads {loads} | {sq.solve_seconds:.2f}s")
        qs.append({"Q": Q, "n_columns": len(cq),
                   "mean_response": rq.weighted_mean_response,
                   "gap": rq.equity_gap, "loads": loads,
                   "solve_seconds": sq.solve_seconds})
    else:
        print(f"    Q={Q} cols {len(cq):>6} | {sq.status}")
        qs.append({"Q": Q, "n_columns": len(cq), "status": sq.status})
sens["capacity"] = qs

print("\n3c. shift length H")
hs = []
for H in (6.0, 7.0, 8.0, 9.0, 10.0):
    Ph = Params(shift_hours=H)
    ch = enumerate_columns(inst["travel"], inst["job_time"], inst["zones"],
                           inst["weights"], Ph.capacity, H)
    sh, rh = solved(inst, Ph, columns=ch)
    if rh:
        print(f"    H={H:<5} cols {len(ch):>5} | mean {rh.weighted_mean_response:.4f} h | "
              f"gap {rh.equity_gap:.4f} | makespan {rh.makespan:.3f} h")
        hs.append({"H": H, "n_columns": len(ch),
                   "mean_response": rh.weighted_mean_response,
                   "gap": rh.equity_gap, "makespan": rh.makespan})
    else:
        print(f"    H={H:<5} cols {len(ch):>5} | {sh.status}")
        hs.append({"H": H, "n_columns": len(ch), "status": sh.status})
sens["shift"] = hs

print("\n3d. zone threshold -- the decision taken before any result was generated")
ths = []
for thr in ZONE_THRESHOLD_SENSITIVITY:
    ft = load_faults(threshold_km=thr)
    it = instance(ft, P)
    ct = enumerate_columns(it["travel"], it["job_time"], it["zones"],
                           it["weights"], P.capacity, P.shift_hours)
    st, rt = solved(it, P, columns=ct)
    if rt:
        nn = sum(1 for x in it["zones"] if x == "Near")
        print(f"    threshold={thr:<5} km | Near {nn}, Far {it['n']-nn} | "
              f"mean {rt.weighted_mean_response:.4f} h | gap {rt.equity_gap:.4f} h")
        ths.append({"threshold_km": thr, "n_near": nn, "n_far": it["n"] - nn,
                    "mean_response": rt.weighted_mean_response, "gap": rt.equity_gap})
sens["zone_threshold"] = ths

results["sensitivity"] = sens
json.dump(sens, open(OUT / "sensitivity" / "sensitivity.json", "w"), indent=1)

# =====================================================================
# 4. MULTI-INSTANCE STUDY (M5)
# =====================================================================
print("\n" + "-" * 74)
print("4. MULTI-INSTANCE STUDY -- 15 instances")
print("-" * 74)
print("feasibility rate is the PRIMARY endpoint; the efficiency comparison is")
print("conditional on the baseline being feasible at all\n")

N_INST, N_RAND = 15, 2000
rows, paired = [], []
for k in range(N_INST):
    fk = generate_faults(15, seed=1000 + k)
    ik = instance(fk, P)
    ck = enumerate_columns(ik["travel"], ik["job_time"], ik["zones"],
                           ik["weights"], P.capacity, P.shift_hours)
    sk, rk = solved(ik, P, columns=ck)
    if rk is None:
        print(f"  inst {k:2d}: optimum {sk.status} ({len(ck)} cols)")
        rows.append({"seed": 1000 + k, "status": sk.status, "n_columns": len(ck)})
        continue
    bk = B.run_all(ik["n"], P, ik["travel"], ik["job_time"], ik["zones"],
                   ik["floors"], ik["weights"], ik["priorities"], n_random=N_RAND)
    bk.pop("_schedules")
    rr = bk["random_round_robin"]
    gs = bk["greedy_bfd_repair"] or bk["greedy_longest_job"]
    ls = bk["local_search"]
    row = {
        "seed": 1000 + k, "status": "Optimal", "n_columns": len(ck),
        "opt_mean": rk.weighted_mean_response, "opt_gap": rk.equity_gap,
        "opt_makespan": rk.makespan, "opt_max_response": rk.max_response,
        "opt_excess_near": rk.zone_excess.get("Near"),
        "opt_excess_far": rk.zone_excess.get("Far"),
        "opt_far_near_ratio": (rk.zone_mean["Far"] / rk.zone_mean["Near"]
                               if "Far" in rk.zone_mean and "Near" in rk.zone_mean
                               else None),
        "random_feasibility_rate": rr["feasibility_rate"],
        "random_mean_of_feasible": rr["mean_of_feasible"],
        "random_best_of_n": rr["best_of_n"],
        "greedy_mean": gs["weighted_mean_response"] if gs else None,
        "greedy_gap": gs["equity_gap"] if gs else None,
        "ls_mean": ls["weighted_mean_response"] if ls else None,
        "ls_gap": ls["equity_gap"] if ls else None,
    }
    rows.append(row)
    if ls:
        paired.append((rk.weighted_mean_response, ls["weighted_mean_response"]))
    print(f"  inst {k:2d}: opt {rk.weighted_mean_response:.4f} h gap {rk.equity_gap:.4f} | "
          f"random feasible {100*rr['feasibility_rate']:5.2f}% | "
          f"greedy {gs['weighted_mean_response']:.4f} " if gs else "", end="")
    print(f"| LS {ls['weighted_mean_response']:.4f}" if ls else "| LS failed")

ok = [r for r in rows if r.get("status") == "Optimal"]
print(f"\n  optimum solved {len(ok)}/{N_INST} instances")
if ok:
    import statistics as st
    fr = [r["random_feasibility_rate"] for r in ok]
    print(f"  random-dispatch feasibility rate: mean {100*st.mean(fr):.2f}%, "
          f"median {100*st.median(fr):.2f}%, range [{100*min(fr):.2f}%, {100*max(fr):.2f}%]")
    tot_f = sum(round(r["random_feasibility_rate"] * N_RAND) for r in ok)
    lo, hi = wilson(tot_f, len(ok) * N_RAND)
    print(f"  pooled over {len(ok)*N_RAND} draws: {100*tot_f/(len(ok)*N_RAND):.2f}% "
          f"(Wilson 95% CI [{100*lo:.2f}%, {100*hi:.2f}%])")
    eq = [r["opt_gap"] for r in ok]
    rat = [r["opt_far_near_ratio"] for r in ok if r["opt_far_near_ratio"]]
    print(f"  equity gap at optimum: mean {st.mean(eq):.4f} h, "
          f"range [{min(eq):.4f}, {max(eq):.4f}]")
    print(f"  Far/Near ratio at optimum: mean {st.mean(rat):.4f}, "
          f"range [{min(rat):.4f}, {max(rat):.4f}]")
    if len(paired) >= 6:
        try:
            from scipy.stats import wilcoxon
            a = [x for x, _ in paired]
            b = [y for _, y in paired]
            stat, p = wilcoxon(a, b)
            d = [100 * (y - x) / x for x, y in paired]
            print(f"\n  optimum vs local search on {len(paired)} instances where both "
                  f"are feasible:")
            print(f"    local search is worse by a median of {st.median(d):.2f}% "
                  f"(range [{min(d):.2f}%, {max(d):.2f}%])")
            print(f"    Wilcoxon signed-rank W={stat:.1f}, p={p:.5f}")
            results["wilcoxon"] = {"n": len(paired), "W": float(stat), "p": float(p),
                                   "median_pct_worse": st.median(d)}
        except ImportError:
            print("  scipy unavailable -- Wilcoxon skipped")

results["multi_instance"] = rows
json.dump(rows, open(OUT / "multi_instance.json", "w"), indent=1)

# =====================================================================
# 5. SCALING (M6)
# =====================================================================
print("\n" + "-" * 74)
print("5. SCALING -- crews scaled as m = ceil(n/3)")
print("-" * 74)
print("holding m=5 while scaling n makes every instance infeasible on repair")
print("time alone from n=30 upward, so the rule is stated and applied\n")
scale = []
for n in (15, 24, 30, 45, 60):
    m = math.ceil(n / 3)
    Pn = Params(n_crews=m)
    fn = generate_faults(n, seed=2000 + n)
    inn = instance(fn, Pn)
    t0 = time.time()
    cn = enumerate_columns(inn["travel"], inn["job_time"], inn["zones"],
                           inn["weights"], Pn.capacity, Pn.shift_hours)
    enum_s = time.time() - t0
    sn, rn = solved(inn, Pn, columns=cn, time_limit=600)
    total = 0
    for sz in range(1, Pn.capacity + 1):
        p = 1
        for q in range(sz):
            p *= (n - q)
        total += p
    msg = (f"    n={n:<3} m={m:<2} | {len(cn):>7}/{total:<9} cols "
           f"({enum_s:5.2f}s enum) | {sn.status}")
    if rn:
        msg += (f" | mean {rn.weighted_mean_response:.4f} h | "
                f"solve {sn.solve_seconds - enum_s:6.2f}s")
    print(msg)
    scale.append({"n": n, "m": m, "n_columns": len(cn), "total_possible": total,
                  "enumerate_seconds": enum_s, "status": sn.status,
                  "solve_seconds": sn.solve_seconds - enum_s,
                  "mean_response": rn.weighted_mean_response if rn else None})
results["scaling"] = scale
json.dump(scale, open(OUT / "sensitivity" / "scaling.json", "w"), indent=1)

json.dump({k: v for k, v in results.items() if k != "baselines"},
          open(OUT / "day3_summary.json", "w"), indent=1, default=str)
print("\n" + "=" * 74)
print("DAY 3 EVIDENCE SUITE COMPLETE -- all solves verified at 1e-6")
print("=" * 74)
