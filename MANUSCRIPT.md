<!--
DRAFT STATUS — read before editing or submitting.

This is a complete manuscript draft, assembled from the project's original
materials (title, problem statement, mathematical notation) and the corrected
model, verified experiments, and figures produced during the September–October
2026 review (see CORRECTIONS.md and AUDIT.md for the full record of what changed
and why).

What this draft is NOT yet:
  - The References section is a placeholder. No citation anywhere in this
    document should be trusted until the literature search (next step) is done
    and each entry is verified against a publisher record.
  - Author affiliations, the corresponding author, and the target venue's
    formatting requirements (reference style, word limit, submission template)
    are not yet applied. Pick the venue before copy-editing to its house style.
  - Ethics approval / ECG permission / interview consent are not yet in hand.
    Do not submit until docs/data_quality.md and CORRECTIONS.md item M10 are
    resolved.

Every number in this draft was pulled directly from result/*.json and the
executed notebooks on 10 October 2026, not retyped from memory. If any
notebook or experiment is re-run, re-check this file against the new JSON
before relying on it again.
-->

# Equitable Assignment of Electricity Distribution Technician Crews to Reported Faults: A Simulation Case Study Grounded in the Hohoe Operations Department

**Authors:** Jonathan Kalami, Sally Gli, Tayyiba Amartey, Ali Abubakar, Bright Owusu
**Affiliation:** *[to be completed]*
**Corresponding author:** *[to be completed]*

---

## Abstract

Rural electricity distribution utilities in sub-Saharan Africa dispatch small
numbers of repair crews across wide, unevenly accessible service areas with
little formal decision support. We study this problem for the Electricity
Company of Ghana's (ECG) Hohoe Operations Department, which serves 23 towns in
the Volta Region from a single base, using five crews of three technicians each
within an eight-hour shift. **Fault instances in this study are simulated**
against the real, field-measured road network; the 23 service towns and their
travel times are primary data collected from the Operations Department, while
the 15 daily faults used in the base instance are generated synthetically, as
no historical fault log was available at the time of writing.

We formulate the daily dispatch decision as an identical-parallel-machine
scheduling problem with crew capacity, a shift-duration limit, and an explicit
spatial-equity constraint on customer response time — the time between shift
start and a crew's arrival at a fault. We show analytically and empirically that
the natural first formulation, minimizing total travel time, is degenerate: under
a coverage constraint requiring every fault to be served exactly once, total
travel time is invariant across all feasible assignments, so such a model
optimizes nothing. Minimizing weighted mean response time avoids this collapse
and is solved to proven optimality via a set-partitioning reformulation over the
complete set of shift-feasible crew workloads (2,955 candidate workloads at the
published scale, 1,793 of them feasible), which solves in well under one second
and is cross-validated against a compact mixed-integer formulation.

On the base instance, crew capacity (5 crews × 3 faults = 15) and shift
utilization (95.1%) are simultaneously binding, so the instance is a tight
bin-packing problem: only 0.04% of 5,000 random dispatch draws, and none of five
deterministic greedy rules we tested, produce a shift-feasible plan, while the
optimization model returns a proven-optimal, verified plan in 0.25 seconds. An
efficiency-only objective produces a measurable equity gap between Near- and
Far-zone customers (0.676 h of excess wait); an epsilon-constraint sweep shows
that a 2% efficiency sacrifice removes 91% of this gap. A multi-instance study
over 15 independently drawn fault days shows the current five-crew establishment
is shift-feasible on only 2 of 15 days (13.3%, Wilson 95% CI [3.7%, 37.9%]); the
minimum crew count needed ranges from 5 to 9 (median 7), giving operations
management a direct staffing target. Against a well-tuned local-search
heuristic, the optimum's efficiency advantage is modest (median 0.39% on the
combined objective) and not the paper's central claim; the central claims are
feasibility, proven optimality at operational speed, and a quantified,
inexpensive equity correction.

**Keywords:** technician dispatch; parallel machine scheduling; equity in
optimization; electricity distribution; rural utility operations; Ghana.

---

## 1. Introduction

### 1.1 Motivation

Electricity distribution utilities in low- and middle-income countries
routinely operate with far fewer repair crews than their service territory and
fault volume would ideally warrant. The Hohoe Operations Department of the
Electricity Company of Ghana (ECG) is representative of this setting: it serves
23 towns spread across the Volta Region's hill country from a single operations
base, using five crews of three technicians who travel out to a fault site,
complete the repair, and return to base before the next assignment. On a given
day, the dispatcher — currently a person making an ad-hoc decision — must decide
which crew attends which reported fault, and in what order within that crew's
shift.

Two considerations compete in this decision. An **efficiency**-minded
dispatcher prioritizes short, nearby jobs, since this clears the most faults per
crew-hour and restores power to the most customers soonest. An **equity**-minded
dispatcher recognizes that efficiency-first dispatch systematically defers
faults in distant towns: because dispatch happens anew each day, a fault in a
far-zone town is never inherently urgent relative to a near-zone fault of the
same type, so a purely efficiency-driven rule will tend to serve it later, every
day, for the entire time the utility operates this way. This produces a
structural, not merely occasional, disparity in restoration time between
customers living near and far from the operations base — precisely the kind of
geographic inequity that rural electrification and distribution-reliability
research has identified as a concern in its own right, independent of aggregate
efficiency (see Section 2).

This paper asks three questions. First, can the daily dispatch decision be
formulated as a tractable optimization problem that a utility with modest
computational resources (an ordinary laptop, open-source solvers) can run
operationally? Second, does solving it exactly change anything relative to the
heuristics a human dispatcher might already be using? Third, and centrally, **how
much does equity cost**, in terms of the efficiency a utility must sacrifice to
guarantee it — and is that price actually small enough to be worth paying?

### 1.2 Contributions

1. A mixed-integer formulation of the daily technician-to-fault assignment
   decision for a single-base, multi-town electricity distribution service area,
   with an explicit, two-sided equity constraint defined on *excess wait* —
   response time in excess of each zone's unavoidable geographic travel floor —
   rather than on raw response time, which we show is necessary to avoid a
   "levelling-down" failure mode in which equity is achieved by delaying
   near-zone customers rather than by genuinely redistributing crew effort.

2. A demonstration, both algebraic and numerical, that the natural total-travel-
   time objective for this problem class is degenerate under a one-crew-per-fault
   coverage constraint: it is provably constant over the entire feasible region
   and therefore cannot be optimized at all. We show this is a general risk for
   any objective that is additively separable in the fault index alone, and we
   verify that our replacement objective, weighted mean response time, is not
   subject to it (spread of 69.9% between the best and worst feasible plans, vs.
   0.0% for total travel time, on the same feasible set).

3. An exact solution method — enumeration of the complete set of shift-feasible
   crew workloads followed by set partitioning — that solves the base instance
   (n = 15, five crews) to proven optimality in a fraction of a second, which we
   validate against an equivalent compact big-M formulation (objective values
   agree to within 2.22 × 10⁻¹⁶), and which scales to 60 faults with mostly
   proven-optimal solutions within a 600-second budget.

4. An independent numerical verification layer that recomputes every reported
   quantity (response times, zone-level excess wait, the equity gap, makespan,
   crew loads) directly from a candidate solution's schedule, rather than trusting
   solver-reported values. This caught two defects during development — an
   earlier, degenerate travel-time objective, and, in a later alternative
   formulation we rejected, an equity constraint whose reported value diverged
   from its true value by two orders of magnitude when the efficiency term
   stopped actively driving it — and we present it as a methodological safeguard
   that should accompany any multi-objective MILP whose fairness metric is not
   directly, tightly bounded by the objective being minimized.

5. A feasibility-aware benchmarking exercise showing that, on this instance,
   conventional dispatch heuristics (random assignment, four deterministic greedy
   rules) overwhelmingly fail to produce a plan that fits within the available
   shift at all; only a repair-augmented packing heuristic and local search
   succeed, and even then the exact optimum is not substantially more efficient
   (median 0.39% on the combined objective across 14 comparable instances) than
   the strongest heuristic — a result we report candidly because it bears on
   what a utility should actually expect to gain from adopting optimization.

6. A multi-instance resourcing analysis: across 15 independently generated fault
   days, the current five-crew establishment is shift-feasible on only 13.3% of
   days; the model identifies the minimum crew count required per day (median 7,
   maximum 9), which we present as a directly actionable staffing recommendation.

---

## 2. Related Work *(to be completed)*

*This section requires a literature search, which is the next step in this
project after the present draft. The structure below indicates the four
literatures the paper needs to engage, each with a one-sentence placeholder for
what must be said once real, verified citations are available. No source should
be inserted here without checking it against the publisher's own record.*

**2.1 Technician and workforce scheduling / dispatch.** [Placeholder: situate
this problem within the technician routing and scheduling problem (TRSP) and
workforce-scheduling literatures; state precisely why this instance, with crews
returning to a single base between every job, is a parallel-machine scheduling
problem rather than a vehicle-routing problem, and cite the standard references
for $P \,\|\, \sum w_jC_j$.]

**2.2 Equity and fairness in optimization and facility location/service
allocation.** [Placeholder: situate the excess-wait equity measure and the
two-sided epsilon-constraint/weighted-sum treatment relative to the equity-in-
routing, equity-in-facility-location, and fair-division literatures; identify
the standard measures (e.g., Gini-type dispersion, minimax, egalitarian
objectives) this paper's $G$ relates to, and justify the choice against them.]

**2.3 Electricity distribution outage management and reliability.** [Placeholder:
situate this paper relative to crew-dispatch-for-restoration literature and
standard reliability indices (SAIDI, SAIFI, CAIDI); state whether and how
response time as modeled here connects to a reliability-index framing.]

**2.4 Ghanaian and sub-Saharan African electricity-sector context.** [Placeholder:
cite ECG's own published operational/reliability statistics if available, and
broader literature on rural electrification and service quality disparities in
comparable settings, to establish the applied motivation independently of this
paper's own data.]

A candidate pool of unverified references compiled during project review is
retained in `docs/appendix_literature_research.md` for the authors' own use in
the next step; **none of it has been checked against a publisher record**, and
at least one entry's characterization is already known to be inaccurate (see
that file's internal notes). It must not be cited from directly.

---

## 3. Problem Description and Data

### 3.1 Operational context

The Hohoe Operations Department dispatches **five crews**, each of **three
technicians who move and work together as a single unit**, from one operations
base in Hohoe. Each crew works a single **eight-hour shift** per day and can be
assigned **at most three faults** in that shift (a capacity limit reflecting
available time and equipment, stated by the operating team; not yet independently
confirmed against ECG's own operating standard — see Section 8). A crew travels
from the base to a fault, performs the repair, and **returns to base** before
traveling to its next assigned fault; no inter-site travel between faults is
modeled (see Section 8 for the routing extension this implies as future work).

### 3.2 The service-town network (primary data)

Table 1 summarizes the 23 service towns for which road distance and travel time
from the Hohoe base were collected by the Operations Department. This is the
paper's primary empirical asset: real, field-measured travel data for a rural
Ghanaian distribution network, which to our knowledge is not otherwise publicly
available for a district of this kind.

**Table 1.** Service-town network summary (n = 23 towns).

| Quantity | Value |
|---|---|
| Towns | 23 |
| Distance range | 0.65–38.4 km |
| Travel-time range | 0.05–1.017 h |
| Near-zone towns (≤ 20 km) | 15 |
| Far-zone towns (> 20 km) | 8 |

Fitting travel time as a linear function of road distance over the 22 towns with
no documented data-quality concern (Section 3.4 explains the one exclusion)
gives:

$$t = 0.1595 + 0.02059\,d \qquad (R^2 = 0.896,\ \text{LOOCV } Q^2 = 0.874,\ \text{LOOCV MAE} = 3.72\ \text{min})$$

The fitted intercept, 9.6 minutes (standard error 2.0 minutes, $p = 1.2\times
10^{-4}$), is interpretable as a fixed per-trip overhead — plausibly the time to
clear Hohoe town itself and reach the trunk road — and the fitted slope implies
a cruising speed of 48.6 km/h ($p = 2.8\times10^{-11}$). An independent power-law
fit, $t = c\,d^k$, gives $k = 0.741$ (95% CI [0.627, 0.856]), rejecting the
constant-speed hypothesis $k=1$ at $p = 1.3\times10^{-4}$ and corroborating the
fixed-overhead interpretation: because a fixed overhead is a larger share of
total time for a short trip, dividing a short trip's total time by its distance
produces an apparently very slow implied speed even though the underlying road
and vehicle are the same as for a longer trip. This finding matters because the
raw implied speeds across these 23 towns range from 1.0 to 47.2 km/h, which in
isolation looks like measurement error; the regression shows that it is
substantially explained by a single global fixed-overhead-plus-cruise-speed
model.

We additionally tested whether an explicit Near/Far zone indicator (see Section
3.3) explains any travel-time variation beyond road distance. A step dummy at
the 20 km threshold used in this paper is **not** statistically significant
once added to the distance regression ($F(1,19) = 4.11$, $p = 0.057$). A dummy
at the single best-fitting threshold among 29 candidates tested (16 km) is
significant ($p = 0.0007$) but does not survive a Bonferroni correction for the
29 comparisons ($\alpha = 0.0017$; only the 16 km threshold itself survives,
which is not the threshold used operationally). We therefore do not include a
separate zone term in the travel-time model and treat the apparent "zone effect"
observed before this check as a specification-search artifact rather than a
genuine finding; see `src/speed_model.py: threshold_placebo()` for the full test.

### 3.3 Zone classification

Faults are classified **Near** (service-town road distance $\le 20$ km from the
Hohoe base) or **Far** ($> 20$ km). This 20 km threshold is fixed exogenously and
was decided before any experimental result in this paper was generated, to avoid
the alternative of a data-dependent threshold (e.g., half the maximum observed
distance), which would silently reclassify towns whenever the dataset's extremes
changed. Table 2 reports the sensitivity of the base instance's equity-relevant
quantities to this choice; one town (Liati, at exactly 20.0 km) reclassifies from
Far to Near between the 19.5 km and 20 km thresholds.

**Table 2.** Sensitivity of the equity-relevant instance description to the
Near/Far threshold.

| Threshold (km) | Near faults | Far faults | Mean response (h) | Equity gap (h) |
|---|---|---|---|---|
| 19.5 | 8 | 7 | 2.3367 | 0.0059 |
| **20.0 (used)** | **9** | **6** | **2.3389** | **0.0702** |
| 25.0 | 11 | 4 | 2.3323 | 0.2470 |

### 3.4 Data-quality note: Fodome

One town's record, Fodome (0.65 km, 0.65 h — an implied speed of 1.0 km/h),
deviates from the fitted travel-time model by 6.5 standard deviations and is a
near-certain transcription error (the recorded travel time implies a distance of
23.8 km under the fitted model, suggesting the recorded distance may be missing
a digit). The value is **retained unchanged** in the published dataset and
**excluded** from the travel-time regression in Section 3.2, rather than
silently corrected, because the true value is not known without access to the
original field measurement. No fault in the base instance used in this study
occurs at Fodome, so this does not affect any reported result; it is disclosed
here because silent, undocumented data correction is a more serious problem for
reproducibility than a flagged, unresolved anomaly.

### 3.5 Fault instances (simulated)

**The 15 daily faults used as the base instance in this study are simulated, not
observed.** They were generated by sampling, with a fixed random seed, a service
town (from the 23 real towns, weighted uniformly), a fault type, and a priority
level for each of 15 faults reported in a single day. Fault-type repair times
(Table 3) and the assumed fault-type and priority-level frequency distributions
were supplied by the project team from general knowledge of ECG field operations
and **do not have a published or independently verified source**; obtaining an
actual historical fault log from the Hohoe district would allow these
distributions to be replaced with measured frequencies, which we identify as the
single highest-value data improvement available for a follow-up study.

**Table 3.** Fault types and assumed repair times.

| Fault type | Repair time (h) | Assumed frequency |
|---|---|---|
| Transformer installation | 4.00 | 15% |
| Transformer maintenance | 0.75 | 25% |
| Cable joining and termination | 0.33 | 20% |
| Network line extension | 2.00 | 15% |
| Pole replacement | 1.00 | 10% |
| Vegetation control | 4.00 | 15% |

Priority is assigned High with probability 0.30 and Normal with probability
0.70 (also unsourced; see above). The base instance (15 faults, seed 60)
contains 9 Near-zone and 6 Far-zone faults, spans 12 distinct towns, and
includes 5 High-priority faults, **4 of which fall in Far-zone towns**. This
imbalance is a property of the specific random draw rather than of the
underlying geography or priority process, and it materially affects any
analysis that weights response time by priority (Section 6.4 controls for it
explicitly).

Using simulated demand against a real underlying service network is a standard
and defensible research design when historical demand data is unavailable; it
becomes a problem only if undisclosed. We disclose it here, in the abstract, and
restate it in the limitations (Section 8).

---

## 4. Mathematical Formulation

### 4.1 Problem class

We formulate the daily dispatch decision as an instance of **identical parallel
machine scheduling with a weighted sum-of-completion-times objective**,
$P \,\|\, \sum_j w_j C_j$ in the standard three-field notation, augmented with
a capacity limit per machine and an explicit spatial-equity constraint. Each
fault is a job; each crew is a machine; "completion time" is the response time
at which a crew reaches the fault, not the time at which the crew finishes the
repair and returns to base. Because every crew returns to the single operations
base between any two assigned jobs, there is no routing component — no
inter-fault travel, no travel-time matrix between service towns is required —
and the only combinatorial freedom within a crew's assignment is the **order**
in which it works its assigned faults.

### 4.2 Sets and parameters

| Symbol | Meaning |
|---|---|
| $J = \{1,\dots,n\}$ | faults reported in the shift ($n = 15$ in the base instance) |
| $I = \{1,\dots,m\}$ | crews ($m = 5$) |
| $K = \{1,\dots,Q\}$ | service positions available within a crew's shift ($Q = 3$) |
| $J^N, J^F$ | the Near- and Far-zone fault subsets |
| $t_j$ | one-way travel time from the base to fault $j$'s town |
| $r_j$ | repair time at fault $j$ |
| $s_j = 2t_j + r_j$ | total shift occupancy of fault $j$: travel out, repair, travel back |
| $H$ | shift length (8 h) |
| $\bar\tau^N, \bar\tau^F$ | mean one-way travel time within each zone — the zone's unavoidable geographic floor |
| $w_j$ | priority weight for fault $j$ ($w_j = 1$ for all faults in every equity-relevant experiment in this paper; see Section 6.4) |
| $\theta \ge 1$ | equity tolerance parameter |
| $\alpha, \beta \ge 0,\ \alpha+\beta=1$ | efficiency and equity objective weights |

### 4.3 Decision variables

$y_{ijk} \in \{0,1\}$: 1 if crew $i$ services fault $j$ at position $k$ of its
shift. $R_j \ge 0$: **response time** of fault $j$ — hours elapsed from shift
start until a crew arrives. $G \ge 0$: the inter-zone equity gap. $C_{\max}$:
the makespan (longest crew shift).

### 4.4 Why total travel time cannot be the objective

A natural first objective is to minimize total crew travel time,
$\sum_i\sum_j t_j x_{ij}$, where $x_{ij} = \sum_k y_{ijk}$ indicates whether
crew $i$ is assigned fault $j$ at all. Under the coverage requirement that every
fault be served by exactly one crew,

$$\sum_i x_{ij} = 1 \quad \forall j \in J, \tag{C1}$$

this objective reduces to

$$\sum_{i}\sum_{j} t_j x_{ij} \;=\; \sum_{j} t_j\left(\sum_i x_{ij}\right) \;=\; \sum_{j} t_j,$$

a constant, independent of the assignment, because $t_j$ depends only on *which*
fault is served, never on *which crew* serves it or *in what order*. On the base
instance this constant equals 8.985 h for every one of the 1,793 shift-feasible
assignments we enumerate in Section 5.2; an optimization solver given this
objective therefore does no meaningful search and returns an arbitrary feasible
point. We verified this numerically: minimizing and maximizing total travel
time over the complete feasible set both return exactly 8.985 h — a spread of
0.0% — confirming that the objective cannot distinguish a good assignment from
a bad one.

This is not specific to travel time: **any objective that is additively
separable in the fault index alone** collapses identically under (C1), for the
same reason. We therefore require an objective sensitive to *order within a
crew's shift*, since order is the only remaining source of variation once (C1)
holds.

### 4.5 The response-time objective

We define **response time** $R_j$ as the time elapsed from shift start until the
crew assigned to fault $j$ *arrives* at it — not when the repair is finished.
If crew $i$ serves faults in the order $(j_1, j_2, \ldots, j_k)$, then

$$R_{j_p} = t_{j_1} + \sum_{q=1}^{p-1}\left(r_{j_q} + 2t_{j_q}\right) \quad (\text{for } p \ge 2),\qquad R_{j_1} = t_{j_1}.$$

Response time depends on *both* the assignment and the *order* within a crew's
shift, because a fault served later waits for every job ahead of it to be fully
completed and the crew to return to base and depart again. This breaks the
degeneracy of Section 4.4: no additive decomposition over faults alone exists,
because each fault's contribution to total response time depends on which other
faults share its crew and in what sequence.

As a concrete illustration on the base instance, the single crew workload
$\{$F15, F8, F12$\}$ has identical total shift occupancy (7.982 h) regardless of
service order, but total customer waiting differs by a factor of 2.50 between
the two possible full orderings (5.383 h vs. 13.483 h), while both orderings
contribute identically (1.451 h) to the degenerate total-travel-time objective
of Section 4.4. Measured over the complete feasible set, minimizing vs.
maximizing weighted mean response time gives 2.300 h vs. 3.908 h — a spread of
69.9%, confirming the objective is non-degenerate.

The efficiency component of the objective is the weighted mean response time,
$\frac{1}{W}\sum_{j} w_j R_j$ where $W = \sum_j w_j$.

### 4.6 Equity treatment

Minimizing mean response time alone is known to bias dispatch toward short,
nearby jobs (a Smith's-rule-type effect), which we confirm empirically produces
a measurable gap between Near- and Far-zone mean response (Section 6.3). Because
Far-zone towns are, by construction, further from the base, naively equalizing
*raw* mean response time between zones could be achieved simply by delaying
Near-zone customers — a "levelling-down" outcome that improves no one and
actively harms some customers to produce the appearance of fairness. We instead
define equity on **excess wait**, the response time in excess of each zone's
unavoidable geographic floor:

$$E^z = \bar R^z - \bar\tau^z, \qquad z \in \{N, F\},$$

where $\bar R^z$ is the mean response time of faults in zone $z$ under a given
assignment and $\bar\tau^z$ is that zone's mean one-way travel time (a property
of the town network alone, not of any assignment). $E^z$ measures the delay
attributable to *dispatch decisions*, net of geography the crew cannot change.

The equity gap and its constraint are both defined **two-sided**:

$$G \;\ge\; E^F - E^N, \qquad G \;\ge\; E^N - E^F, \tag{C-gap}$$
$$E^F \;\le\; \theta\, E^N, \qquad E^N \;\le\; \theta\, E^F. \tag{C-cap}$$

A one-sided constraint (e.g., only $E^F \le \theta E^N$) would permit the solver
to satisfy the equity requirement by *inflating* $E^N$ rather than by
compressing $E^F$ — the same failure mode in a different guise. The two-sided
cap in (C-cap) is well-posed only for $\theta \ge 1$: combining both inequalities
gives $E^F \le \theta^2 E^F$, which is satisfiable only if $\theta \ge 1$ (or
$E^F = E^N = 0$). We enforce this restriction in the model implementation
(`src/config.py`) rather than allowing a $\theta < 1$ specification to silently
return a misleading "infeasible" result for a reason unrelated to the data.

### 4.7 Full formulation

$$\min \;\; \alpha \cdot \frac{1}{W}\sum_{j\in J} w_j R_j \;+\; \beta \cdot G \tag{Obj}$$

subject to

$$\sum_{i\in I}\sum_{k\in K} y_{ijk} = 1 \qquad \forall j \in J \tag{C1 — coverage}$$
$$\sum_{j\in J} y_{ijk} \le 1 \qquad \forall i\in I,\ k\in K \tag{C2 — one fault per slot}$$
$$\sum_{j\in J} y_{ijk} \ge \sum_{j\in J} y_{i,j,k+1} \qquad \forall i\in I,\ k < Q \tag{C3 — no idle gaps}$$
$$\sum_{j\in J}\sum_{k\in K} s_j\, y_{ijk} \le H \qquad \forall i\in I \tag{C4 — shift limit}$$
$$R_j \text{ pinned by equality to the crew/position choice } y_{ijk} \tag{C5 — response time}$$
$$\text{(C-gap), (C-cap)} \tag{C6, C7 — equity}$$

Constraint (C5) deserves emphasis: it must pin $R_j$ **by equality**, not merely
bound it from below. An earlier variant of this model (and an alternative
arc-based formulation considered during development) bounded $R_j$ only from
below by the true arrival time via a big-$M$ constraint; because nothing then
*upper*-bounded $R_j$ except the objective's own pressure to minimize it, a
solver asked to minimize the equity gap alone (or under an $\varepsilon$-
constraint budget on efficiency) could satisfy the equity constraint by
inflating $R_j$ for some faults without that inflation being reflected in any
actual routing decision — producing a model that reports a near-zero equity gap
on paper while its actual schedule has a materially larger one. We verified this
defect numerically in that alternative formulation (reported gap 0.000 vs. a
true recomputed gap of 0.588 h at $\beta = 1$) before rejecting it in favor of
the exact-pricing method of Section 5.2, under which $R_j$ is *computed*, not
chosen by the solver, making this failure mode structurally impossible.

---

## 5. Solution Method

### 5.1 Compact formulation

The constraints of Section 4.7 can be encoded directly as a mixed-integer
program using big-$M$ constraints to pin $R_j$ to the arrival time implied by
the chosen $y_{ijk}$ (see `src/model.py`). This is a correct and complete
statement of the model and is useful as the formulation a reader expects to see,
but it is computationally expensive relative to the alternative below: the
25-variable-per-crew-slot big-$M$ encoding solves the base instance in several
minutes with a general-purpose solver, and a 7-fault, 3-crew validation instance
(Section 5.3) takes 2.04 seconds against 0.036 seconds for the set-partitioning
encoding of Section 5.2 at the same scale.

### 5.2 Set-partitioning reformulation

Because the crew capacity $Q = 3$ is small, the complete set of **ordered crew
workloads** of length 1, 2, or 3 can be exhaustively enumerated:

$$15 + 15\cdot14 + 15\cdot14\cdot13 = 2{,}955$$

ordered workloads at $n = 15$. Each workload's exact cost — every fault's
response time, the workload's total shift occupancy, and its contribution to
each zone's excess wait — is computed directly in closed form at enumeration
time, with no approximation. Workloads whose total shift occupancy exceeds $H$
are discarded; **1,793 of the 2,955 possible workloads (60.7%) are shift-
feasible** at $H=8$h. A set-partitioning master problem then selects at most $m$
of these workloads such that every fault is covered exactly once, minimizing the
same objective (Obj):

$$\min\; \alpha\cdot\frac{1}{W}\sum_\omega c_\omega \lambda_\omega + \beta\, G \qquad \text{s.t.}\qquad \sum_{\omega:\, j\in\omega} \lambda_\omega = 1\ \ \forall j,\quad \sum_\omega \lambda_\omega \le m,\quad \lambda_\omega \in \{0,1\}.$$

Because the enumerated column set is **complete** — every shift-feasible crew
workload is a candidate column — the optimum of this set-partitioning problem
is the **exact** optimum of the original model, not a heuristic or a relaxation.
This formulation requires no big-$M$ constant, no subtour-elimination logic
(there are no subtours to eliminate, since there is no routing), and — most
importantly for Section 4.7's concern — response times are **computed once per
column, in plain arithmetic**, never chosen as a solver decision variable; the
equity-gap-decoupling failure mode described in Section 4.7 is therefore
structurally impossible in this encoding.

### 5.3 Validation against the compact formulation

To confirm the set-partitioning reformulation solves the same model as the
compact formulation of Section 5.1, we solved a reduced instance (the first 7
faults of the base instance, $m=3$ crews) under both encodings. Both returned
objective value **1.335500**, agreeing to within $2.22\times10^{-16}$ (floating-
point equality), with the set-partitioning solve completing in 0.036 s and the
compact big-$M$ solve in 2.042 s.

### 5.4 Verification protocol

Every reported solution in this paper is passed through an independent
verification step (`src/verify.py`) that:

1. confirms the solver's reported status is a genuine optimum (see Section 5.5
   on a subtlety here) and that the schedule covers every fault exactly once;
2. confirms every crew's shift occupancy and fault count respect $H$ and $Q$;
3. **recomputes every reported quantity — each fault's response time, both
   zones' mean response and excess wait, the equity gap, the makespan, and each
   crew's load — directly from the schedule, in plain arithmetic, independent of
   any solver-internal value**, and asserts agreement to within $10^{-6}$.

Step 3 is the step that caught both defects described in Sections 4.4 and 4.7.
In each case the model *appeared* to solve successfully and reported plausible-
looking output; only recomputation from the realized schedule revealed that the
reported quantity was decoupled from the actual decision. We present this
verification step as a general methodological recommendation for any
multi-objective optimization model whose secondary (here, equity) objective is
not tightly and directly bounded by the primary objective being minimized.

### 5.5 A note on solver status

We additionally found that the solver interface used (PuLP, with the CBC
solver) reports a status of "Optimal" whenever the underlying solver returns any
feasible incumbent, **including when the solver was stopped by a wall-clock
time limit before completing its search** — that is, "Optimal" from this
interface does not reliably distinguish a proven optimum from an unproven best-
found solution. We address this by parsing the underlying solver's own log for
its explicit "stopped on time limit" / "search completed" language and its
reported optimality gap, and we report results at larger instance sizes
(Section 6.6) using this corrected status rather than the interface's own label.

---

## 6. Computational Experiments

All experiments were run with PuLP 3.3.2 and the bundled CBC solver on a
general-purpose virtual machine; no specialized hardware or commercial solver
was used. Code and raw results are available in the accompanying repository
(see Data and Code Availability).

### 6.1 Base-instance solution

**Table 4.** The optimal dispatch plan, base instance ($n=15$, $m=5$,
$\alpha=0.7$, $\beta=0.3$, $\theta=1.6$).

| Crew | Service order | Towns | Arrival times (h) | Shift occupancy (h) |
|---|---|---|---|---|
| 1 | F3 → F1 → F9 | Golokwati, Afadzo South, Santrokofi | 0.500, 2.767, 5.117 | 7.450 |
| 2 | F6 → F11 → F4 | Afadzo South, Ve-Dator, Agome yo | 1.017, 2.964, 4.831 | 7.348 |
| 3 | F7 → F2 → F10 | Akpafu, Liati, Wli | 0.417, 1.714, 3.497 | 7.980 |
| 4 | F13 → F14 → F5 | Ve-Kobenu, Agome yo, Logba | 0.583, 2.013, 4.280 | 7.280 |
| 5 | F15 → F8 → F12 | Gbi-Kledzo, Agome yo, Ve-Gbodome | 0.267, 1.801, 3.315 | 7.982 |

This plan is illustrated in **Figure 1** (crew schedule Gantt chart). Summary
statistics:

| Metric | Value |
|---|---|
| Status | Proven optimal (verified to $10^{-6}$) |
| Solve time | 0.25 s |
| Weighted mean response time | 2.3389 h |
| Worst-case customer wait | 5.1170 h |
| Makespan | 7.9820 h (of 8 h available) |
| Mean response, Near zone | 2.1897 h |
| Mean response, Far zone | 2.5627 h |
| Excess wait, Near / Far | 1.7118 h / 1.7820 h |
| Equity gap $G$ | 0.0702 h |
| Objective value ($\alpha=0.7,\beta=0.3$) | 1.6583 |

Two structural features of this instance are worth noting before interpreting
later results. Crew capacity and the number of faults coincide exactly
($5 \times 3 = 15$), so every crew must take exactly three faults — there is no
slack in how many faults any crew receives. Total required shift occupancy is
38.04 h against 40 h available (5 crews $\times$ 8 h), a **95.1% utilization**
rate. Together, these make the base instance a tight bin-packing problem, which
is the direct explanation for the baseline-comparison results in Section 6.2.

### 6.2 Comparison against dispatch heuristics

We compared the optimal plan against seven alternative dispatch policies: two
random policies (5,000 draws each — uniform random assignment, and the same
random assignment with each crew's jobs re-ordered optimally), and five
deterministic greedy rules (shortest-job-first, longest-job-first, nearest-
town-first, priority-first, and zone-clustered assignment), plus a local-search
procedure initialized from the best feasible greedy solution found. Feasibility
— whether a policy's output even respects the 8-hour shift and 3-fault capacity
limits — is measured rather than assumed, since the project's original baseline
comparison (a single random draw) was itself infeasible.

**Table 5.** Feasibility and quality of dispatch policies, base instance.

| Policy | Feasible | Mean response (h) | Equity gap (h) | Objective |
|---|---|---|---|---|
| **Optimum** | — | **2.3389** | **0.0702** | **1.6583** |
| Random assignment (5,000 draws) | 2/5,000 (0.04%) | 2.9902* | 0.5438* | 2.1385* (best) |
| Random, re-ordered per crew | 2/5,000 (0.04%) | 2.2997* | 1.5606* | 2.0250* (best) |
| Shortest-job-first | 0/1 | — | — | — |
| Longest-job-first | 0/1 | — | — | — |
| Nearest-town-first | 0/1 | — | — | — |
| Priority-first | 0/1 | — | — | — |
| Zone-clustered crews | 0/1 | — | — | — |
| Best-fit-decreasing + repair | 1/1 | 2.2823 | 1.7044 | 2.1090 |
| ...+ local search | 1/1 | 2.2867 | 1.2293 | 1.9695 |

*Statistics over feasible draws only; "Objective" column for random policies
reports the best objective achieved among feasible draws, not a mean.

Four of five simple deterministic greedy rules **never produce a feasible
plan** on this instance: each either front-loads small jobs and strands larger
ones with insufficient remaining capacity, or produces an unbalanced crew split
that violates the shift limit. Only a bin-packing-style heuristic explicitly
designed to repair infeasible partial assignments succeeds, and random
assignment succeeds on only 0.04% of draws. This supports our central empirical
claim: **on this instance, the practical value of optimization is substantially
about guaranteeing feasibility, not primarily about efficiency gains over an
already-feasible heuristic plan.**

Where a feasible heuristic plan does exist (best-fit-decreasing with repair,
and its local-search refinement), it achieves a slightly *better* raw mean
response time than the exact optimum (2.282 h and 2.287 h vs. 2.339 h) while
being substantially less equitable (equity gap 1.70 h and 1.23 h vs. 0.07 h) —
an order of magnitude worse on the fairness dimension this paper cares about.
Reporting only mean response time would make the heuristic look superior;
reporting the combined objective shows the optimum ahead by 27% and 19%
respectively. This is not an accident: it is precisely the efficiency–equity
trade-off this paper studies, and it is the correct way to read this
comparison — not as a demonstration that optimization dramatically outperforms
heuristics on efficiency, but as a demonstration that equity is not a free
by-product of a good efficiency heuristic and must be modeled explicitly.

### 6.3 The efficiency–equity frontier

We trace the trade-off between weighted mean response time and the equity gap
$G$ using an $\varepsilon$-constraint sweep (minimizing $G$ subject to a budget
on mean response, expressed as a percentage above the pure-efficiency optimum of
2.300 h), rather than the weighted-sum form of (Obj), because the weighted-sum
form recovers only *supported* (convex-hull) Pareto points — several distinct
$\beta$ values in our sweep returned the identical plan — while the
$\varepsilon$-constraint form traces the frontier completely. **Figure 2** plots
this frontier; Table 6 reports it numerically.

**Table 6.** Efficiency–equity frontier ($\varepsilon$-constraint sweep).

| Efficiency budget (vs. pure-efficiency optimum) | Mean response (h) | Equity gap (h) | Gap reduction |
|---|---|---|---|
| +0% | 2.3002 | 0.6763 | — |
| +1% | 2.3166 | 0.6490 | 4% |
| **+2%** | **2.3442** | **0.0613** | **91%** |
| +3% | 2.3678 | 0.0220 | 97% |
| +5% | 2.3802 | 0.0013 | 99.8% |
| +8% | 2.4831 | 0.0003 | >99.9% |

The pure-efficiency optimum produces a non-trivial equity gap of 0.676 h,
confirming that minimizing response time alone *does* produce a geographic
disparity on this instance — it is not a hypothetical concern. The central
finding is that **this disparity is remarkably inexpensive to correct**: a 2%
sacrifice in mean response time removes 91% of the gap, and by 5% the gap is
essentially eliminated (99.8% reduction). We regard this as the paper's
principal decision-support result: on this network and instance, equitable
dispatch is not a difficult trade-off against efficiency but a nearly free
adjustment to it.

### 6.4 Priority faults and the priority–zone confound

**Table 7.** Effect of high-priority weighting on the Far/Near response ratio.

| High-priority weight $w_H$ | Mean response (h) | Far/Near ratio | Mean High-priority arrival (h) |
|---|---|---|---|
| 1.0 (used throughout) | 2.3389 | 1.1703 | 1.9164 |
| 1.5 | 2.2373 | 1.1656 | 1.5956 |
| 2.0 | 2.1692 | 1.1489 | 1.5864 |
| 3.0 | 2.0552 | 1.1451 | 1.5864 |

In the base instance, **4 of the 5 High-priority faults fall in Far-zone
towns** — a property of this particular random draw, not of any underlying
relationship between urgency and geography. Table 7 shows that simply raising
the priority weight $w_H$ moves the Far/Near response ratio downward on its
own, with no equity *mechanism* doing any of the work — an entirely spurious
"equity improvement" that is really just the priority weighting happening to
also privilege Far-zone faults in this draw. **Every equity result in this
paper (Sections 6.3, 6.5) is computed at $w_H = 1$** specifically to avoid this
confound; priority weighting is presented here as a separate, clearly labeled
analysis, not folded into the equity results.

**Table 8 / Figure 5.** Feasibility of a high-priority response-time service
guarantee ($w_H=1$).

| Target $D$ (h) | Feasible | Mean response (h) | Penalty vs. no target | Mean High-priority arrival (h) |
|---|---|---|---|---|
| none | — | 2.3389 | — | 1.9164 |
| 3.0 | Yes | 2.5190 | +7.7% | 1.8856 |
| 2.5 | Yes | 2.6133 | +11.7% | 1.3296 |
| 2.0 | **No — proven infeasible** | — | — | — |
| 1.5 / 1.2 / 1.0 / 0.8 | No — proven infeasible | — | — | — |

With the current five-crew establishment, a service guarantee that every High-
priority fault is reached within **2.5 hours** is achievable at an 11.7% cost in
mean response time; a 2-hour guarantee is **provably infeasible** regardless of
dispatch policy. This is a directly actionable operational statement: if ECG
Hohoe does have (or wishes to adopt) a formal restoration-time target for
high-priority faults, this model can state precisely whether the current crew
establishment can meet it, and at what efficiency cost.

### 6.5 Multi-instance study

A single instance cannot establish how representative these results are. We
generated 15 additional fault instances (15 faults each, independent random
seeds) against the same real town network and repeated the full analysis.

**Feasibility of the current establishment.** With the current five-crew
establishment, only **2 of 15 (13.3%, Wilson 95% CI [3.7%, 37.9%]) instances are
shift-feasible at all**: required crew-time across the 15 instances averages
47.73 h (range 36.91–58.05 h) against 40 h available, implying 92–145%
utilization. **On most simulated days, no feasible assignment exists under the
current crew count** — a resourcing conclusion, not an artifact of the solution
method.

**Minimum crews required.** For each instance, we computed the minimum crew
count $m$ for which a feasible assignment exists (holding $Q=3$, $H=8$h fixed).
**Figure 4** and Table 9 report the distribution.

**Table 9.** Minimum feasible crew count across 15 simulated instances.

| Minimum crews | Instances | Cumulative coverage |
|---|---|---|
| 5 (current) | 2 | 13.3% |
| 6 | 5 | 46.7% |
| 7 | 5 | 80.0% |
| 8 | 2 | 93.3% |
| 9 | 1 | 100.0% |

The median requirement is 7 crews; raising the establishment from 5 to 7 crews
would make 80% of simulated days feasible, and 9 crews would cover all 15. We
present this as a direct, quantified staffing recommendation, independent of
any claim about optimization quality.

**Optimum vs. heuristic, instance-by-instance.** For each instance, solved at
its own minimum feasible crew count (so the comparison is not conditioned on
feasibility at a fixed establishment), we compared the exact optimum against
the local-search heuristic of Section 6.2. Across the 14 instances where both
produced a feasible plan, the heuristic's combined objective exceeded the
optimum's by a median of **0.39%** (Wilcoxon signed-rank $W=0$, $p=0.005$);
differences in mean response time alone and in the equity gap alone were each
*not* individually significant ($W=13, p=0.139$ and $W=9, p=0.110$
respectively, median difference 0.0% and 0.0 h in each case — several
instances tied exactly).

We flag explicitly that the significance of the combined-objective comparison
should not be over-read: because the optimum by construction minimizes the very
quantity being compared, it is mathematically guaranteed never to lose, so a
one-sided Wilcoxon test here is close to automatically significant whenever any
real difference exists at all, however small. **The magnitude (0.39%) is the
informative number; the $p$-value is not evidence of a large effect.** We
report this candidly because overstating the efficiency case for optimization
is a common and avoidable overclaim in applied operations-research case
studies, and because the paper's stronger, better-supported claims (Sections
6.2's feasibility result and 6.3's equity-cost result) do not depend on it.

### 6.6 Scalability

To assess whether the set-partitioning method remains usable beyond the
15-fault base instance, we generated synthetic instances at $n \in
\{15,24,30,45,60\}$, scaling the crew count $m$ at each size to hold crew
utilization approximately constant at the base instance's 95.1% level (simply
holding $m$ fixed at 5 while increasing $n$ makes every larger instance
infeasible purely on crew-hours, which is a resourcing fact, not a scalability
result — see Section 6.5).

**Table 10.** Scalability of the set-partitioning method.

| $n$ | $m$ | Utilization | Feasible columns | Enumeration time | Solve time | Outcome |
|---|---|---|---|---|---|---|
| 15 | 6 | 83.7% | 1,635 | 0.006 s | 1.03 s | Proven optimal |
| 24 | 10 | 89.9% | 4,676 | 0.019 s | 144.0 s | Proven optimal |
| 30 | 14 | 92.3% | 5,224 | 0.022 s | 246.3 s | Proven optimal |
| 45 | 19 | 90.6% | 29,861 | 0.179 s | 601.5 s | Best found within time limit; gap 0.0%† |
| 60 | 26 | 92.9% | 62,708 | 0.422 s | 28.8 s | Proven optimal |

†The $n=45$ instance was stopped at a 600-second time limit before the solver's
internal search completed, as reported by the solver's own log (see Section
5.5); the final reported optimality gap at that point was 0.0%, so the returned
solution is very likely optimal, but this has not been formally proven and we
report it accordingly rather than as a proven optimum.

Solve time does not increase monotonically with $n$: the $n=60$ instance solved
in 29 seconds while the smaller $n=45$ instance did not complete within the
600-second budget. This reflects that computational difficulty in this method
depends on how tightly a particular instance's column structure packs, not
simply on the number of faults, and should be reported as such rather than
implying a smooth, predictable growth curve.

---

## 7. Discussion

Three results in this study are, in our view, more important for an operating
utility than the headline fact that an exact optimum exists. First, **the
current five-crew establishment appears, on simulated but realistically scaled
demand, to be under-resourced for most days** (Section 6.5) — a conclusion that
does not depend on optimization quality at all and would be equally true if
dispatch were done perfectly by hand. Second, **the price of fairness on this
network is low**: a 2% efficiency sacrifice removes the great majority of the
Near/Far response-time disparity that an efficiency-only policy produces
(Section 6.3). Third, **a formal priority service guarantee is directly
testable** against the current establishment, and the model can state precisely
where such a guarantee becomes infeasible (Section 6.4).

By contrast, the result we are most careful *not* to overstate is the
efficiency comparison against a well-constructed heuristic (Sections 6.2, 6.5):
the exact optimum's advantage there is modest, and we believe this is an honest
and useful finding in its own right. It suggests that for this problem class
and scale, the primary operational value of a formal optimization approach may
lie less in squeezing additional efficiency out of an already-competent
dispatcher's intuition, and more in (a) *guaranteeing feasibility* when the
day's demand is tight, (b) *making the equity trade-off explicit and tunable*
rather than implicit and unmanaged, and (c) *supporting direct, auditable
answers* to resourcing and service-guarantee questions that would otherwise
require ad-hoc judgment.

---

## 8. Limitations

We state these explicitly, as a frank limitations section is, in our view, more
valuable to a reader than a paper that omits or buries them.

1. **Fault instances are simulated.** The 23-town road network and its travel
   times are real, field-measured data; the 15 (and additional 15 for the
   multi-instance study) daily faults are synthetically generated, and the
   fault-type and priority distributions used to generate them are unsourced
   assumptions (Section 3.5). Results about *this specific instance's* optimal
   plan should be read as a demonstration of method, not as an operational
   recommendation for a specific day; results about *feasibility rates and
   resourcing* (Section 6.5) depend on these same assumed distributions being
   reasonably representative, which has not been independently verified.

2. **No inter-site routing is modeled.** Crews are modeled as returning to the
   single operations base between every two assigned faults. Operational field
   input available to the authors indicates that crews may in practice travel
   directly between fault sites in some circumstances, returning to base
   primarily when a specific tool or material is needed. Modeling this
   correctly would require a town-to-town travel-time matrix, which was not
   available at the time of this study, and recasts the problem as a
   capacitated vehicle-routing problem rather than a parallel-machine
   scheduling problem. We regard this as the most significant and most
   tractable direction for follow-up work, given the field-collected,
   depot-to-town travel-time data already in hand as a starting point for
   estimating or collecting the required town-to-town matrix.

3. **The planning horizon is static.** All faults in a given instance are
   assumed known at the start of the shift. Field input suggests faults may be
   reported during the shift rather than only at its start, which would argue
   for framing this model as representing either (a) morning dispatch planning
   under faults known at that time, or (b) an offline upper bound on achievable
   performance against which a rolling, dynamic re-dispatch policy could be
   compared — we have not implemented or evaluated such a dynamic policy here.

4. **Travel times are deterministic.** No seasonal, weather-related, or
   time-of-day variation in travel time is modeled, despite the Volta Region's
   terrain and road conditions plausibly producing real variation of this kind.

5. **A single district and a single day are modeled at a time.** No multi-day
   rostering, fault carry-over, or crew fatigue/rest constraints are
   represented.

6. **Faults are treated as electrically independent.** The model does not
   represent feeder-level topology, under which restoring one fault might
   already restore (or fail to restore) customers affected by another; this is
   a simplification relative to how outage restoration interacts with the
   underlying distribution network.

7. **Operating parameters are asserted, not independently sourced.** The 8-hour
   shift length, the 3-fault crew capacity, the 5-crew establishment, and the
   assumption that all crews are equally skilled and based at the same depot
   are all stated by the project team as representative of current practice but
   have not yet been independently confirmed with ECG Hohoe's own operating
   standards.

---

## 9. Conclusion and Future Work

We have formulated the daily technician-dispatch decision for a rural
electricity distribution district as a parallel-machine scheduling problem with
an explicit equity constraint on customer response time, identified and
corrected a degeneracy in the natural total-travel-time objective, and solved
the resulting model to proven optimality via an exact set-partitioning
reformulation that runs in well under one second on the base instance. The
central applied findings are that the current five-crew establishment appears
resourced for only a minority of plausible daily demand, that geographic equity
in response time can be substantially restored at a small efficiency cost
(2% for a 91% reduction in the measured gap), and that the exact optimum's
efficiency advantage over a well-constructed heuristic is modest — a candid
result we regard as useful rather than disappointing, since it clarifies where
this type of model actually adds value.

The most promising direction for follow-up work is extending the model to
represent direct inter-site crew travel (full vehicle routing rather than
base-return-only parallel scheduling), for which field input gathered during
this study provides initial motivation; a second is replacing the simulated
fault-generation process with an actual historical fault log, which would allow
every resourcing and feasibility conclusion in Section 6.5 to be stated with
considerably more confidence.

---

## Acknowledgements

We thank the Electricity Company of Ghana's Hohoe Operations Department, and
Abdul Haliq in particular, for operational context informing this study.
*Publication of any district-specific operational data, and any attribution of
field input to a named individual, is contingent on written permission and
informed consent that have not yet been obtained — see Data and Code
Availability and `CORRECTIONS.md` item M10. This acknowledgement section must
not be finalized before that permission is in hand.*

## Data and Code Availability

All code, the full experimental suite, and the datasets discussed in Section 3
are available in the accompanying repository. The service-town travel-time
data (Table 1) are field-collected primary data; **their publication is subject
to written permission from the Electricity Company of Ghana, which has not yet
been obtained** (see `CORRECTIONS.md`). The synthetic fault-generation process
(Section 3.5) is fully specified and reproducible from a fixed random seed. A
reproducibility notebook (`notebooks/02_optimization_model.ipynb`) reconstructs
every result in Sections 4–6 from source, including the verification step of
Section 5.4.

## Author Contributions

*To be completed following CRediT taxonomy conventions once author roles are
finalized.*

## Conflict of Interest

The authors declare no conflict of interest.

## Ethics Statement

*This study references operational input from an ECG Hohoe technician.
Informed consent for this reference, and any applicable institutional ethics
approval or waiver, have not yet been obtained. This manuscript must not be
submitted until that process is complete; see `CORRECTIONS.md` item M10.*

---

## References

*[Placeholder — see Section 2. No references are listed here yet. The next
step after this draft is a verified literature search; nothing from
`docs/appendix_literature_research.md` should be copied into this section
without independently confirming it against the publisher's own record.]*

---

## Figures

- **Figure 1** (`result/figures/fig1_schedule.png`): Gantt chart of the optimal
  crew schedule, base instance.
- **Figure 2** (`result/figures/fig2_frontier.png`): Efficiency–equity frontier
  ($\varepsilon$-constraint sweep).
- **Figure 3** (`result/figures/fig3_zones.png`): Response time by zone at the
  optimum.
- **Figure 4** (`result/figures/fig4_crew_requirement.png`): Distribution of
  minimum crews required across 15 simulated instances.
- **Figure 5** (`result/figures/fig5_sla_sweep.png`): Feasibility and cost of a
  high-priority service-time guarantee.
