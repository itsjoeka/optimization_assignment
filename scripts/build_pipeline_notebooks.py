"""Generate the three pipeline notebooks: 01_data, 02_optimization_model, 04_baselines.

These are the REPRODUCIBILITY notebooks -- they perform the actual run, step by
step, the way 02_optimization_model.ipynb originally did. 05_manuscript_results
is a different thing: it reports the finished values as paste-ready tables.

All three are generated rather than hand-edited so the cells stay readable in
diffs, and the generator refuses to write a notebook whose code cells do not
parse (a newline escape that does not survive a triple-quoted string silently
splits a string literal, and the only symptom is a notebook that executes to
nothing).
"""
import ast
import json
import pathlib

NB_DIR = pathlib.Path(__file__).resolve().parent.parent / "notebooks"


def md(text):
    return {"cell_type": "markdown", "metadata": {},
            "source": text.strip("\n").splitlines(keepends=True)}


def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": text.strip("\n").splitlines(keepends=True)}


def write(name, cells):
    bad = []
    for i, c in enumerate(cells):
        if c["cell_type"] != "code":
            continue
        try:
            ast.parse("".join(c["source"]))
        except SyntaxError as e:
            bad.append((i, e.lineno, e.msg))
    if bad:
        for i, ln, msg in bad:
            print(f"  {name} cell {i}: SyntaxError line {ln}: {msg}")
        raise SystemExit(f"refusing to write {name}: cells do not parse")
    nb = {"cells": cells,
          "metadata": {"kernelspec": {"display_name": "Python 3",
                                      "language": "python", "name": "python3"},
                       "language_info": {"name": "python", "version": "3.11"}},
          "nbformat": 4, "nbformat_minor": 5}
    path = NB_DIR / name
    path.write_text(json.dumps(nb, indent=1))
    print(f"wrote {path.name} ({len(cells)} cells, all code cells parse)")


BOOTSTRAP = '''
import pathlib, sys
ROOT = pathlib.Path.cwd().parent if pathlib.Path.cwd().name == "notebooks" else pathlib.Path.cwd()
sys.path.insert(0, str(ROOT))
'''

# =====================================================================
# 01 -- DATA
# =====================================================================
c01 = []
c01.append(md("""
# 1. Data Acquisition and Preprocessing

Builds both datasets from source and documents every decision taken about them.

## What is real and what is simulated

**Real field data.** The 23 service towns, their road distances from the Hohoe
ECG base, and their travel times. Collected from the Hohoe Operations Department.
This is the project's primary asset.

**Simulated.** The 15 faults. They are drawn with `random.choices` against an
assumed fault-type mix and an assumed 30/70 priority split, neither of which has
a published source.

Simulated demand against a real network is a standard and acceptable study
design. **Undisclosed, it is a research-integrity problem** — so this must be
stated in the paper's *abstract*, not only in Methods.
"""))

c01.append(code(BOOTSTRAP + '''
import numpy as np
import pandas as pd

from src.config import SUSPECT_TOWNS, ZONE_THRESHOLD_KM, ZONE_THRESHOLD_SENSITIVITY
from src.data import classify_zone, describe_instance, load_towns
from src.generate import (FAULT_TYPES, PRIORITY_WEIGHTS, PUBLISHED_SEED,
                          TYPE_WEIGHTS, generate_faults, reproduces_published)
from src.speed_model import fit, outlier_report, power_law, threshold_placebo

pd.set_option("display.width", 120)
print(f"zone threshold in use: {ZONE_THRESHOLD_KM} km")
'''))

c01.append(md("""
## 1.1 The service-town network

23 towns with field-measured distance and travel time from the base.
"""))

c01.append(code('''
towns = load_towns()
towns[["service_town", "distance_in_km", "travel_time_in_hours",
       "zone", "implied_speed_kmh"]].sort_values("distance_in_km")
'''))

c01.append(md("""
## 1.2 Zone classification — a decision taken before any result was generated

The original code set the Near/Far boundary at `ceil(max(distance))/2` = 19.5 km.
That is a **function of the farthest town in the dataset**: adding one distant
town silently reclassifies others. The README stated 20 km. The two disagree on
**Liati, at exactly 20.0 km**.

The threshold is now an exogenous constant in `src/config.py`. Changing it moves
every equity constant in the paper, which is why it was fixed first.
"""))

c01.append(code('''
rows = []
for thr in ZONE_THRESHOLD_SENSITIVITY:
    z = towns["distance_in_km"].apply(classify_zone, threshold_km=thr)
    rows.append({"threshold_km": thr,
                 "n_near": int((z == "Near").sum()),
                 "n_far": int((z == "Far").sum()),
                 "Liati": classify_zone(20.0, thr)})
print(pd.DataFrame(rows).to_string(index=False))
print(f"\\nin use: {ZONE_THRESHOLD_KM} km (src.config.ZONE_THRESHOLD_KM)")
'''))

c01.append(md("""
## 1.3 The travel-time model

The first audit flagged the implied road speeds — distance ÷ travel time —
as spanning 1.0 to 47.2 km/h and called it a data-quality problem.

**It is mostly not.** Regressing travel time on distance recovers a fixed
overhead plus a roughly constant cruise speed. Dividing a *fixed* overhead by a
*short* distance is what produces an apparently slow town.

This turns the dataset's most reviewer-visible oddity into a finding the paper
can report, rather than an assumption it has to defend.
"""))

c01.append(code('''
sf = fit(towns)
print(sf.summary())
print(f"\\n  intercept {sf.intercept_h:.4f} h = {sf.overhead_min:.1f} min"
      f"  (se {sf.intercept_se:.4f}, p = {sf.intercept_p:.2e})")
print(f"  slope     {sf.slope_h_per_km:.5f} h/km -> cruise {sf.cruise_kmh:.2f} km/h"
      f"  (p = {sf.slope_p:.2e})")
print(f"  excluded from the fit: {sf.excluded}  (see section 1.4)")
'''))

c01.append(code('''
# An independent route to the same conclusion. Constant speed would mean k = 1.
pl = power_law(towns)
print(f"power law  t = c * d^k")
print(f"  k = {pl['k']:.4f}   95% CI [{pl['ci95'][0]:.4f}, {pl['ci95'][1]:.4f}]"
      f"   R2 = {pl['r2']:.4f}")
print(f"  H0 (k = 1, constant speed): t = {pl['t_vs_constant_speed']:.3f},"
      f" p = {pl['p_vs_constant_speed']:.2e}")
print("\\n  k < 1 means effective speed RISES with distance -- which is exactly")
print("  what a fixed per-trip overhead produces.")
'''))

c01.append(md("""
### Is there a genuine Near/Far break in travel time?

A Near/Far step dummy added to the linear model looks significant (p ≈ 0.039).
Before that goes anywhere near the paper it has to survive a placebo test:
**if a dummy at many thresholds is significant, the one we happened to pick is
not a finding.**
"""))

c01.append(code('''
pb = threshold_placebo(towns)
at20 = next(r for r in pb["tests"] if r["threshold_km"] == 20)
print(f"candidate thresholds tested      : {pb['n_tests']}")
print(f"significant at p < 0.05          : {pb['n_significant_uncorrected']}")
print(f"best threshold                   : {pb['best']['threshold_km']:.0f} km"
      f" (p = {pb['best']['p']:.4f})")
print(f"Bonferroni alpha                 : {pb['bonferroni_alpha']:.5f}")
print(f"surviving correction             : {pb['surviving_bonferroni']}")
print(f"\\nAt the {ZONE_THRESHOLD_KM:.0f} km threshold the optimisation model actually uses:")
print(f"  F = {at20['F']:.2f}, p = {at20['p']:.4f}"
      f"  -> {'significant' if at20['p'] < 0.05 else 'NOT significant'}")
print("\\nConclusion: no separate zone term is warranted. The step dummy is a")
print("competing parameterisation of the same fixed overhead, the best-fitting")
print("threshold (16 km) is not the one the model uses, and reporting it would")
print("be a specification search over 29 candidates.")
'''))

c01.append(md("""
## 1.4 Data quality — documented, never silently patched

A reviewer who downloads the CSV, finds an anomaly, and sees no mention of it
will assume the worst. Everything known is in `docs/data_quality.md`; the
machine-checkable part is in `src/config.SUSPECT_TOWNS`.
"""))

c01.append(code('''
for o in outlier_report(towns, sf):
    print(f"{o['town']}")
    print(f"  recorded                     : {o['recorded_km']} km in "
          f"{o['recorded_hours']} h = {o['implied_speed_kmh']:.2f} km/h")
    print(f"  model predicts for that distance: {o['model_predicts_hours'] * 60:.1f} min")
    print(f"  distance implied by that TIME   : {o['distance_implied_by_time_km']:.1f} km")
    print(f"  residual                        : {o['residual_sd']:.1f} sd")
    print(f"  decision                        : {o['note']}")
print("\\nThe value is RETAINED unchanged and excluded from the fit. It is not")
print("corrected because the true value is unknown -- that needs the original")
print("measurement source. No fault in the published instance occurs here.")
'''))

c01.append(md("""
## 1.5 Fault simulation

Reproduces `dataset/ecg_faults_dataset.csv` exactly at seed 60. The assertion
below is what stops this module and the committed dataset from silently
diverging.
"""))

c01.append(code('''
print("ASSUMED fault-type mix (no published source -- state as an assumption):")
for (name, repair), wgt in zip(FAULT_TYPES.items(), TYPE_WEIGHTS):
    print(f"  {wgt:>5.0%}  {name:<32} repair {repair} h")
print(f"\\nASSUMED priority split: {PRIORITY_WEIGHTS[0]:.0%} High / {PRIORITY_WEIGHTS[1]:.0%} Normal")
print("\\nObtaining ECG's historical fault log would replace both with measured")
print("frequencies and materially strengthen the paper.")

ok = reproduces_published(ROOT / "dataset" / "ecg_faults_dataset.csv")
assert ok, "generator and committed dataset have diverged -- stop and investigate"
print(f"\\ngenerator reproduces the committed dataset at seed {PUBLISHED_SEED}: {ok}")
'''))

c01.append(code('''
faults = generate_faults(15, seed=PUBLISHED_SEED)
d = describe_instance(faults)
print("| Quantity | Value |")
print("|---|---|")
for k, v in [("Faults", d["n_faults"]), ("Distinct towns", d["distinct_towns"]),
             ("Near-zone faults", d["n_near"]), ("Far-zone faults", d["n_far"]),
             ("Mean one-way travel, Near", f"{d['mean_travel_near']:.4f} h"),
             ("Mean one-way travel, Far", f"{d['mean_travel_far']:.4f} h"),
             ("Total repair time", f"{d['total_repair']:.3f} h"),
             ("High-priority faults", d["n_high_priority"]),
             ("...of which in Far towns", d["n_high_priority_far"])]:
    print(f"| {k} | {v} |")
faults
'''))

c01.append(md("""
> **Note for the equity analysis.** Four of the five high-priority faults are in
> Far towns. Weighting priority therefore moves the Far/Near ratio with no equity
> mechanism doing any work, so every equity experiment runs at `w_High = 1`.
"""))

c01.append(md("""
## 1.6 Write the datasets

These two lines were **commented out** in the original notebook, so running it
did not regenerate the committed CSVs and a reviewer could not verify their
provenance.
"""))

c01.append(code('''
towns.drop(columns=["implied_speed_kmh", "data_quality_flag"]).to_csv(
    ROOT / "dataset" / "ecg_towns_dataset.csv", index=False)
faults.to_csv(ROOT / "dataset" / "ecg_faults_dataset.csv", index=False)
print("written:")
print("  dataset/ecg_towns_dataset.csv")
print("  dataset/ecg_faults_dataset.csv")
'''))

write("01_data.ipynb", c01)


# =====================================================================
# 02 -- THE MODEL
# =====================================================================
c02 = []
c02.append(md("""
# 2. The Technician Assignment Model

**This is the reproducibility notebook.** It builds the model from its sets and
parameters through to a solved, verified dispatch plan — the run that produces
the paper's headline numbers.

`05_manuscript_results.ipynb` is a different thing: it reports finished values as
paste-ready tables. This notebook is where the model is actually constructed.

---

## What this model is

**Class:** identical parallel machine scheduling, $P \\,\\|\\, \\sum_j w_j C_j$, with
crew capacity, a shift-duration limit and a spatial-equity constraint.

Each fault is a job. Each crew is a machine. A crew dispatches from the Hohoe
base, repairs, and returns before its next job, so job $j$ occupies
$s_j = 2t_j + r_j$ of a crew's shift.

This is an **assignment** problem with a service order. There is no inter-site
travel, no travel matrix, no subtour elimination and no routing. The order
matters only because a customer later in a crew's shift waits longer — that is
scheduling, not routing.

## What changed from the original model, and why it had to

The published model minimised **total travel time**. Under the coverage
constraint that every fault is served exactly once, that objective is a
**constant** — proved in §2.3 below, on this data. Every feasible assignment
scored identically, so the solver was not choosing a good plan; it was returning
the first feasible point it found.

The objective is now **response time**: hours from shift start until a crew
reaches each customer. That depends on which crew takes the fault and on how many
jobs precede it, so no such collapse exists.
"""))

c02.append(code(BOOTSTRAP + '''
import math
import time

import pandas as pd
import pulp

from src.config import Params
from src.data import (job_times, load_faults, priority_weights, zone_floors)
from src.model import build_and_solve
from src.solver import Column, enumerate_columns, solve
from src.verify import VerificationError, check_solution, objective_varies

print(f"PuLP {pulp.__version__} | solver: CBC (bundled)")
'''))

c02.append(md("## 2.1 Sets and parameters"))

c02.append(code('''
P = Params()
faults = load_faults()

J = list(range(len(faults)))                      # faults
I = list(range(P.n_crews))                        # crews
K = list(range(P.capacity))                       # service positions in a shift

travel = faults["Travel_time_hours"].tolist()     # t_j, base -> fault, one way
repair = faults["Repair_time_hours"].tolist()     # r_j, on site
zones = faults["Zone"].tolist()                   # z_j
ids = faults["Fault_ID"].tolist()

print(f"J  faults    : {len(J)}")
print(f"I  crews     : {len(I)}  (3 technicians each, moving as one unit)")
print(f"K  positions : {len(K)}  (max faults per crew per shift, Q)")
print(f"H  shift     : {P.shift_hours} h")
print(f"theta        : {P.theta}   (equity tolerance, defined on [1, inf))")
print(f"alpha, beta  : {P.alpha}, {P.beta}   (efficiency / equity weights)")
'''))

c02.append(code('''
# Job occupancy. The crew drives out, repairs, and drives back to base before
# its next job, so s_j = 2*t_j + r_j.
#
# The RETURN leg occupies the crew but no customer waits on it, so it enters the
# shift constraint and NEVER the objective. Getting that wrong would charge
# customers for the crew's drive home.
s = job_times(faults, round_trip=P.round_trip)

print("| Fault | Town | Zone | t_j (h) | r_j (h) | s_j = 2t+r |")
print("|---|---|---|---|---|---|")
for j in J:
    print(f"| {ids[j]} | {faults['Town'][j]} | {zones[j]} | {travel[j]:.3f} "
          f"| {repair[j]:.2f} | {s[j]:.3f} |")
print(f"\\ntotal crew-time required : {sum(s):.3f} h")
print(f"total crew-time available: {P.n_crews * P.shift_hours:.1f} h")
print(f"utilisation              : {100 * sum(s) / (P.n_crews * P.shift_hours):.1f}%")
'''))

c02.append(md("""
> Two features of this instance drive everything downstream.
>
> **Capacity exactly equals demand** — 5 crews × 3 faults = 15 faults, so every
> crew must take exactly three.
>
> **Utilisation is 95.1%.** Together these make the day a tight bin-packing
> problem, which is why ad-hoc dispatch usually produces a plan that does not fit
> the shift at all (notebook 04).
"""))

c02.append(code('''
# Zone floors: each zone's mean ONE-WAY travel -- the geographic floor a crew
# cannot beat. Equity is measured as wait ABOVE this, because Far towns are
# further by construction and equalising raw means could only be achieved by
# delaying Near-zone customers.
floors = zone_floors(faults)
weights = priority_weights(faults, P.high_priority_weight)   # 1.0: confound control

for z, v in sorted(floors.items()):
    members = [j for j in J if zones[j] == z]
    print(f"{z:>5}: {len(members)} faults, mean one-way travel {v:.4f} h")
print(f"\\npriority weights all {P.high_priority_weight} -- four of the five High-priority")
print("faults are in Far towns, so any higher weight would move the Far/Near")
print("ratio with no equity mechanism doing the work.")
'''))

c02.append(md("""
## 2.2 Decision variables

$y_{ijk} = 1$ if crew $i$ services fault $j$ at position $k$ of its shift.

$R_j \\ge 0$ is the **response time** of fault $j$: hours from shift start until a
crew arrives. $G \\ge 0$ is the inter-zone equity gap, $C_{\\max}$ the makespan.
"""))

c02.append(code('''
print(f"y_ijk : {len(I)} x {len(J)} x {len(K)} = {len(I)*len(J)*len(K)} binaries")
print(f"R_j   : {len(J)} continuous (response time)")
print("G, Cmax, Rmax : 3 continuous")
print("\\nThe full formulation is in src/model.py. It is the statement a referee")
print("expects to see; section 2.5 explains why a different ENCODING is used to")
print("solve it, and section 2.7 checks the two agree.")
'''))

c02.append(md("""
## 2.3 Why the original objective could not work

Under coverage, $\\sum_i\\sum_j t_j x_{ij} = \\sum_j t_j\\left(\\sum_i x_{ij}\\right)
= \\sum_j t_j$, because $t_j$ depends only on *which fault*, never on *which crew*
or *in what order*.

This holds whether travel is counted one-way or as a round trip, so it is a
property of the arithmetic rather than of the dispatch protocol. The cell below
demonstrates it, and the one after shows what the response-time objective does
on the same plans.
"""))

c02.append(code('''
cols = enumerate_columns(travel, s, zones, weights, P.capacity, P.shift_hours)
total_possible = sum(math.perm(len(J), k) for k in range(1, P.capacity + 1))
print(f"crew workloads: {len(cols)} shift-feasible of {total_possible} possible\\n")

eff = Params(alpha=1.0, beta=0.0)
lo = solve(travel, repair, zones, floors, weights, eff, sense="min", columns=cols)
hi = solve(travel, repair, zones, floors, weights, eff, sense="max", columns=cols)
lo_mean = lo.reported["weighted_mean_response"]
hi_mean = hi.reported["weighted_mean_response"]
_, spread = objective_varies([lo_mean, hi_mean])

print("| Objective | Best feasible plan | Worst feasible plan | Spread |")
print("|---|---|---|---|")
print(f"| Total travel time (original) | {sum(travel):.3f} h | {sum(travel):.3f} h | **0.0%** |")
print(f"| Mean response time (this model) | {lo_mean:.4f} h | {hi_mean:.4f} h | **{spread:.1f}%** |")
print("\\nA 0.0% spread means the objective cannot tell a good plan from a bad one.")
'''))

c02.append(code('''
# The clearest witness: one crew's workload, worked in two orders.
def arrivals(seq):
    cum, out = 0.0, []
    for j in seq:
        out.append(cum + travel[j])
        cum += s[j]
    return out, cum

demo = [14, 7, 11]                      # F15, F8, F12
fwd, dur = arrivals(demo)
rev, dur_r = arrivals(demo[::-1])
print("| Service order | Arrival times (h) | Total customer waiting | Crew time |")
print("|---|---|---|---|")
print(f"| {' -> '.join(ids[j] for j in demo)} | {', '.join(f'{a:.3f}' for a in fwd)} "
      f"| **{sum(fwd):.3f} h** | {dur:.3f} h |")
print(f"| {' -> '.join(ids[j] for j in demo[::-1])} | {', '.join(f'{a:.3f}' for a in rev)} "
      f"| **{sum(rev):.3f} h** | {dur_r:.3f} h |")
print(f"\\nIdentical crew time ({dur:.3f} h). Customer waiting differs by "
      f"{max(sum(fwd), sum(rev)) / min(sum(fwd), sum(rev)):.2f}x.")
print(f"Both score {sum(travel[j] for j in demo):.3f} h under the original objective.")
'''))

c02.append(md("""
## 2.4 Constraints

| | Constraint | Meaning |
|---|---|---|
| C1 | $\\sum_i\\sum_k y_{ijk} = 1\\ \\forall j$ | every fault served exactly once |
| C2 | $\\sum_j y_{ijk} \\le 1\\ \\forall i,k$ | one fault per position slot |
| C3 | $\\sum_j y_{ijk} \\ge \\sum_j y_{ij,k+1}$ | no idle gaps in a crew's shift |
| C4 | $\\sum_j\\sum_k s_j y_{ijk} \\le H\\ \\forall i$ | shift-duration limit |
| C5 | $R_j$ pinned by **equality** to its arrival time | see below |
| C6 | $G \\ge \\lvert E^F - E^N\\rvert$ | two-sided equity gap on **excess wait** |
| C7 | $E^F \\le \\theta E^N$ and $E^N \\le \\theta E^F$ | two-sided equity cap, $\\theta \\ge 1$ |

**C5 is pinned by equality, not minimality.** With only a lower bound, $R_j$ is
driven to the true arrival time *solely* by the efficiency term; whenever the
objective stops pushing it down (β = 1, or an ε-constraint) the solver inflates
$R_j$ and buys equity with fiction. An earlier version of this project had
exactly that defect and reported a gap of 0.000 against a true 0.588 h.

**C6 is two-sided** for the same reason: a one-sided constraint lets the solver
manufacture parity by *delaying Near-zone* customers.

**C7 requires θ ≥ 1.** Two-sided, $E^F \\le \\theta E^N$ and $E^N \\le \\theta E^F$
imply $E^F \\le \\theta^2 E^F$, so θ < 1 is identically infeasible. `src/config.py`
rejects it rather than letting the model report a misleading `Infeasible`.
"""))

c02.append(md("""
## 2.5 Solution method: set partitioning over enumerated crew workloads

The constraints above describe the model. Solving it as a compact MILP with
big-M arrival constraints works but is slow — minutes at n = 15.

Because $Q = 3$, the complete set of ordered crew workloads is
$15 + 15\\cdot14 + 15\\cdot14\\cdot13 = 2{,}955$, small enough to enumerate
exhaustively and price **exactly** in closed form. Three consequences:

1. The column set is **complete**, so the set-partitioning optimum is the exact
   optimum — not a heuristic, not a relaxation.
2. There is **no big-M**, so no weak relaxation and no slow solve.
3. Response times are **computed**, never chosen by the solver, which makes the
   decoupled-equity defect described above *structurally impossible*.

Point 3 is the important one and belongs in the paper.
"""))

c02.append(code('''
t0 = time.time()
cols = enumerate_columns(travel, s, zones, weights, P.capacity, P.shift_hours)
enum_s = time.time() - t0
print(f"enumerated {len(cols)} shift-feasible workloads of {total_possible} "
      f"possible in {enum_s:.3f} s")
print(f"  ({100 * len(cols) / total_possible:.1f}% of orderings fit an {P.shift_hours:g} h shift)\\n")

c = cols[0]
print("each column carries its exact cost, computed in plain Python:")
print(f"  faults   {[ids[j] for j in c.faults]}")
print(f"  arrivals {[round(a, 3) for a in c.arrivals]}")
print(f"  duration {c.duration:.3f} h")
print(f"  cost     {c.cost:.4f}  (sum of w_j * arrival_j)")
'''))

c02.append(md("## 2.6 Solve"))

c02.append(code('''
sol = solve(travel, repair, zones, floors, weights, P, columns=cols)
meta = sol.columns

print(f"status          : {sol.status}")
print(f"search completed: {meta['search_completed']}   "
      f"(read from CBC's log, not inferred from PuLP's status)")
print(f"objective       : {sol.objective:.6f}")
print(f"solve time      : {meta['solve_seconds']:.3f} s")
print(f"model size      : {sol.n_variables} variables, {sol.n_constraints} constraints")
'''))

c02.append(md("""
## 2.7 Verification — the step that must never be skipped

Both defects that nearly sank this project shared one shape: a quantity that
*looked* optimised but was decoupled from the decision. Neither was caught by
reading the model. Both are caught instantly by taking the schedule the solver
chose, recomputing every reported number from it in plain Python, and asserting
agreement.

If the cell below raises, **no number in this notebook can be used**.
"""))

c02.append(code('''
rc = check_solution(
    sol.schedule, sol.reported,
    travel=travel, job_time=s, zones=zones, floors=floors, weights=weights,
    n_faults=len(J), status=sol.status,
    shift_hours=P.shift_hours, capacity=P.capacity)
print("VERIFIED at 1e-6: coverage, solver status, shift and capacity limits, and")
print("every reported quantity recomputed independently from the schedule.")
'''))

c02.append(md("## 2.8 The dispatch plan"))

c02.append(code('''
print("| Crew | Faults in service order | Towns | Arrival times (h) | Crew time (h) |")
print("|---|---|---|---|---|")
for crew, seq in sorted(sol.schedule.items()):
    print(f"| {crew + 1} | {' -> '.join(ids[j] for j in seq)} "
          f"| {', '.join(faults['Town'][j] for j in seq)} "
          f"| {', '.join(f'{rc.response[j]:.3f}' for j in seq)} "
          f"| {rc.loads[crew]:.3f} |")

obj = P.alpha * rc.weighted_mean_response + P.beta * rc.equity_gap
print()
print("| Metric | Value |")
print("|---|---|")
for k, v in [("Mean response time", f"{rc.weighted_mean_response:.4f} h"),
             ("Worst customer wait", f"{rc.max_response:.4f} h"),
             ("Makespan (longest crew day)", f"{rc.makespan:.4f} h"),
             ("Mean response, Near", f"{rc.zone_mean['Near']:.4f} h"),
             ("Mean response, Far", f"{rc.zone_mean['Far']:.4f} h"),
             ("Excess wait, Near", f"{rc.zone_excess['Near']:.4f} h"),
             ("Excess wait, Far", f"{rc.zone_excess['Far']:.4f} h"),
             ("Equity gap", f"{rc.equity_gap:.4f} h"),
             (f"Objective (alpha={P.alpha}, beta={P.beta})", f"{obj:.4f}")]:
    print(f"| {k} | {v} |")
'''))

c02.append(md("""
## 2.9 Cross-check: does the compact MILP agree?

The set-partitioning encoding is only legitimate if it solves the *same model*.
The compact big-M formulation in `src/model.py` is checked against it here.

It is run at **reduced size**, because the big-M encoding takes minutes at
n = 15 while set partitioning takes a fraction of a second — which is itself the
argument for the encoding, and worth reporting in the paper.
"""))

c02.append(code('''
N_SMALL = 7
sub = faults.head(N_SMALL)
t_s = sub["Travel_time_hours"].tolist()
r_s = sub["Repair_time_hours"].tolist()
z_s = sub["Zone"].tolist()
f_s = zone_floors(sub)
w_s = priority_weights(sub, P.high_priority_weight)
P_s = Params(n_crews=3)

sp = solve(t_s, r_s, z_s, f_s, w_s, P_s)
t0 = time.time()
mi = build_and_solve(t_s, r_s, z_s, f_s, w_s, P_s, time_limit=600)
milp_s = time.time() - t0

print(f"n = {N_SMALL}, m = {P_s.n_crews}\\n")
print(f"  set partitioning : {sp.status:<10} objective {sp.objective:.6f}"
      f"  in {sp.columns['solve_seconds']:.3f} s")
print(f"  compact MILP     : {mi.status:<10} objective {mi.objective:.6f}"
      f"  in {milp_s:.3f} s")
gap = abs(sp.objective - mi.objective)
print(f"\\n  difference: {gap:.2e}")
assert gap < 1e-6, "the two encodings disagree -- stop and investigate"
print("  AGREE to 1e-6: the two encodings describe the same model.")
'''))

c02.append(md("## 2.10 Save the plan"))

c02.append(code('''
rows = []
for crew, seq in sorted(sol.schedule.items()):
    for pos, j in enumerate(seq, start=1):
        rows.append({"Crew": crew + 1, "Position": pos, "Fault_ID": ids[j],
                     "Town": faults["Town"][j], "Zone": zones[j],
                     "Fault_Type": faults["Fault_type"][j],
                     "Priority": faults["Priority"][j],
                     "Travel_hrs": travel[j], "Repair_hrs": repair[j],
                     "Job_occupancy_hrs": round(s[j], 3),
                     "Response_hrs": round(rc.response[j], 3)})
out = pd.DataFrame(rows)
out.to_csv(ROOT / "result" / "optimization_results.csv", index=False)
print(f"written: result/optimization_results.csv ({len(out)} rows)")
out
'''))

write("02_optimization_model.ipynb", c02)


# =====================================================================
# 04 -- BASELINES
# =====================================================================
c04 = []
c04.append(md("""
# 4. Benchmark Policies

What the optimum is compared against.

## What was wrong with the original comparison

The original notebook drew **one** random assignment at seed 61 and compared
against it. Three problems, any one of which invalidates the comparison:

- **n = 1.** A single draw has no sampling distribution and no statistical content.
- **It was infeasible.** The notebook's own output reported one crew working
  11.667 h against an 8 h shift. Comparing a feasible optimum against an
  *infeasible* alternative is a win by construction, on constraint satisfaction
  rather than on objective value.
- **Wrong counterfactual.** Round-robin over a shuffle is a straw man.

## What replaces it

Feasibility is **measured, not assumed**, and reported as a rate with a Wilson
interval. The policy set includes a best-fit-decreasing heuristic with 1-swap
repair — what a dispatcher actually does when a naive rule gets stuck — so the
optimum has to beat a bar a competent human could reach.
"""))

c04.append(code(BOOTSTRAP + '''
import math

import pandas as pd

from src import baselines as B
from src.config import Params
from src.data import job_times, load_faults, priority_weights, zone_floors
from src.solver import enumerate_columns, solve
from src.verify import check_solution

P = Params()
faults = load_faults()
travel = faults["Travel_time_hours"].tolist()
repair = faults["Repair_time_hours"].tolist()
zones = faults["Zone"].tolist()
prio = faults["Priority"].tolist()
floors = zone_floors(faults)
weights = priority_weights(faults, P.high_priority_weight)
s = job_times(faults, round_trip=P.round_trip)
n = len(faults)

cols = enumerate_columns(travel, s, zones, weights, P.capacity, P.shift_hours)
opt = solve(travel, repair, zones, floors, weights, P, columns=cols)
rc = check_solution(opt.schedule, opt.reported, travel=travel, job_time=s,
                    zones=zones, floors=floors, weights=weights, n_faults=n,
                    status=opt.status, shift_hours=P.shift_hours,
                    capacity=P.capacity)
opt_obj = P.alpha * rc.weighted_mean_response + P.beta * rc.equity_gap
print(f"optimum: mean response {rc.weighted_mean_response:.4f} h | "
      f"gap {rc.equity_gap:.4f} h | objective {opt_obj:.4f}")
'''))

c04.append(md("""
## 4.1 Why feasibility is the headline

Capacity exactly equals demand (5 crews × 3 = 15 faults) and utilisation is
95.1%, which makes this a tight bin-packing problem. Most ad-hoc plans do not
fit the shift at all.
"""))

c04.append(code('''
def wilson(k, N, z=1.96):
    if N == 0:
        return (0.0, 0.0)
    p, d = k / N, 1 + z * z / N
    c = (p + z * z / (2 * N)) / d
    h = z * math.sqrt(p * (1 - p) / N + z * z / (4 * N * N)) / d
    return (max(0.0, c - h), min(1.0, c + h))

bl = B.run_all(n, P, travel, s, zones, floors, weights, prio, n_random=5000)
schedules = bl.pop("_schedules")

print("| Random policy | Feasible draws | Rate | Wilson 95% CI | Mean of feasible |")
print("|---|---|---|---|---|")
for key, label in (("random_round_robin", "Round-robin over a shuffle"),
                   ("random_best_order", "Random, best order within crew")):
    r = bl[key]
    lo, hi = wilson(r["n_feasible"], r["n_trials"])
    mean = (f"{r['mean_of_feasible']:.4f} h" if r["n_feasible"] else "—")
    print(f"| {label} | {r['n_feasible']} / {r['n_trials']} "
          f"| {100 * r['feasibility_rate']:.2f}% "
          f"| [{100 * lo:.2f}%, {100 * hi:.2f}%] | {mean} |")
'''))

c04.append(md("""
## 4.2 Deterministic policies

Note what shortest-job-first does here. It is the right rule for *mean response*
and the wrong rule for *packing*: it places the small jobs while every crew is
empty and then cannot fit the large ones. Longest-job-first packs better but
still fails on this instance. Only best-fit-decreasing **with repair** succeeds.

Reporting "every heuristic fails" without including a repair step would be a
straw man, which is why it is here.
"""))

c04.append(code('''
labels = {"greedy_bfd_repair": "Best-fit-decreasing + 1-swap repair",
          "local_search": "...then relocate/swap local search",
          "greedy_longest_job": "Longest-job-first",
          "greedy_shortest_job": "Shortest-job-first",
          "greedy_nearest": "Nearest-first",
          "greedy_priority": "Priority-first",
          "zone_clustered": "Zone-clustered crews"}

print("| Policy | Mean response | vs optimum | Equity gap | Objective | vs optimum |")
print("|---|---|---|---|---|---|")
print(f"| **Optimum** | **{rc.weighted_mean_response:.4f} h** | — "
      f"| **{rc.equity_gap:.4f} h** | **{opt_obj:.4f}** | — |")
for key, label in labels.items():
    r = bl[key]
    if r is None:
        print(f"| {label} | *no feasible plan* | — | — | — | — |")
        continue
    dm = 100 * (r["weighted_mean_response"] - rc.weighted_mean_response) / rc.weighted_mean_response
    do = 100 * (r["objective"] - opt_obj) / opt_obj
    print(f"| {label} | {r['weighted_mean_response']:.4f} h | {dm:+.2f}% "
          f"| {r['equity_gap']:.4f} h | {r['objective']:.4f} | {do:+.2f}% |")
'''))

c04.append(md("""
> **Report both columns, and read them carefully.**
>
> The repair heuristic achieves slightly *better* raw mean response than the
> optimum while being an order of magnitude less equitable. Reporting mean
> response alone would flatter the heuristic; reporting the objective shows the
> optimum ahead.
>
> That contrast **is** the efficiency–equity trade-off this paper is about, and
> it is the honest way to present the comparison. The paper should not claim
> large efficiency gains over a well-built heuristic — on repeated instances the
> median objective difference is under half a percent.
"""))

c04.append(md("## 4.3 Save"))

c04.append(code('''
rows = []
for key, label in labels.items():
    r = bl[key]
    rows.append({"policy": label, "feasible": r is not None,
                 "mean_response_h": r["weighted_mean_response"] if r else None,
                 "equity_gap_h": r["equity_gap"] if r else None,
                 "objective": r["objective"] if r else None})
for key, label in (("random_round_robin", "Round-robin over a shuffle"),
                   ("random_best_order", "Random, best order within crew")):
    r = bl[key]
    rows.append({"policy": label, "feasible": r["n_feasible"] > 0,
                 "feasibility_rate": r["feasibility_rate"],
                 "mean_response_h": r["mean_of_feasible"],
                 "best_of_n_h": r["best_of_n"]})
df = pd.DataFrame(rows)
df.to_csv(ROOT / "result" / "baseline_comparison.csv", index=False)
print("written: result/baseline_comparison.csv")
df
'''))

write("04_baseline_model.ipynb", c04)
