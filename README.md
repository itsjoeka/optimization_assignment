<h1 align="center">Equitable Assignment of ECG Technician Crews to Electricity Faults Across Multi-Town Service Areas</h1>
<p align="center"><i>A simulation case study grounded in the Hohoe Operations Department, Volta Region, Ghana</i></p>

---

## Table of Contents

- [Project Overview](#project-overview)
- [Key Results](#key-results)
- [Installation and Reproduction](#installation-and-reproduction)
- [Repository Layout](#repository-layout)
- [Data](#data)
- [Mathematical Formulation](#mathematical-formulation)
- [Verification](#verification)
- [Limitations](#limitations)
- [Status](#status)
- [Acknowledgement](#acknowledgement)
- [Team](#team)
- [References](#references)

---

## Project Overview

When faults are reported across a rural electricity distribution district, a
dispatcher must decide which technician crew attends which fault, and in what
order. Two objectives pull against each other. **Efficiency** says serve the
nearest, quickest jobs first, because that restores the most customers soonest.
**Equity** says customers in distant towns should not systematically wait longer
for power than customers near the district office.

This project formulates that decision for the Electricity Company of Ghana's
Hohoe Operations Department as a mixed-integer programme, solves it exactly, and
measures the trade-off between the two objectives.

**Problem class.** Identical parallel machine scheduling, $P \,\|\, \sum_j w_j C_j$,
with crew capacity, a shift-duration limit and a spatial-equity constraint. Each
fault is a job; each crew is a machine. Crews dispatch from the Hohoe base and
return between jobs, so fault $j$ occupies $s_j = 2t_j + r_j$ of a crew's shift.

This is an **assignment** problem with a service order — there is no inter-site
travel, no travel-time matrix and no routing. The order matters only because a
customer later in a crew's shift waits longer. Routing is deliberately out of
scope and is named in [Limitations](#limitations).

**Scale.** 23 real service towns, 15 simulated faults, 5 crews of 3 technicians,
an 8-hour shift. The instance solves to proven optimality in about a third of a
second.

---

## Key Results

**Feasibility, not efficiency, is the headline.** Crew capacity exactly equals
demand (5 crews × 3 faults = 15 faults) and crew utilisation is 95.1%, which
makes a day's dispatch a tight bin-packing problem.

| Finding | Value |
|---|---|
| Random dispatch producing a shift-feasible plan | **2 of 5,000 draws** (0.04%) |
| Standard greedy rules producing any feasible plan | **0 of 4** |
| Optimal plan | proven optimal in **0.34 s** |
| Mean response time at the optimum | 2.3389 h |
| Worst customer wait | 5.1170 h |
| Equity gap (Far minus Near excess wait) | 0.0702 h |
| Makespan (longest crew day) | 7.9820 h of 8 h |

**Five crews cannot serve a typical day.** Over 15 independently drawn fault days:

| Crews | Days servable | Cumulative coverage |
|---|---|---|
| 5 (current) | 2 | 13.3% |
| 6 | 5 | 46.7% |
| 7 | 5 | 80.0% |
| 8 | 2 | 93.3% |
| 9 | 1 | 100.0% |

Required crew-time averages 47.73 h against 40 h available. **This is a
resourcing result, not a solver result** — on most days no assignment exists.

**Equity is cheap.** Minimising mean response alone produces a measurable equity
gap, but a 2% efficiency sacrifice removes most of it:

| Efficiency budget | Mean response | Equity gap | Gap reduction |
|---|---|---|---|
| +0% | 2.3002 h | 0.6763 h | — |
| **+2%** | 2.3442 h | **0.0613 h** | **91%** |
| +5% | 2.3802 h | 0.0013 h | 99.8% |

**A high-priority service guarantee is achievable at 2.5 hours.** A 2-hour target
is provably infeasible with five crews. The 2.5-hour guarantee costs 11.7% on
mean response.

**What this study does _not_ claim.** Against a well-built heuristic the median
objective difference is **0.39%**, and local search ties the optimum outright on
several instances. The value here is proven optimality in under a second, the
feasibility argument, and the quantified equity trade-off — not large efficiency
gains over a competent dispatcher.

---

## Installation and Reproduction

```bash
git clone https://github.com/itsjoeka/optimization_assignment.git
cd optimization_assignment
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

The solver is CBC, bundled with PuLP — nothing extra to install.

Run the notebooks in order from the `notebooks/` directory:

| Notebook | What it does | Runtime |
|---|---|---|
| `01_data.ipynb` | Builds both datasets, fits the travel-time model, documents data quality | seconds |
| `02_optimization_model.ipynb` | **Builds and solves the model step by step.** The reproducibility notebook | ~1 min |
| `03_diagnostics.ipynb` | Infeasibility diagnostics, for when a solve does not return optimal | seconds |
| `04_baseline_model.ipynb` | Benchmark policies and the feasibility comparison | ~2 min |
| `05_manuscript_results.ipynb` | Regenerates every number in the paper as paste-ready tables | ~5 min |

Or run the full experiment suite headless:

```bash
python3 scripts/day3_evidence.py     # baselines, priority, sensitivity, scaling
python3 scripts/multi_instance.py    # 15-instance study with significance tests
python3 scripts/scaling.py           # scaling with honest solver verdicts
python3 scripts/run_notebook.py notebooks/02_optimization_model.ipynb
```

All parameters live in `src/config.py`. Nothing is redefined locally — that is
what previously allowed the equity tolerance to drift between notebooks.

---

## Repository Layout

```
src/                      importable model code; notebooks are thin wrappers over it
  config.py               every parameter, in one place
  data.py                 loading, zone classification, derived quantities
  generate.py             synthetic fault instances (seeded, reproducible)
  speed_model.py          travel-time regression and its placebo tests
  model.py                the compact MILP -- the formal statement
  solver.py               set-partitioning encoding -- what actually solves
  baselines.py            benchmark dispatch policies
  verify.py               independent recomputation of every reported quantity

notebooks/                the reproducibility pipeline, in order
scripts/                  headless experiment runners and notebook generators
dataset/                  the two input datasets
result/                   solved plans, experiment outputs, figures
docs/                     data-quality register, audit and review material
```

---

## Data

**Real.** `dataset/ecg_towns_dataset.csv` — 23 service towns with road distance
and travel time from the Hohoe ECG base, collected from the Operations
Department. This is the project's primary asset.

**Simulated.** `dataset/ecg_faults_dataset.csv` — 15 faults drawn with
`random.choices` (seed 60) against an assumed fault-type mix and an assumed 30/70
priority split. **Neither distribution has a published source.** Simulated demand
against a real network is a standard design, but it must be disclosed in the
paper's abstract, not only in Methods.

### The travel-time model

Implied road speeds across the 23 towns span 1.0 to 47.2 km/h, which looks like
noisy data. It mostly is not. Regressing travel time on distance (22 towns;
Fodome excluded, see below) recovers a fixed overhead plus a constant cruise
speed:

$$t = 0.1595 + 0.02059\,d \qquad R^2 = 0.896,\quad \text{LOOCV } Q^2 = 0.874,\quad \text{CV MAE} = 3.7\ \text{min}$$

The intercept is **9.6 minutes** (p = 1.2 × 10⁻⁴) — the time to clear Hohoe town
and reach the trunk road — and the slope implies **48.6 km/h** cruising
(p = 2.8 × 10⁻¹¹). Dividing a *fixed* overhead by a *short* distance is what
produces an apparently slow town: Wli at 47 km/h and Gbi-Kledzo at 18 km/h are
the same vehicle on the same road model. A power-law fit reaches the same
conclusion independently ($k = 0.74$, 95% CI [0.63, 0.86], rejecting constant
speed at p = 1.3 × 10⁻⁴).

**No separate zone term is warranted.** A Near/Far step dummy looks significant
(p = 0.039), but `src/speed_model.threshold_placebo()` tests a dummy at all 29
candidate thresholds: five are significant uncorrected, only 16 km survives
Bonferroni, and at the 20 km threshold the model actually uses it is **not**
significant (p = 0.057). Reporting the best of 29 would be a specification search.

### Data quality

Every known issue is in [`docs/data_quality.md`](docs/data_quality.md) with the
decision taken. Nothing is silently patched.

**Fodome** records 0.65 km in 0.65 h — 1.0 km/h, a 6.5 sd outlier. The value is
**retained unchanged**, flagged in `src/config.SUSPECT_TOWNS` and excluded from
the regression. It is not corrected because the true value is unknown; the
recorded *time* implies 23.8 km under the fitted model, so the distance is the
more likely error. No fault in the published instance occurs at Fodome.

**Zone threshold.** The original code used `ceil(max(distance))/2` = 19.5 km, a
function of the farthest town in the dataset. The threshold is now an exogenous
20 km in `src/config.py`, with sensitivity reported over 19.5 / 20 / 25 km. This
moves Liati (exactly 20.0 km) to Near and changes every equity constant, which is
why it was decided before any result was generated.

---

## Mathematical Formulation

### Sets

| | |
|---|---|
| $J = \{1,\dots,n\}$ | faults in the shift ($n = 15$) |
| $I = \{1,\dots,m\}$ | crews ($m = 5$; three technicians moving as one unit) |
| $K = \{1,\dots,Q\}$ | service positions within a crew's shift ($Q = 3$) |
| $J^N, J^F$ | Near / Far zone partition |

### Parameters

| | |
|---|---|
| $t_j$ | one-way travel time, base to fault $j$ |
| $r_j$ | repair time at fault $j$ |
| $s_j = 2t_j + r_j$ | shift occupancy: out, repair, back |
| $H = 8$ h | shift length |
| $\bar\tau^z$ | mean one-way travel in zone $z$ — the geographic floor |
| $w_j$ | priority weight ($=1$ for all equity experiments) |
| $\theta \ge 1$ | equity tolerance |
| $\alpha,\beta$ | efficiency / equity weights, $\alpha+\beta=1$ |

### Decision variables

$y_{ijk} \in \{0,1\}$ — crew $i$ services fault $j$ at position $k$.
$R_j \ge 0$ — **response time**, hours from shift start until a crew reaches
fault $j$. $G \ge 0$ — equity gap. $C_{\max}$ — makespan.

### Objective

$$\min\; \alpha\cdot\underbrace{\frac{1}{W}\sum_{j\in J} w_j R_j}_{\text{efficiency}} \;+\; \beta\cdot\underbrace{G}_{\text{equity}}, \qquad W=\sum_j w_j$$

The return leg occupies the crew but **no customer waits on it**, so it enters
$s_j$ and the shift constraint, never the objective.

### Constraints

| | | |
|---|---|---|
| C1 | $\sum_i\sum_k y_{ijk} = 1 \;\; \forall j$ | every fault served exactly once |
| C2 | $\sum_j y_{ijk} \le 1 \;\; \forall i,k$ | one fault per position |
| C3 | $\sum_j y_{ijk} \ge \sum_j y_{ij,k+1}$ | no idle gaps |
| C4 | $\sum_j\sum_k s_j y_{ijk} \le H \;\; \forall i$ | shift limit |
| C5 | $R_j$ pinned **by equality** to its arrival time | see below |
| C6 | $G \ge \lvert E^F - E^N \rvert$, $E^z = \bar R^z - \bar\tau^z$ | two-sided gap on **excess wait** |
| C7 | $E^F \le \theta E^N$ and $E^N \le \theta E^F$ | two-sided cap, $\theta \ge 1$ |

**Three modelling decisions that are not arbitrary.**

*Equity is measured on excess wait, not raw zone means.* Far towns are further
from the base by construction, so equalising raw means could only be achieved by
delaying Near-zone customers — "levelling down". Subtracting each zone's
geographic floor measures the delay the **dispatcher** causes.

*C5 is pinned by equality.* With only a lower bound, $R_j$ reaches its true
arrival time solely because the efficiency term pushes it there. Whenever the
objective stops pushing — at $\beta = 1$, or under an ε-constraint — the solver
inflates $R_j$ and buys equity with fiction. An earlier version of this project
had exactly that defect and reported an equity gap of 0.000 against a true
0.588 h.

*C7 requires $\theta \ge 1$.* Two-sided, $E^F \le \theta E^N$ and
$E^N \le \theta E^F$ imply $E^F \le \theta^2 E^F$, so $\theta < 1$ is identically
infeasible. `src/config.py` rejects it rather than letting the model return a
misleading `Infeasible`.

### Why the objective is response time and not travel time

The original formulation minimised total travel time. Under C1 that objective is
a **constant**:

$$\sum_i\sum_j t_j x_{ij} = \sum_j t_j \Big(\sum_i x_{ij}\Big) = \sum_j t_j = 8.985\ \text{h}$$

because $t_j$ depends only on *which fault*, never on *which crew* or *in what
order*. Every feasible assignment scored identically. This holds for one-way and
round-trip travel alike, so it is a property of the arithmetic rather than of the
dispatch protocol.

The witness, on this data — one crew's workload, worked in two orders:

| Service order | Arrival times (h) | Total customer waiting | Crew time |
|---|---|---|---|
| F15 → F8 → F12 | 0.267, 1.801, 3.315 | **5.383 h** | 7.982 h |
| F12 → F8 → F15 | 0.667, 5.851, 6.965 | **13.483 h** | 7.982 h |

Identical crew time, **2.50× the customer waiting**, and both score 1.451 h under
the original objective. Measured over the whole feasible set, total travel time
has a **0.0%** spread while mean response time has **69.9%**.

### Solution method

Because $Q = 3$, the complete set of ordered crew workloads is
$15 + 15 \cdot 14 + 15 \cdot 14 \cdot 13 = 2{,}955$, of which 1,793 fit the
shift. All are enumerated and priced exactly in closed form, then a
set-partitioning MILP selects a cover. Three consequences:

1. The column set is **complete**, so the optimum is exact — not a heuristic.
2. **No big-M**, so no weak relaxation: 0.34 s against minutes for the compact
   encoding.
3. Response times are **computed**, never chosen by the solver, which makes the
   decoupled-equity defect above *structurally impossible*.

The compact MILP in `src/model.py` is the formal statement; `02_optimization_model.ipynb`
§2.9 checks the two encodings agree to 1e-6.

---

## Verification

Every solve passes `src/verify.py`, which takes the schedule the solver chose,
recomputes response times, zone excess waits, the equity gap, makespan and crew
loads **from that schedule alone** in plain Python, and asserts agreement to
1e-6. It also parses the solver status rather than assuming it.

This exists because both defects that nearly derailed this project shared one
shape: a quantity that *looked* optimised but was decoupled from the decision.
Neither was caught by reading the model; both are caught immediately by
recomputation.

Solver status is read from **CBC's own log**, not from PuLP's `LpStatus`. PuLP
reports `Optimal` whenever CBC returns a feasible solution — including when CBC
stopped on its time limit having proved nothing. On the n = 45 scaling instance
the two disagree, and only CBC is right.

---

## Limitations

State all of these in the paper.

- **Faults are simulated.** The network is real; the demand is not.
- **No inter-site routing.** Crews are modelled as returning to base between
  jobs. Field evidence indicates they often travel site-to-site, which is a
  genuine routing problem requiring a town-to-town travel matrix the project does
  not have. This is the natural next paper.
- **Static horizon.** All faults are assumed known at shift start. A technician's
  account indicates faults arrive *during* the shift, so this is best framed as
  morning dispatch planning, or as an offline bound on achievable performance.
- **Deterministic travel times.** No weather, season or time-of-day variation.
- **Single district, single day.** No multi-day rostering.
- **Faults treated as electrically independent.** No feeder-level dependency,
  where restoring one fault restores customers downstream of another.
- **Shift length, crew capacity and crew count are asserted, not sourced.**
  They need confirmation from ECG.

---

## Status

The model, experiments and verification are complete. Still outstanding before
submission:

- [ ] Written permission from ECG Hohoe to publish district operational data
- [ ] Informed consent for the technician interview, and an ethics statement
- [ ] Literature review (20–30 references)
- [ ] Manuscript draft
- [ ] Data licence distinct from the code's MIT (CC-BY-4.0 is conventional)

See [`CORRECTIONS.md`](CORRECTIONS.md) for the full register and
[`AUDIT.md`](AUDIT.md) for the review that produced it.

---

## Acknowledgement

Electricity Company of Ghana, Hohoe Operations Department, and Abdul Haliq.

> Publication of this dataset is subject to written permission from ECG, which
> has not yet been obtained. The technician interview referenced in the
> limitations requires informed consent before any quotation is published.

## Team

Jonathan Kalami · Sally Gli · Tayyiba Amartey · Dr. Ali Abubakar · Dr. Bright Owusu

## References

*To be completed.* The reference pool assembled during review — 86 candidates
across technician routing and scheduling, equity in optimisation, power
distribution outage management, and the Ghanaian context — is in
[`docs/appendix_literature_research.md`](docs/appendix_literature_research.md).

> **None of those citations has been verified against a publisher record.** Every
> one must be checked before it is cited.

## Licence

Code is MIT (see [`LICENSE`](LICENSE)). **The datasets are not yet licensed for
redistribution** pending ECG permission.
