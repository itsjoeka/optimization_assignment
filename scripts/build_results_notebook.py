"""Generate notebooks/05_manuscript_results.ipynb.

Keeping the notebook in a generator rather than hand-editing JSON means the
cells stay readable in diffs and cannot drift from src/.
"""
import json
import pathlib

MD = "markdown"
CODE = "code"


def cell(kind, text):
    lines = text.strip("\n").splitlines(keepends=True)
    if kind == MD:
        return {"cell_type": MD, "metadata": {}, "source": lines}
    return {"cell_type": CODE, "execution_count": None, "metadata": {},
            "outputs": [], "source": lines}


cells = []
A = cells.append

A(cell(MD, """
# Manuscript Results

Every number in the paper, regenerated from source. Run this notebook top to
bottom from a clean kernel and each table below is ready to paste into the
manuscript.

**What this notebook is for.** The results in the paper must be reproducible by
anyone who downloads this repository. This notebook is the bridge: it imports
the same `src/` modules the experiments use, so a number here cannot drift from
a number in the paper.

**Before trusting any output below**, note that every solve is passed through
`src.verify.check_solution`, which recomputes the response times, zone excess
waits, equity gap, makespan and crew loads *from the chosen schedule* in plain
Python and asserts they match what the solver reported, to 1e-6. If any cell
raises `VerificationError`, **no number in this notebook can be used**.

| Section | Produces |
|---|---|
| 1 | Environment and data provenance |
| 2 | Table 1 — instance description |
| 3 | Table 2 — why the original objective could not work |
| 4 | Table 3 — the optimal dispatch plan |
| 5 | Table 4 — comparison against dispatch heuristics |
| 6 | Table 5 — efficiency/equity frontier |
| 7 | Table 6 — priority SLA sweep |
| 8 | Table 7 — parameter sensitivity |
| 9 | Table 8 — multi-instance study and significance test |
| 10 | Table 9 — scaling |
| 11 | Figures |
"""))

A(cell(MD, "## 1. Environment and provenance"))

A(cell(CODE, '''
import json, math, pathlib, platform, statistics as st, sys

ROOT = pathlib.Path.cwd().parent if pathlib.Path.cwd().name == "notebooks" else pathlib.Path.cwd()
sys.path.insert(0, str(ROOT))

import pandas as pd
import pulp

from src import baselines as B
from src.config import Params, ZONE_THRESHOLD_KM, ZONE_THRESHOLD_SENSITIVITY
from src.data import (describe_instance, job_times, load_faults, load_towns,
                      priority_weights, zone_floors)
from src.generate import PUBLISHED_SEED, generate_faults, reproduces_published
from src.solver import enumerate_columns, solve
from src.verify import VerificationError, check_solution, objective_varies

# Set False to also recompute the slowest scaling points (n = 45, 60).
# They take several minutes each; everything else computes live regardless.
QUICK = True

print(f"python {platform.python_version()} | pandas {pd.__version__} | PuLP {pulp.__version__}")
print(f"solver: CBC (bundled with PuLP)")
print(f"zone threshold in use: {ZONE_THRESHOLD_KM} km")

ok = reproduces_published(ROOT / "dataset" / "ecg_faults_dataset.csv")
print(f"\\ngenerator reproduces the committed fault dataset at seed {PUBLISHED_SEED}: {ok}")
assert ok, "the generator and the committed dataset have diverged -- stop and investigate"
'''))

A(cell(MD, """
### A note on what is real and what is simulated

**State this in the abstract, not only in Methods.**

The 23 service towns, their road distances and their travel times from the
Hohoe ECG base are **real field data** collected from the Hohoe Operations
Department. The 15 faults are **simulated** — drawn with `random.choices`
against an assumed fault-type mix and an assumed 30/70 priority split, neither
of which has a published source.

Simulated demand against a real network is a standard and acceptable study
design. Undisclosed, it is a research-integrity problem.
"""))

A(cell(MD, "## 2. Table 1 — the instance"))

A(cell(CODE, '''
P = Params()
faults = load_faults()
towns = load_towns()

travel  = faults["Travel_time_hours"].tolist()
repair  = faults["Repair_time_hours"].tolist()
zones   = faults["Zone"].tolist()
prio    = faults["Priority"].tolist()
floors  = zone_floors(faults)
weights = priority_weights(faults, P.high_priority_weight)   # 1.0 -- confound control
s       = job_times(faults, round_trip=P.round_trip)

V = dict(travel=travel, job_time=s, zones=zones, floors=floors, weights=weights,
         n_faults=len(faults), shift_hours=P.shift_hours, capacity=P.capacity)

d = describe_instance(faults)
rows = [
    ("Faults in the shift", d["n_faults"]),
    ("Distinct towns touched", d["distinct_towns"]),
    ("Near-zone faults", d["n_near"]),
    ("Far-zone faults", d["n_far"]),
    ("Crews", P.n_crews),
    ("Technicians per crew", 3),
    ("Max faults per crew (Q)", P.capacity),
    ("Shift length (H)", f"{P.shift_hours} h"),
    ("Mean one-way travel, Near", f"{d['mean_travel_near']:.4f} h"),
    ("Mean one-way travel, Far", f"{d['mean_travel_far']:.4f} h"),
    ("Total repair time", f"{d['total_repair']:.3f} h"),
    ("Total crew-time required", f"{sum(s):.3f} h"),
    ("Total crew-time available", f"{P.n_crews * P.shift_hours:.1f} h"),
    ("Crew utilisation", f"{100 * sum(s) / (P.n_crews * P.shift_hours):.1f}%"),
    ("High-priority faults", d["n_high_priority"]),
    ("...of which in Far towns", d["n_high_priority_far"]),
]
print("| Quantity | Value |")
print("|---|---|")
for k, v in rows:
    print(f"| {k} | {v} |")
'''))

A(cell(MD, """
Two features of this instance drive everything that follows.

**Capacity exactly equals demand.** 5 crews × 3 faults = 15 faults, so every
crew must take exactly three. There is no slack in the capacity dimension.

**Crew utilisation is 95.1%.** Required crew-time is 38.04 h against 40 h
available. Combined with the first point, this makes the day a tight
bin-packing problem — which is why ad-hoc dispatch usually produces a plan that
does not fit the shift at all (§5).
"""))

A(cell(MD, """
## 3. Table 2 — why the original objective could not work

The published model minimised total travel time. Under the coverage constraint
that every fault is served exactly once, that objective is a **constant**:

$$\\sum_i\\sum_j t_j x_{ij} = \\sum_j t_j \\Big(\\sum_i x_{ij}\\Big) = \\sum_j t_j$$

because $t_j$ depends only on *which fault*, never on *which crew* or *in what
order*. Every feasible assignment scores identically, so the solver was not
choosing a good plan — it was returning the first feasible point it found.

This holds whether travel is counted one-way or as a round trip, so it is a
property of the arithmetic rather than of the dispatch protocol.

The cell below demonstrates it on this instance, and shows that the
response-time objective does not collapse the same way.
"""))

A(cell(CODE, '''
cols = enumerate_columns(travel, s, zones, weights, P.capacity, P.shift_hours)
total_possible = sum(math.perm(len(faults), k) for k in range(1, P.capacity + 1))
print(f"crew workloads enumerated: {len(cols)} shift-feasible of {total_possible} possible")

# Minimise and maximise the SAME functional over the SAME feasible set.
eff = Params(alpha=1.0, beta=0.0)
lo = solve(travel, repair, zones, floors, weights, eff, sense="min", columns=cols)
hi = solve(travel, repair, zones, floors, weights, eff, sense="max", columns=cols)
lo_rc = check_solution(lo.schedule, lo.reported, status=lo.status, **V)
hi_rc = check_solution(hi.schedule, hi.reported, status=hi.status, **V)
_, spread = objective_varies([lo_rc.weighted_mean_response, hi_rc.weighted_mean_response])

print()
print("| Objective | Best feasible | Worst feasible | Spread |")
print("|---|---|---|---|")
print(f"| Total travel time (published model) | {sum(travel):.3f} h | {sum(travel):.3f} h | **0.0%** |")
print(f"| Mean response time (this paper) | {lo_rc.weighted_mean_response:.4f} h "
      f"| {hi_rc.weighted_mean_response:.4f} h | **{spread:.1f}%** |")
print()
print("A 0.0% spread means the objective cannot distinguish a good plan from a bad one.")
'''))

A(cell(MD, """
### The witness: same crew, same faults, reversed order

The clearest demonstration is a single crew's workload worked in two different
orders. The driving is identical; the waiting is not. Under the published
objective both score the same.
"""))

A(cell(CODE, '''
def arrivals(seq):
    cum, out = 0.0, []
    for j in seq:
        out.append(cum + travel[j])
        cum += s[j]
    return out, cum

# Pick the crew workload in the optimal plan with the widest spread of job sizes.
base = solve(travel, repair, zones, floors, weights, P, columns=cols)
base_rc = check_solution(base.schedule, base.reported, status=base.status, **V)
demo = max(base.schedule.values(), key=lambda q: max(s[j] for j in q) - min(s[j] for j in q))

fwd, dur = arrivals(demo)
rev, dur_r = arrivals(demo[::-1])
ids = faults["Fault_ID"].tolist()

print("| Service order | Arrival times (h) | Total customer waiting | Crew time |")
print("|---|---|---|---|")
print(f"| {' -> '.join(ids[j] for j in demo)} | "
      f"{', '.join(f'{a:.3f}' for a in fwd)} | **{sum(fwd):.3f} h** | {dur:.3f} h |")
print(f"| {' -> '.join(ids[j] for j in demo[::-1])} | "
      f"{', '.join(f'{a:.3f}' for a in rev)} | **{sum(rev):.3f} h** | {dur_r:.3f} h |")
print()
print(f"Identical crew time ({dur:.3f} h). Customer waiting differs by "
      f"{max(sum(fwd), sum(rev)) / min(sum(fwd), sum(rev)):.2f}x.")
print(f"Both score {sum(travel[j] for j in demo):.3f} h under the published objective.")
'''))

A(cell(MD, "## 4. Table 3 — the optimal dispatch plan"))

A(cell(CODE, '''
opt = base
rc = base_rc
opt_obj = P.alpha * rc.weighted_mean_response + P.beta * rc.equity_gap

print(f"status: {opt.status} | solved in {opt.solve_seconds:.2f} s "
      f"| {opt.n_variables} variables, {opt.n_constraints} constraints")
print(f"VERIFIED: every reported quantity recomputed from the schedule, agrees to 1e-6\\n")

print("| Crew | Faults in service order | Towns | Arrival times (h) | Crew time (h) |")
print("|---|---|---|---|---|")
for c, seq in sorted(opt.schedule.items()):
    print(f"| {c + 1} | {' -> '.join(ids[j] for j in seq)} "
          f"| {', '.join(faults['Town'][j] for j in seq)} "
          f"| {', '.join(f'{rc.response[j]:.3f}' for j in seq)} "
          f"| {rc.loads[c]:.3f} |")

print()
print("| Metric | Value |")
print("|---|---|")
print(f"| Mean response time | {rc.weighted_mean_response:.4f} h |")
print(f"| Worst customer wait | {rc.max_response:.4f} h |")
print(f"| Makespan (longest crew day) | {rc.makespan:.4f} h |")
print(f"| Mean response, Near zone | {rc.zone_mean['Near']:.4f} h |")
print(f"| Mean response, Far zone | {rc.zone_mean['Far']:.4f} h |")
print(f"| Excess wait, Near (above geographic floor) | {rc.zone_excess['Near']:.4f} h |")
print(f"| Excess wait, Far | {rc.zone_excess['Far']:.4f} h |")
print(f"| Equity gap | {rc.equity_gap:.4f} h |")
print(f"| Objective (alpha={P.alpha}, beta={P.beta}) | {opt_obj:.4f} |")
'''))

A(cell(MD, """
**Excess wait, not raw mean.** Far towns are further from the base *by
construction*, so equalising raw zone means could only be achieved by delaying
Near-zone customers. Equity is therefore measured as the wait *above* each
zone's mean one-way travel — the delay the dispatcher causes, net of geography
the crew cannot change.
"""))

A(cell(MD, """
## 5. Table 4 — comparison against dispatch heuristics

The original repository compared the optimum against a single random draw that
was itself infeasible. This replaces it with a suite in which **feasibility is
measured rather than assumed**, including a best-fit-decreasing policy with
1-swap repair — what a dispatcher does when a naive rule gets stuck. Without
that policy the comparison would be a straw man.
"""))

A(cell(CODE, '''
bl = B.run_all(len(faults), P, travel, s, zones, floors, weights, prio, n_random=5000)
bl.pop("_schedules")

def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p, dd = k / n, 1 + z * z / n
    c = (p + z * z / (2 * n)) / dd
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / dd
    return (max(0.0, c - h), min(1.0, c + h))

print("**Feasibility of random dispatch**\\n")
print("| Policy | Feasible draws | Rate | Wilson 95% CI |")
print("|---|---|---|---|")
for name, label in (("random_round_robin", "Random round-robin"),
                    ("random_best_order", "Random, best order within crew")):
    r = bl[name]
    lo_, hi_ = wilson(r["n_feasible"], r["n_trials"])
    print(f"| {label} | {r['n_feasible']} / {r['n_trials']} "
          f"| {100 * r['feasibility_rate']:.2f}% "
          f"| [{100 * lo_:.2f}%, {100 * hi_:.2f}%] |")

print("\\n**Quality against deterministic policies**\\n")
print("| Policy | Mean response | vs optimum | Equity gap | Objective | vs optimum |")
print("|---|---|---|---|---|---|")
print(f"| **Optimum (this paper)** | **{rc.weighted_mean_response:.4f} h** | — "
      f"| **{rc.equity_gap:.4f} h** | **{opt_obj:.4f}** | — |")
labels = {"greedy_bfd_repair": "Best-fit-decreasing + repair",
          "local_search": "...+ local search",
          "greedy_longest_job": "Longest-job-first",
          "greedy_shortest_job": "Shortest-job-first",
          "greedy_nearest": "Nearest-first",
          "greedy_priority": "Priority-first",
          "zone_clustered": "Zone-clustered crews"}
for name, label in labels.items():
    r = bl[name]
    if r is None:
        print(f"| {label} | *no feasible plan* | — | — | — | — |")
        continue
    dm = 100 * (r["weighted_mean_response"] - rc.weighted_mean_response) / rc.weighted_mean_response
    do = 100 * (r["objective"] - opt_obj) / opt_obj
    print(f"| {label} | {r['weighted_mean_response']:.4f} h | {dm:+.2f}% "
          f"| {r['equity_gap']:.4f} h | {r['objective']:.4f} | {do:+.2f}% |")
'''))

A(cell(MD, """
**Read this table carefully, and report both columns.** The repair heuristic
achieves slightly *better* raw mean response than the optimum while being an
order of magnitude less equitable. Reporting mean response alone would flatter
the heuristic; reporting the objective shows the optimum ahead. That contrast
is the efficiency–equity trade-off this paper is about, and it is the honest
way to present the comparison.

**Lead the results with feasibility, not with a percentage.** On this instance
the stronger statement is that ad-hoc dispatch usually produces a plan that does
not fit the shift at all, whereas the model produces a proven-optimal feasible
plan in under a second.
"""))

A(cell(MD, """
## 6. Table 5 — the efficiency/equity frontier

Use the **ε-constraint** form for the frontier, not the weighted sum: a weighted
sum recovers only supported (convex-hull) Pareto points, and on this instance
several different β values return the identical plan.
"""))

A(cell(CODE, '''
z_eff = lo_rc.weighted_mean_response          # pure-efficiency optimum from section 3
front = []
print("| Efficiency budget | Mean response | Penalty | Equity gap | Gap reduction | Worst wait |")
print("|---|---|---|---|---|---|")
g0 = None
for eps in (0.0, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20, 0.30):
    se = solve(travel, repair, zones, floors, weights, P, columns=cols,
               epsilon_budget=z_eff * (1 + eps))
    if se.status != "Optimal":
        continue
    re = check_solution(se.schedule, se.reported, status=se.status, **V)
    if g0 is None:
        g0 = re.equity_gap
    print(f"| +{100 * eps:.0f}% | {re.weighted_mean_response:.4f} h "
          f"| {100 * (re.weighted_mean_response - z_eff) / z_eff:+.2f}% "
          f"| {re.equity_gap:.4f} h | {100 * (1 - re.equity_gap / g0):.1f}% "
          f"| {re.max_response:.4f} h |")
    front.append({"epsilon": eps, "mean_response": re.weighted_mean_response,
                  "gap": re.equity_gap, "max_response": re.max_response})
'''))

A(cell(MD, """
**The premise holds and the remedy is cheap.** Minimising mean response alone
produces a measurable equity gap — the efficiency objective front-loads short,
near jobs, so the bias against far customers is a property of the objective
rather than an accident of this data. But a small efficiency sacrifice removes
most of it. That is the paper's central decision-support finding.
"""))

A(cell(MD, """
## 7. Table 6 — priority SLA sweep

A hard cap on how long a high-priority fault may wait. Operationally this is the
form an ECG engineer recognises: *"every high-priority fault reached within D
hours"*. Sweeping D locates the feasibility threshold.

Run at `w_High = 1`. **Four of the five high-priority faults in this instance
are in Far towns**, so weighting them more heavily moves the Far/Near ratio with
no equity mechanism doing the work. That confound is quantified below the sweep.
"""))

A(cell(CODE, '''
hi_idx = [j for j, p in enumerate(prio) if p == "High"]
print(f"high-priority faults: {[ids[j] for j in hi_idx]} "
      f"({sum(1 for j in hi_idx if zones[j] == 'Far')} of {len(hi_idx)} in Far towns)\\n")

print("| SLA target D | Feasible workloads | Mean response | Penalty | Mean high-priority arrival | Status |")
print("|---|---|---|---|---|---|")
for D in (None, 3.0, 2.5, 2.0, 1.5, 1.2, 1.0):
    Pd = Params(sla_hours=D)
    cD = enumerate_columns(travel, s, zones, weights, Pd.capacity, Pd.shift_hours,
                           sla_hours=D, sla_faults=hi_idx)
    sD = solve(travel, repair, zones, floors, weights, Pd, columns=cD, sla_faults=hi_idx)
    label = "none" if D is None else f"{D:g} h"
    if sD.status != "Optimal":
        print(f"| {label} | {len(cD)} | — | — | — | **{sD.status}** |")
        continue
    rD = check_solution(sD.schedule, sD.reported, status=sD.status, **V)
    hm = sum(rD.response[j] for j in hi_idx) / len(hi_idx)
    pen = 100 * (rD.weighted_mean_response - rc.weighted_mean_response) / rc.weighted_mean_response
    print(f"| {label} | {len(cD)} | {rD.weighted_mean_response:.4f} h | {pen:+.2f}% "
          f"| {hm:.4f} h | {sD.status} |")
'''))

A(cell(CODE, '''
print("**Priority/zone confound control**\\n")
print("| High-priority weight | Mean response | Far/Near ratio | Mean high-priority arrival |")
print("|---|---|---|---|")
for wh in (1.0, 1.5, 2.0, 3.0):
    w2 = priority_weights(faults, wh)
    c2 = enumerate_columns(travel, s, zones, w2, P.capacity, P.shift_hours)
    V2 = dict(V, weights=w2)
    s2 = solve(travel, repair, zones, floors, w2, P, columns=c2)
    r2 = check_solution(s2.schedule, s2.reported, status=s2.status, **V2)
    hm = sum(r2.response[j] for j in hi_idx) / len(hi_idx)
    print(f"| {wh} | {r2.weighted_mean_response:.4f} h "
          f"| {r2.zone_mean['Far'] / r2.zone_mean['Near']:.4f} | {hm:.4f} h |")
print()
print("The ratio moves with the weight alone. Keep w_High = 1 for every equity")
print("experiment and present priority weighting as a separate, labelled result.")
'''))

A(cell(MD, "## 8. Table 7 — parameter sensitivity"))

A(cell(CODE, '''
print("**Equity tolerance theta** (two-sided cap; theta is defined on [1, inf))\\n")
print("| theta | Mean response | Equity gap | Status |")
print("|---|---|---|---|")
for th in (2.0, 1.6, 1.4, 1.2, 1.1, 1.05, 1.0):
    st_ = solve(travel, repair, zones, floors, weights, Params(theta=th), columns=cols)
    if st_.status != "Optimal":
        print(f"| {th} | — | — | **{st_.status}** |")
        continue
    rt = check_solution(st_.schedule, st_.reported, status=st_.status, **V)
    print(f"| {th} | {rt.weighted_mean_response:.4f} h | {rt.equity_gap:.4f} h | {st_.status} |")
'''))

A(cell(CODE, '''
print("**Crew capacity Q**\\n")
print("| Q | Feasible workloads | Mean response | Equity gap | Faults per crew |")
print("|---|---|---|---|---|")
for Q in (2, 3, 4, 5):
    Pq = Params(capacity=Q)
    cq = enumerate_columns(travel, s, zones, weights, Q, Pq.shift_hours)
    sq = solve(travel, repair, zones, floors, weights, Pq, columns=cq)
    if sq.status != "Optimal":
        print(f"| {Q} | {len(cq)} | — | — | **{sq.status}** |")
        continue
    rq = check_solution(sq.schedule, sq.reported, status=sq.status, **dict(V, capacity=Q))
    loads = sorted((len(v) for v in sq.schedule.values()), reverse=True)
    print(f"| {Q} | {len(cq)} | {rq.weighted_mean_response:.4f} h "
          f"| {rq.equity_gap:.4f} h | {loads} |")
print()
print("At Q=3 capacity exactly equals demand, so every crew must take exactly three")
print("faults. Report the Q-relaxed result as sensitivity: it shows how much of the")
print("plan is fixed by arithmetic rather than chosen by the model.")
'''))

A(cell(CODE, '''
print("**Shift length H**\\n")
print("| H | Feasible workloads | Mean response | Equity gap | Makespan |")
print("|---|---|---|---|---|")
for H in (6.0, 7.0, 8.0, 9.0, 10.0):
    Ph = Params(shift_hours=H)
    ch = enumerate_columns(travel, s, zones, weights, Ph.capacity, H)
    sh = solve(travel, repair, zones, floors, weights, Ph, columns=ch)
    if sh.status != "Optimal":
        print(f"| {H:g} h | {len(ch)} | — | — | **{sh.status}** |")
        continue
    rh = check_solution(sh.schedule, sh.reported, status=sh.status, **dict(V, shift_hours=H))
    print(f"| {H:g} h | {len(ch)} | {rh.weighted_mean_response:.4f} h "
          f"| {rh.equity_gap:.4f} h | {rh.makespan:.3f} h |")
'''))

A(cell(CODE, '''
print("**Near/Far zone threshold**\\n")
print("The original code used ceil(max(distance))/2 = 19.5 km, which is a function of")
print("the farthest town in the dataset; the README stated 20 km. The two disagree on")
print("Liati, at exactly 20.0 km. The threshold is now fixed exogenously, and the")
print("decision was taken BEFORE any result was generated.\\n")
print("| Threshold | Near | Far | Mean response | Equity gap |")
print("|---|---|---|---|---|")
for thr in ZONE_THRESHOLD_SENSITIVITY:
    ft = load_faults(threshold_km=thr)
    zt = ft["Zone"].tolist()
    flt = zone_floors(ft)
    wt = priority_weights(ft, P.high_priority_weight)
    ct = enumerate_columns(travel, s, zt, wt, P.capacity, P.shift_hours)
    stt = solve(travel, repair, zt, flt, wt, P, columns=ct)
    rt = check_solution(stt.schedule, stt.reported,
                        **dict(V, zones=zt, floors=flt, weights=wt), status=stt.status)
    nn = sum(1 for x in zt if x == "Near")
    mark = " **(in use)**" if thr == ZONE_THRESHOLD_KM else ""
    print(f"| {thr:g} km{mark} | {nn} | {len(zt) - nn} "
          f"| {rt.weighted_mean_response:.4f} h | {rt.equity_gap:.4f} h |")
'''))

A(cell(MD, """
## 9. Table 8 — multi-instance study

A single instance cannot support a claim. This repeats the comparison over 15
independently drawn fault instances against the same real town network.

**Feasibility rate is the primary endpoint.** The efficiency comparison is
*conditional on the baseline being feasible at all*, and that condition fails on
most instances — so a paired test is run only on the subset where both the
optimum and the heuristic produce a feasible plan, with that subset's size
reported explicitly.
"""))

A(cell(CODE, '''
N_INST, N_RAND = 15, 2000
rows, paired = [], []
for k in range(N_INST):
    fk = generate_faults(15, seed=1000 + k)
    tk = fk["Travel_time_hours"].tolist(); rk_ = fk["Repair_time_hours"].tolist()
    zk = fk["Zone"].tolist(); flk = zone_floors(fk)
    wk = priority_weights(fk, P.high_priority_weight)
    sk = job_times(fk, round_trip=P.round_trip)
    Vk = dict(travel=tk, job_time=sk, zones=zk, floors=flk, weights=wk,
              n_faults=len(fk), shift_hours=P.shift_hours, capacity=P.capacity)
    ck = enumerate_columns(tk, sk, zk, wk, P.capacity, P.shift_hours)
    sol = solve(tk, rk_, zk, flk, wk, P, columns=ck)
    if sol.status != "Optimal":
        rows.append({"seed": 1000 + k, "status": sol.status})
        continue
    r = check_solution(sol.schedule, sol.reported, status=sol.status, **Vk)
    bk = B.run_all(len(fk), P, tk, sk, zk, flk, wk, fk["Priority"].tolist(),
                   n_random=N_RAND)
    bk.pop("_schedules")
    ls = bk["local_search"]
    rows.append({
        "seed": 1000 + k, "status": "Optimal",
        "opt_mean": r.weighted_mean_response, "opt_gap": r.equity_gap,
        "far_near": r.zone_mean["Far"] / r.zone_mean["Near"],
        "rand_rate": bk["random_round_robin"]["feasibility_rate"],
        "ls_mean": ls["weighted_mean_response"] if ls else None,
        "ls_gap": ls["equity_gap"] if ls else None,
    })
    if ls:
        paired.append((r.weighted_mean_response, ls["weighted_mean_response"],
                       r.equity_gap, ls["equity_gap"]))

ok_rows = [x for x in rows if x.get("status") == "Optimal"]
print("| Instance | Optimum mean | Optimum gap | Far/Near | Random feasibility | Heuristic mean | Heuristic gap |")
print("|---|---|---|---|---|---|---|")
for x in ok_rows:
    print(f"| {x['seed']} | {x['opt_mean']:.4f} h | {x['opt_gap']:.4f} h "
          f"| {x['far_near']:.4f} | {100 * x['rand_rate']:.2f}% "
          f"| {x['ls_mean']:.4f} h | {x['ls_gap']:.4f} h |" if x["ls_mean"]
          else f"| {x['seed']} | {x['opt_mean']:.4f} h | {x['opt_gap']:.4f} h "
               f"| {x['far_near']:.4f} | {100 * x['rand_rate']:.2f}% | *none* | — |")
'''))

A(cell(CODE, '''
print(f"**Summary over {len(ok_rows)} instances**\\n")
rr = [x["rand_rate"] for x in ok_rows]
gaps = [x["opt_gap"] for x in ok_rows]
ratios = [x["far_near"] for x in ok_rows]
tot_f = sum(round(x["rand_rate"] * N_RAND) for x in ok_rows)
lo_, hi_ = wilson(tot_f, len(ok_rows) * N_RAND)

print("| Quantity | Value |")
print("|---|---|")
print(f"| Instances solved to proven optimality | {len(ok_rows)} / {N_INST} |")
print(f"| Random-dispatch feasibility, pooled | {100 * tot_f / (len(ok_rows) * N_RAND):.2f}% "
      f"(Wilson 95% CI [{100 * lo_:.2f}%, {100 * hi_:.2f}%]) |")
print(f"| Random-dispatch feasibility, per-instance range | "
      f"{100 * min(rr):.2f}% to {100 * max(rr):.2f}% |")
print(f"| Equity gap at optimum, mean | {st.mean(gaps):.4f} h |")
print(f"| Equity gap at optimum, range | {min(gaps):.4f} to {max(gaps):.4f} h |")
print(f"| Far/Near response ratio at optimum, mean | {st.mean(ratios):.4f} |")

if len(paired) >= 6:
    from scipy.stats import wilcoxon
    dm = [100 * (b - a) / a for a, b, _, _ in paired]
    dg = [b - a for _, _, a, b in paired]
    wm, pm = wilcoxon([a for a, _, _, _ in paired], [b for _, b, _, _ in paired])
    wg, pg = wilcoxon([a for _, _, a, _ in paired], [b for _, _, _, b in paired])
    print(f"\\n**Optimum vs best heuristic, on the {len(paired)} instances where both are feasible**\\n")
    print("| Comparison | Median difference | Wilcoxon W | p |")
    print("|---|---|---|---|")
    print(f"| Mean response | {st.median(dm):+.2f}% | {wm:.1f} | {pm:.5f} |")
    print(f"| Equity gap | {st.median(dg):+.4f} h | {wg:.1f} | {pg:.5f} |")
    print()
    print("Wilcoxon signed-rank, not a t-test: these differences are not normal.")
'''))

A(cell(MD, """
## 10. Table 9 — scaling

**Crew count must scale with the workload, not just the fault count.** There are
two capacity dimensions — faults per crew ($m \\cdot Q \\ge n$) and crew-hours
($m \\cdot H \\ge$ total work). Scaling only the first makes utilisation exceed
100% and the instances become genuinely infeasible rather than merely hard.

The rule applied holds crew utilisation at the published instance's level:

$$m = \\max\\left(\\left\\lceil n/Q \\right\\rceil,\\ \\left\\lceil \\frac{\\text{total work}}{H \\cdot u} \\right\\rceil\\right), \\quad u = 0.951$$

**State this rule in the paper**, and report the utilisation column so the
reader can see the instances are comparable.
"""))

A(cell(CODE, '''
TARGET_U = 0.951
print("| n | Crews m | Utilisation | Feasible / possible workloads | Enumerate | Solve | Status | Mean response |")
print("|---|---|---|---|---|---|---|---|")
sizes = (15, 24, 30) if QUICK else (15, 24, 30, 45, 60)
for n in sizes:
    fn = generate_faults(n, seed=2000 + n)
    tn = fn["Travel_time_hours"].tolist(); rn_ = fn["Repair_time_hours"].tolist()
    zn = fn["Zone"].tolist(); fln = zone_floors(fn)
    wn = priority_weights(fn, P.high_priority_weight)
    sn_ = job_times(fn, round_trip=P.round_trip)
    work = sum(sn_)
    m = max(math.ceil(n / P.capacity), math.ceil(work / (P.shift_hours * TARGET_U)))
    Pn = Params(n_crews=m)
    import time as _t
    t0 = _t.time()
    cn = enumerate_columns(tn, sn_, zn, wn, Pn.capacity, Pn.shift_hours)
    enum_s = _t.time() - t0
    sn = solve(tn, rn_, zn, fln, wn, Pn, columns=cn, time_limit=600)
    poss = sum(math.perm(n, k) for k in range(1, Pn.capacity + 1))
    util = 100 * work / (m * Pn.shift_hours)
    mean_txt = "—"
    if sn.status == "Optimal":
        rn = check_solution(sn.schedule, sn.reported, status=sn.status,
                            travel=tn, job_time=sn_, zones=zn, floors=fln,
                            weights=wn, n_faults=n, shift_hours=Pn.shift_hours,
                            capacity=Pn.capacity)
        mean_txt = f"{rn.weighted_mean_response:.4f} h"
    print(f"| {n} | {m} | {util:.1f}% | {len(cn)} / {poss} | {enum_s:.2f} s "
          f"| {sn.solve_seconds - enum_s:.2f} s | {sn.status} | {mean_txt} |")
if QUICK:
    print("\\n(QUICK = True: n = 45 and 60 omitted. Set QUICK = False to include them;")
    print(" they take several minutes each. Their values are in result/sensitivity/scaling.json.)")
'''))

A(cell(MD, "## 11. Figures"))

A(cell(CODE, '''
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIG = ROOT / "result" / "figures"
FIG.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.size": 9, "figure.dpi": 150, "savefig.bbox": "tight"})

# Figure 1 -- crew schedule Gantt
fig, ax = plt.subplots(figsize=(7.5, 3.0))
for c, seq in sorted(opt.schedule.items()):
    cum = 0.0
    for j in seq:
        ax.barh(c, 2 * travel[j], left=cum, color="#9fb3c8", edgecolor="white", height=0.6)
        ax.barh(c, repair[j], left=cum + travel[j], color="#2f6f9f",
                edgecolor="white", height=0.6)
        ax.text(cum + travel[j] + repair[j] / 2, c, ids[j], ha="center", va="center",
                color="white", fontsize=7)
        cum += s[j]
ax.axvline(P.shift_hours, color="#b23a3a", ls="--", lw=1)
ax.text(P.shift_hours, -0.9, f" {P.shift_hours:g} h shift", color="#b23a3a", fontsize=8)
ax.set_yticks(range(len(opt.schedule)))
ax.set_yticklabels([f"Crew {c + 1}" for c in sorted(opt.schedule)])
ax.set_xlabel("Hours from start of shift")
ax.set_title("Optimal dispatch plan (light = travel, dark = repair)")
ax.invert_yaxis()
fig.savefig(FIG / "fig1_schedule.png")
plt.close(fig)

# Figure 2 -- efficiency/equity frontier
fig, ax = plt.subplots(figsize=(4.6, 3.4))
ax.plot([f["mean_response"] for f in front], [f["gap"] for f in front],
        "o-", color="#2f6f9f")
for f in front[::2]:
    ax.annotate(f"+{100 * f['epsilon']:.0f}%",
                (f["mean_response"], f["gap"]), fontsize=7,
                textcoords="offset points", xytext=(5, 4))
ax.set_xlabel("Mean response time (h)")
ax.set_ylabel("Equity gap (h)")
ax.set_title("Efficiency / equity frontier")
ax.grid(alpha=0.3)
fig.savefig(FIG / "fig2_frontier.png")
plt.close(fig)

# Figure 3 -- response time by zone
fig, ax = plt.subplots(figsize=(4.6, 3.4))
for i, z in enumerate(("Near", "Far")):
    vals = [rc.response[j] for j in rc.response if zones[j] == z]
    ax.scatter([i + 0.04 * (k - len(vals) / 2) for k in range(len(vals))], vals,
               s=22, color=["#2f6f9f", "#b23a3a"][i], label=f"{z} (n={len(vals)})")
    ax.hlines(st.mean(vals), i - 0.25, i + 0.25, color="black", lw=1.5)
ax.set_xticks([0, 1]); ax.set_xticklabels(["Near", "Far"])
ax.set_ylabel("Response time (h)")
ax.set_title("Response time by zone at the optimum\\n(bars = zone means)")
ax.legend(fontsize=7); ax.grid(alpha=0.3, axis="y")
fig.savefig(FIG / "fig3_zones.png")
plt.close(fig)

print(f"figures written to {FIG}")
for p in sorted(FIG.glob("*.png")):
    print(" ", p.name)
'''))

A(cell(MD, """
## Verification summary

Every solve in this notebook passed `check_solution`, which independently
recomputes response times, zone excess waits, the equity gap, the makespan and
crew loads from the chosen schedule and asserts agreement with the solver's own
reported values to 1e-6.

If this notebook ran to completion without raising `VerificationError`, every
number above is internally consistent with the plan it describes.

### Still required before submission

- Disclose in the **abstract** that fault instances are simulated.
- Written permission from ECG Hohoe to publish district operational data.
- Informed consent for the technician interview, and an ethics statement.
- The literature review — 20 to 30 references.
- Confirm with ECG: the 8 h shift, the 3-faults-per-crew limit, any formal
  Near/Far kilometre threshold, and any published restoration target for
  high-priority faults.
"""))

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python",
                       "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

out = pathlib.Path(__file__).resolve().parent.parent / "notebooks" / "05_manuscript_results.ipynb"
out.write_text(json.dumps(nb, indent=1))
print(f"wrote {out} ({len(cells)} cells)")
