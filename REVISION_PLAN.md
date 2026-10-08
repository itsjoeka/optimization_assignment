# Revision Plan — to a Complete Draft by Friday 2 October 2026

**Supersedes §6 and §8 of [`AUDIT.md`](AUDIT.md).** §§1–5, §7 and §9.1 of the audit stand unchanged.
§9.2 (the round-trip feasibility probe) remains **superseded and unquotable**.

Written 22 September 2026 after two developments: a technician at the Hohoe post confirmed crews
travel **site-to-site**, and the deadline moved to **Friday 2 October**.

> ### How to read the numbers in this document
>
> | Marking | Meaning |
> |---|---|
> | *(field data)* | Computed directly from `dataset/*.csv`. Exact, but see **C6** — the zone-threshold decision moves several of these. |
> | *(synthetic matrix)* | Produced against a **fabricated** inter-town travel-time matrix. **Directionally reliable, provisional in magnitude.** Regenerate everything so marked once the real matrix lands. |
>
> No routing number in this plan is publishable as-is. They exist to prove the method works and to
> size the effects, not to go in the paper.

**Provenance.** Produced by 14 agents: 6 research, 3 independent formulation designs (each built and
solved), 3 judge panels (each rebuilding the candidates from scratch), 1 synthesis, 1 adversarial
critic. Full raw output in [`docs/`](docs/). The critic's corrections are **integrated below**, not
appended — §L lists what changed and why.

---

## A. What the field evidence changes

### A.1 The problem class

Crews do not round-trip to the depot between jobs; they drive directly from site to site, returning
only for tools or materials. That moves the project into a named, well-studied class:

> A single-depot, multi-vehicle **Cumulative Capacitated VRP with Service Times and a route-duration
> limit** (CCVRP), inside the **Technician Routing and Scheduling Problem** family (TRSP), augmented
> with a customer-side spatial-equity constraint. Theoretically the **multi-vehicle minimum-latency /
> k-travelling-repairman problem**.

Call it **E-CCVRP-ST** (Equitable CCVRP with Service Times). **Name the class in the abstract and the
first paragraph of Methods.** That converts the biggest reviewer risk — an untethered student MILP —
into the smallest.

**Do not claim the site-to-site protocol as novel.** Tool-driven depot returns are already an
explicit TRSP feature. The correct, referee-proof sentence is:

> *"A field interview with an ECG Hohoe technician confirms that district operations conform to the
> standard TRSP structure, in which depot returns are tool-driven rather than job-driven. We
> therefore model direct inter-site travel with an optional depot revisit."*

### A.2 Why the fatal defect becomes structurally impossible

This is what rescues the paper, and it is worth stating precisely.

**The old failure.** The objective's coefficient `t_j` depended **only on the fault**, never on which
crew served it or in what order. Coverage factored it straight out:

$$\sum_i\sum_j t_j x_{ij} = \sum_j t_j\Big(\sum_i x_{ij}\Big) = \sum_j t_j = 8.985\ \text{h}\ \textit{(field data)}$$

**Any objective additively separable over faults dies the same way.** State the defect in exactly
that generality in the paper — it is a better contribution than hiding it.

**Why routing cannot die that way.** Response time of the fault in position *p* of route
σ = (j₁…j_k) is $A_{j_p} = \tau_{0,j_1} + \sum_{q<p}(r_{j_q} + \tau_{j_q,j_{q+1}})$, so total route
waiting is a **positional-weight sum** $\sum_p A_{j_p} = k\tau_{0,j_1} + \sum_{q=1}^{k-1}(k-q)(r_{j_q}+\tau_{j_q,j_{q+1}})$.
The weights (k−q) attach to different legs when the route is permuted — a separable cost is
permutation-invariant; this is not. Independently, arrival times contain τ terms between **pairs** of
faults, so a fault's cost depends on which others share its route.

Formally, collapse requires a vector (γ_j) with $c_\sigma = \sum_{j\in\sigma}\gamma_j$ for every
feasible route. Either mechanism defeats that. Constancy needs all τ equal **and** all r equal; here
$r_j \in [0.33, 4.0]$ h *(field data)*. **Degeneracy is excluded by construction, not by luck.**

**Put this table in the paper.** Same three faults, same crew, same total driving, route reversed:

| Route | Arrival times (h) | Σ waiting | Route duration |
|---|---|---|---|
| F15 → F7 → F10 | 0.267, 1.580, 2.318 | **4.165 h** | 6.801 h |
| F10 → F7 → F15 | 0.483, 4.891, 5.784 | **11.158 h** | 6.801 h |

*(synthetic matrix — regenerate on the real one)*. **Identical duration, 2.68× the customer waiting,
and identical 8.985 h under the old objective.** That is the whole diagnosis in one table: a travel-time
objective is order-blind, an arrival-time objective is not. Three judge panels reconstructed it to the digit.

### A.3 The LP-relaxation observation — state it carefully or not at all

A design agent noticed the arc model's root LP relaxation equals the old degenerate objective. Two
panels measured **0.599**, and indeed $\frac{1}{n}\sum_j t_j = 8.985/15 = 0.599$ exactly *(field data)*.

**The drafted sentence "the degenerate objective IS the LP bound" is wrong by a factor of n and must
not reach print.** The defensible version:

> *"The root LP relaxation of the vehicle-flow formulation equals the published objective divided by
> the number of faults — the per-fault 'teleportation' bound, the value obtained if every crew
> arrived everywhere at time zero. The original model was computing a valid but unattainable lower
> bound and reporting it as an optimum."*

Two caveats a referee will test: this is a property of the **arc relaxation specifically** (the
set-partitioning LP is far tighter — ≈1.42 against an integer optimum ≈1.43 *(synthetic matrix)*, no
such coincidence), and it is matrix-independent because it depends only on the field-measured depot
legs. Stated with both caveats it is an interesting paragraph; overstated it is a free hit.

---

## B. The recommended formulation

Three independent judge panels reached the same verdict **unanimously**, scoring it 9–10 on every
criterion including deadline safety:

> **Present the problem as an arc-based vehicle-flow MILP (the model). Solve it by a priori route
> enumeration and set partitioning (the method). Report the comparison as a computational result.**

**Why both.** The arc model is what a referee expects and stays valid when crews stop being identical
or depot-based. The set-partitioning encoding is what actually solves: **0.010 s to enumerate,
0.106 s to a proven optimum**, against 70–150 s for the arc model and **never** for the
position-indexed alternative *(synthetic matrix)*. That speed is what makes ten days work — the whole
sensitivity suite regenerates in minutes the afternoon the real matrix lands.

**Claim no novelty in the model class.** Claim the application, the primary data, and the
customer-side equity treatment.

### B.1 The set-partitioning solver (SP-ECG) — the thing you actually build

Because Q = 3, the complete ordered route set is $15 + 210 + 2730 = 2{,}955$. Enumerate all,
price each **exactly** in closed form, discard those exceeding H, solve a set-partitioning master.
**The column set is complete, so this is exactly optimal — not a heuristic, not a relaxation.**

Per route ω = (j₁…j_k), computed once at enumeration time:

$$a^\omega_1 = \tau_{0,\text{site}(j_1)}, \qquad a^\omega_p = a^\omega_{p-1} + r_{j_{p-1}} + \tau_{\text{site}(j_{p-1}),\text{site}(j_p)}$$
$$D_\omega = a^\omega_{k} + r_{j_{k}} + \rho\tau_{\text{site}(j_k),0}, \qquad c_\omega = \sum_p w_{j_p} a^\omega_p, \qquad e^z_\omega = \!\!\sum_{p: j_p \in J^z}\!\! a^\omega_p$$

Admit ω iff $D_\omega \le H$ and any operating rule holds (SLA, position cap, restocking). With
λ_ω ∈ {0,1}:

$$\min\ \alpha\cdot\frac{1}{W}\sum_\omega c_\omega\lambda_\omega + \beta G$$
$$\text{(S1) }\sum_\omega A_{j\omega}\lambda_\omega = 1\ \forall j \qquad \text{(S2) }\sum_\omega \lambda_\omega \le m$$
$$\text{(S3) } G \ge \pm\Big[\Big(\tfrac{1}{n_F}\sum_\omega e^F_\omega\lambda_\omega - \bar\tau^F\Big) - \Big(\tfrac{1}{n_N}\sum_\omega e^N_\omega\lambda_\omega - \bar\tau^N\Big)\Big]$$
$$\text{(S4) } C_{\max} \ge D_\omega\lambda_\omega,\quad R^{\max} \ge M_\omega\lambda_\omega\ \ \forall\omega$$

**No big-M. No subtour elimination. No crew index, hence no m! = 120-fold symmetry.**

> ### ⚠️ **C3 — the Gini machinery is deleted from the model**
> An earlier draft added variables $d_{jj'} \ge \pm(R_j - R_{j'})$ to compute Gini mean difference
> inside the MILP. **Remove them.** They equal $|R_j - R_{j'}|$ only if GMD carries a positive
> objective coefficient, and the design explicitly says *don't optimise Gini* — so d is unbounded
> above and anyone reading GMD off the solver gets a meaningless number. That is 120 variables and
> 225 rows computing nothing. **Extract the route plan and compute GMD, Gini, R^max and range in
> Python post-hoc.** (Also: the drafted $\text{GMD} = \frac{1}{n^2}\sum_{j<j'}d_{jj'}$ is **half**
> the standard population GMD — unordered-pair sum with an ordered-pair normaliser — so every Gini
> would have been wrong by 2×.)

**Use the ε-constraint for the frontier figure, not the weighted sum:**
$$\min G \quad \text{s.t. (S1)–(S4)},\quad \tfrac{1}{W}\sum_\omega c_\omega\lambda_\omega \le (1+\varepsilon)Z^\star_{\text{eff}}$$

### B.2 The arc model (E-CCVRP-ST) — for presentation and one cross-check only

Full statement in [`docs/appendix_full_synthesis.md`](docs/appendix_full_synthesis.md) §6A.2. Two
lemmas earn their space in Methods:

> **Lemma 1 (subtour elimination is free).** If $r_i > 0$ for all i, the arrival recursion
> $R_v \ge R_u + r_u + \tau_{uv} - M_{uv}(1-\hat x_{uv})$ admits no cycle among fault nodes. Summing
> around a cycle: big-M terms vanish, R telescopes to zero, giving $0 \ge \sum_u r_u > 0$. ∎
> **Strict positivity of r is load-bearing** (min 0.33 h here) — a zero-duration inspection job would
> silently break it.

> **Lemma 2 (shift limit as a variable bound).** **Under the triangle inequality**, imposing
> $R_j \le H - r_j - \rho\tau_{j0}$ at every fault is equivalent to imposing it only at each route's
> last fault. ∎

> ### ⚠️ **C1 — the arc model as drafted repeats the exact defect this project is fixing**
> $R_j$ appears only in **≥** constraints. It is driven to the true arrival time *only* by the
> efficiency term. Whenever the objective stops pushing it down, **the solver inflates $R_j$ and buys
> equity with fiction.** Verified numerically on the repo's real fault data:
>
> | Run | Model reports G | **True gap recomputed from the chosen routes** |
> |---|---|---|
> | α=1, β=0 | 0.1080 | 0.1080 ✓ |
> | **α=0, β=1** | **0.000000** | **0.587667** ✗ |
> | ε-constraint, ε=0.05 | 0.042467 | 0.052800 ✗ |
>
> At β=1 the model reports *perfect equity* while its routes have a 0.59 h gap. The ε-constraint
> understates by 24% — **and that is the number that would have gone in the frontier figure.** This
> is the same disease as v1: a quantity that looks optimised but is decoupled from the decision.
>
> **Two fixes, apply both.** (i) Add the reverse big-M so R is pinned by equality:
> $R_v \le R_u + r_u + \tau_{uv} + M(1-\hat x_{uv})$ and $R_j \le \tau_{0j} + M(1-\sum_k x_{0jk})$.
> Then state in Methods that $R_j$ equals arrival time in *every* feasible solution, not just optimal
> ones. (ii) **SP-ECG is immune by construction** — arrival times are computed in Python per route,
> never chosen by a solver. This is a substantive argument for the set-partitioning method and
> belongs in the paper.

> ### ⚠️ **C2 — Lemma 2's triangle precondition contradicts the matrix policy**
> Lemma 2 needs the triangle inequality. The matrix plan says *don't* apply metric closure. With
> violations present the arc model cuts off routes SP admits, the feasible sets differ, and the
> cross-check fails for reasons nobody will understand at 11pm on a Thursday. Violations are likely
> here because the matrix is field-measured on row 0 and API-derived in the interior with a fitted
> overhead on the depot legs.
>
> **Decide once:** enforce metric closure on the **interior only**, keep depot legs verbatim,
> re-check. Run the cross-check at **n ≤ 8** where it is cheap, and **before** Gate 1 — not as a
> headline result.

---

## C. Equity — the design, and three adjudications

**Why an equity term is needed at all.** Minimising mean latency is Smith's-rule-like: it front-loads
short, near jobs. The bias against far customers is a **property of the efficiency objective**, not an
accident of this data. Under pure efficiency the Far/Near response ratio is **1.79**, and across every
geometry tested (circuity 1.0–1.6, bearing jitter ±25°/±45°, asymmetry ±15%) it stayed in **1.37–3.02
and was always > 1** *(synthetic matrix)*. **Demonstrate this rather than asserting it** — it is the
paper's argument for the whole equity apparatus.

**Adjudication 1 — use excess wait, not raw zone means.** Far towns are *by construction* further
away, so equalising *raw* means can only be achieved by delaying near customers ("levelling down").
Define $E^z = \bar R^z - \bar\tau^z$ — the delay the **dispatcher** causes, net of geography. Linear,
because $\bar\tau^z$ is a constant. All three panels grafted this independently. It reaches parity to
within 0.2% at a 5.1% efficiency cost **and improves the worst-served customer** (3.59 → 3.08 h),
whereas the raw-ratio form was measured to *worsen* the worst customer as θ tightened.

**Adjudication 2 — G and θ must be two-sided, and θ is defined only on [1, ∞).** A one-sided
constraint lets the solver buy feasibility by **inflating near-zone response** — the original failure
mode in a new costume, and not hypothetical: a panel caught a one-sided run "achieving equity" with
E^N = 1.087 > E^F = 0.914. But all three designs then missed that the two-sided *hard cap* is
identically infeasible for θ < 1: $E^F \le \theta E^N$ and $E^N \le \theta E^F$ imply
$E^F \le \theta^2 E^F$. Keep $G \ge |E^F - E^N|$ two-sided always; state θ ∈ [1, ∞); drive sub-parity
exploration with the ε-constraint, which is well-posed throughout.

**Adjudication 3 — ε-constraint for the frontier.** The weighted sum recovers only supported
(convex-hull) Pareto points: β = 0.15 and β = 0.30 return the **identical plan**, while the
ε-constraint gives 5 distinct plans over 6 budgets. Three panels found the same collapse. **Report
both** — the α/β table as the scalarisation the README promised, the ε-constraint as the frontier
figure. And β = 1 is catastrophic (79.6% efficiency loss), so **never optimise dispersion alone**.

**Report three equity lenses, not one:** zone gap G (the policy instrument, optimised); **Gini/GMD**
of individual $R_j$ (threshold-free — answers the referee who attacks the 19.5 km zone cut);
and **$R^{\max}$** (the most politically legible number — *"no town waits more than X hours"*).
Report $R^{\max}$ but do **not optimise** it — min-max can cost up to m× the min-sum optimum.

**Also report crew-side workload spread**, and state explicitly that customer-side and crew-side
equity are distinct and why you chose customer-side. **Conflating them is the single most common
referee complaint in this literature**, and the distinction is the paper's sharpest positioning move:
the VRP equity literature is overwhelmingly crew-side workload balance, while Near/Far is
customer-side spatial accessibility from equitable facility location.

---

## D. Priority — and the highest-value catch in the review

Priority enters three ways, all free in set partitioning: soft weight $w_j$ inside $c_\omega$
(normalise by $W = \sum_j w_j$, **not** by n); hard SLA $R_j \le D$ for high-priority faults (a column
filter); position cap (also a filter).

> ### 🔴 **The priority/zone confound — control for this or the equity finding is a random seed**
> From the CSV *(field data)*: the High-priority faults are **F1, F3, F6, F8, F10** — and **four of
> the five are in Far towns.** Priority weighting *alone* therefore drags the Far/Near ratio down with
> no equity mechanism doing any work:
>
> | $w_{\text{High}}$ | Mean response | **Far/Near ratio** |
> |---|---|---|
> | 1.0 | 1.428 h | **1.789** |
> | 1.5 | 1.467 h | **1.421** |
> | 2.0+ | 1.467 h | **1.421** |
>
> *(synthetic matrix)*. That is a property of `random.choices(seed=60)`, not of Hohoe. **Run every
> equity experiment at $w_{\text{High}} = 1$** and present priority weighting as a separate, clearly
> labelled experiment. Two judge panels and the synthesiser verified this independently; the design
> that produced the winning formulation did not spot it.

**The SLA sweep is the best result in the study.** At $w_{\text{High}} = 1$ *(synthetic matrix)*:

| D | Feasible columns | Mean response | Mean High-priority arrival | Status |
|---|---|---|---|---|
| none | 2,350 | 1.428 h | 1.608 h | optimal |
| 2.0 h | 1,418 | 1.464 h (+2.5%) | 1.279 h | optimal |
| 1.5 h | 1,177 | 1.682 h (+17.8%) | 1.062 h | optimal |
| 1.2 h | 1,083 | 1.944 h (+36.1%) | 0.840 h | optimal |
| 1.0 h | 908 | — | — | **proven INFEASIBLE** |

A second agent reproduced the same feasibility threshold (1.2 h feasible, 1.0 h infeasible) on a
completely different synthetic matrix. **That cross-matrix replication is the most robust finding in
the review.** It yields the sentence the utility actually wants:

> *"With five crews, Hohoe can guarantee every high-priority fault is reached within 1.2 hours; a
> 1-hour target is infeasible. The 1.2-hour guarantee costs 36% on mean response."*

**Get ECG's real restoration target** and that becomes a statement about whether the utility meets its
own standard. Until then present D as a sweep with no privileged value.

**Relax Q and audit §5.4 dissolves.** With n=15, m=5, Q=3, total capacity is exactly 15 — every crew
must take exactly 3, so arithmetic fixes much of the decision space. The 8-hour shift self-limits
route length anyway, so **run the headline at Q=3 (ECG's stated rule) and report Q-free as the primary
sensitivity**. Relaxing Q to 4 improves mean response 4.7% with an unbalanced load [2,3,3,3,4].

> ⚠️ **C5 — Q-free enumeration needs prefix-pruned DFS.** The complete ordered route set at n=15 with
> Q free is **3,554,627,472,075**, not 92,229. The small figure is reachable *only* by depth-first
> search pruning on partial route duration — valid because prefix arrival times are monotone
> increasing. **State that monotonicity lemma explicitly**; it is what makes "complete column set ⇒
> exactly optimal" true at Q-free. A student writing `itertools.permutations` hangs forever, on Friday.

---

## E. Assumptions — state every one in Methods

| # | Assumption | Status | Action |
|---|---|---|---|
| A1 | Crews travel **site-to-site** | **Confirmed by interview** | The justification for routing over assignment. Cite the interview. |
| A2 | Crews return to post at **end of shift**, inside the paid 8 h (ρ=1) | **Assumed — not asked** | Charge the return leg to H but **never to the objective** (no customer waits on it). ρ=1 and ρ=0 give the identical plan at n=15, so not load-bearing — but ask. |
| A3 | No mid-shift depot return in the base case | **Known approximation** | Handled as a column filter, not deferred. Ask how often it fires. |
| A4 | All 5 crews start at the post, identical, Hohoe-based | Assumed | If any crew is out-district, SP columns re-root trivially but the 2-index arc reduction becomes invalid. |
| A5 | **All n faults known at shift start** | ⚠️ **Contradicted by the interview — see below** | Frame explicitly as morning dispatch planning. |
| A6 | H=8 h, Q=3 are ECG's real figures | **Asserted, no source** | Confirm. |
| A7 | δ=0.05 h between faults in the same town | Assumed | State it. |
| A8 | Near/Far threshold | ⚠️ **Unstable — see C6** | Fix exogenously, decide Wednesday. |
| A9 | Faults are **simulated** | **True** | Disclose in the **abstract**. Retitle to *"A Simulation Case Study Grounded in the Hohoe Operations Department."* |

> ### 🔴 **The biggest interpretive miss: the technician described a *dynamic* problem**
> The quote is *"**when there's a call** and they are already at a different site, they just move to
> the new place."* **"When there's a call"** means faults arrive *during* the shift — which directly
> contradicts A5. The same sentence that justifies routing over assignment also undermines the static
> horizon, and a referee who reads the interview quote in the paper will see it immediately.
>
> **Two honest options.** (a) Frame the model explicitly as **morning dispatch planning, or an offline
> benchmark bound on achievable performance** — one paragraph, defensible, costs nothing. (b) Add a
> cheap **rolling-horizon evaluation**: re-solve on each arrival, which at 0.13 s per solve is
> genuinely realistic and would be a strong result. **Do not leave the contradiction visible and
> unaddressed.**

> ### ⚠️ **C6 — the zone-threshold decision moves numbers marked *(field data)***
> Under 19.5 km (current code): $n_N=8$, $n_F=7$, $\bar\tau^N=0.468875$, $\bar\tau^F=0.747714$.
> Under 20 km (README): **Liati, at exactly 20.0 km, flips to Near** → $n_N=9$, $n_F=6$,
> $\bar\tau^N=0.477889$, $\bar\tau^F=0.780667$. Every equity constant, every $E^z$, the 1.789 ratio
> and the priority-confound table all move. **Decide the threshold on Wednesday morning, before any
> result is generated**, recompute all constants, and put a one-line threshold-sensitivity result in
> Results.

---

## F. Verification protocol — non-negotiable, and cheap

Defect **C1** existed because nothing recomputed the model's own outputs from its own decisions.
**Write this first, Wednesday morning, before any experiment.** One file, three asserts, called by
every experiment script:

1. **Coverage** — all 15 faults assigned exactly once.
2. **Status** — `Optimal` parsed from the CBC log, not assumed.
3. **Independent recomputation** — extract the chosen routes, recompute every $R_j$, $G$, $\bar R^N$,
   $\bar R^F$, $C_{\max}$ in plain Python, and **assert agreement with the model's own values to 1e-6**.

Assert 3 is the one that catches the whole class of bug that sank v1 and nearly sank v2.

Plus, once each: **brute-force cross-check** at n ≤ 8 (enumerate every partition, confirm the SP
optimum), and the **arc-vs-SP equivalence check** at n ≤ 8 (after resolving C2).

---

## G. The travel-time matrix — the critical path

**Nothing else is blocking. This is.** Every routing number here rests on a fabricated matrix, and a
paper that ships with one is rejectable on that alone. With normal internet it is **one afternoon**.

**Minimum viable artefact:** the 15-fault instance touches only **12 distinct towns** *(field data)*,
so a **13×13** matrix reproduces the headline instance exactly. **Build that first**; the full 24×24
is needed only for new instances and the scaling study.

**M1 — coordinates (~2 h, BLOCKING).** 24 verified lat/lon. This is the whole critical path. Record
`dataset_name, verified_settlement_name, latitude, longitude, gps_source, corridor_road`. Several
town names are ambiguous and need an ECG callback — start today.

**M2 — the matrix (~10 min).** **One HTTP request, not 253.** OSRM's `/table` returns up to 10,000
durations per call:
```
GET https://router.project-osrm.org/table/v1/driving/{lon1},{lat1};...;{lon24},{lat24}?annotations=duration,distance
```
**Coordinates are LON,LAT** — this trips everyone up. Depot first. Divide durations by 3600, distances
by 1000. Max 1 req/s, non-commercial. Commit the raw JSON.

**M3 — calibration (~30 min).** Compare the API's depot row against your 23 field-measured legs, fit a
single scaling constant λ, apply to the interior only. Check triangle-inequality violations (see C2).

**The no-API fallback — publish a bracket, never a point estimate.** Two metric-consistent
constructions:
- **Matrix A — corridor tree (upper bound), needs no coordinates.** Cross-corridor travel routes back
  through Hohoe: $d(i,j) = |d_i - d_j|$ within a corridor, $d_i + d_j$ otherwise. Mean 0.804 h.
- **Matrix B — polar law-of-cosines × circuity 1.162 (lower bound), needs corridor bearings.** Mean 0.608 h.

Both are **symmetric with zero triangle violations** — worth stating explicitly, because most ad-hoc
imputation schemes *do* violate the triangle inequality and produce VRP "optima" that are artefacts.
Solve under both and report the spread on every headline number. Measured: mean response moves
**2.8%**, makespan 2.7%, Near/Far gap **0.7%**, improvement over ad-hoc stays in **45.5–48.9%**. That
makes the matrix **non-load-bearing for every claim the paper makes**.

**What the bracket does NOT license:** the optimal crew-to-fault *partition* differs between matrices
(one comparison shared only 9 of 20 arcs). **The aggregates are outside the uncertainty; the specific
dispatch plan is inside it.** Say that in one sentence and you disarm the objection pre-emptively.

### A genuine side-result: the speed model

Fitting on the 22 clean towns (Fodome excluded):
$$t = 0.1595 + 0.02059\,d, \qquad R^2 = 0.8957,\ \ \text{LOOCV } Q^2 = 0.8743,\ \ \text{CV MAE} = 3.72\ \text{min}$$

The intercept is **9.6 min** (p = 0.0001), the slope 1/48.57 km/h (p = 2.8×10⁻¹¹). Physically: ~10
minutes to clear Hohoe town, then ~49 km/h cruise. **So the audit's "1 to 47 km/h spread" is mostly an
artefact of dividing a fixed overhead by a short distance** — Wli at 47.2 km/h and Gbi-Kledzo at
18.4 km/h are the same vehicle on the same road model. Corridor structure adds nothing (ANOVA
F = 0.529, p = 0.716), so a single global speed model is adequate — **report that as a tested
negative, not an assumption.** This turns the dataset's most reviewer-visible oddity into a clean
data-section finding.

### What the paper MUST disclose

- **How many of the 552 ordered node pairs are field-measured: 23, i.e. 4.2%.** That ratio must appear
  in the paper. The danger sentence is any variant of *"travel times between towns were obtained from
  field data."*
- Provider, profile, query timestamp, traffic-aware or free-flow, the calibration constant, raw JSON committed.
- **The Fodome correction, with the rule and its sensitivity.** Do not silently fix it — a reviewer who
  downloads the CSV, sees `0.65, 0.65` and finds no mention will assume the worst.
- That the 15 faults are simulated (**in the abstract**).
- Solve time, time limit, best bound and gap for every solve, parsed from the CBC log.

**Keep the bracketed fallback in the paper even if the real matrix arrives.** *"How well can you do a
routing study with nothing but depot-to-town odometer readings?"* matters to every utility in the
region without a GIS department, and answering it with a measured error is a better contribution than
quietly deleting it.

---

## H. Ten-day plan

Three tracks run in parallel from Wednesday so nobody is blocked on the matrix. The optimisation track
develops against the bracketed fallback from day one and swaps in the real matrix by changing one
function.

| Person | Role | Track |
|---|---|---|
| **Jonathan Kalami** | SP-ECG engine, experiments | **O** |
| **Sally Gli** | Baselines, statistics, verification, scaling | **O** |
| **Tayyiba Amartey** | Coordinates, matrix, data repairs, figures | **M** |
| **Dr. Ali Abubakar** | ECG liaison, permissions, TRSP literature, Methods review | **W** |
| **Dr. Bright Owusu** | Equity/power literature, Intro & Related Work, venue, compliance | **W** |

> **2 October is the lecturer's deadline for a complete, internally reviewed draft. It is not a
> submission date.** Journal submission follows supervisor review. Say this to the lecturer now so
> expectations match.

### Tonight — Tuesday 22 September

- [ ] **Dr. Abubakar — email ECG Hohoe.** Written permission to publish district data, **plus the
      questions in §K**. The only critical-path item outside the team's control.
- [ ] **🔴 Ethics and consent — start tonight.** The paper's headline field-evidence claim rests on an
      interview with a named individual, and there is currently **no informed consent, no ethics
      clearance or waiver, and no anonymisation policy.** Journals ask at submission; university ethics
      offices take days even for a waiver. Get written consent from the technician, and from Abdul
      Haliq for being named. **Default to "an ECG Hohoe technician (name withheld)" unless consent to
      be named is explicit.** Draft an Ethics Statement section.
- [ ] **Dr. Owusu — email the CIRED 2027 secretariat** asking whether the 14 September abstract
      deadline was extended. Costs a 500-word abstract; CIRED is the best domain match in the world.
- [ ] **Tayyiba — start the coordinate sheet.** Every hour of delay here is an hour off the end.
- [ ] **All — agree authorship order, corresponding author, CRediT roles, in writing.**

### Wednesday 23 — foundations (move these earlier than instinct says)

| Track | Owner | Task |
|---|---|---|
| **O** | Jonathan | **09:00 first:** `requirements.txt` pinned, `src/` skeleton, **the §F verification module**. Then the SP-ECG engine. |
| **O** | Sally | Baselines (see below), 30→**12–15** instance generator, feasibility-rate harness |
| **M** | Tayyiba | **Decide the zone threshold (C6) before any result is generated.** Then coordinates → 13×13 matrix → calibration. Fix Fodome, normalise town names, repair `03_diagnostics.ipynb` |
| **W** | Abubakar | TRSP/routing literature; verify citations against publisher records |
| **W** | Owusu | Equity/power literature; **decide LaTeX vs Word and create the manuscript file** |

### Thursday 24 — 🚦 **Gate 1 (model)**

Do not proceed until all four hold:
1. SP-ECG returns a **proven optimum**; the §F recomputation asserts pass to 1e-6.
2. Brute-force cross-check at n ≤ 8 agrees.
3. Min–max spread over the identical feasible set is **large** (target > 100%) — this, **never the
   node count**, is the non-degeneracy evidence. ⚠️ SP-ECG *also* reports 0 B&B nodes, for the
   opposite reason (its LP bound is tight). **Say so explicitly in the paper** or a reader who has
   read the audit will conclude nothing changed.
4. ε-constraint produces **distinct** plans across budgets.

### Friday 25 — 🚦 **Gate 2 (matrix)**

13×13 real matrix committed with raw JSON, calibration reported, triangle check run. **If not: switch
to the bracket permanently and say so in the paper.** Do not let this slip past Friday.

### Sat 26 – Sun 27 — buffer and first writing pass
### Monday 28 — full results suite on the final matrix
### Tuesday 29 — 🚦 **Gate 3 (results freeze).** Every number and figure exists on disk. No figure is made after today.
### Wed 30 – Thu 1 Oct — write
### Friday 2 Oct — internal review by all five, hand in

### The results suite — with the critic's corrections

> ⚠️ **C4 — the scaling study as drafted runs on infeasible instances.** Holding m=5, H=8 (40
> crew-hours) while scaling n: mean repair alone is 1.338 h/fault, so Σ repair is 40.1 h at n=30 and
> 80.3 h at n=60. **Every solve time quoted for n ≥ 30 is time-to-prove-infeasibility.** Scale
> $m = \lceil n/3 \rceil$ (or hold utilisation constant), **state the rule in the table**, and re-run.
> Cut scaling at n ≤ 60.

> ⚠️ **C7 — the statistical comparison is undefined where it matters most.** If ad-hoc dispatch is
> feasible only 3–14% of the time, then on most instances the baseline has *no* feasible draw and the
> paired difference does not exist. **Make feasibility rate the primary endpoint** with a binomial CI;
> run the paired efficiency test (**Wilcoxon signed-rank, not t-test** — routing deltas will not be
> normal) on the subset where both are feasible, report that subset's n explicitly, and say plainly
> that the efficiency comparison is conditional on baseline feasibility.

> ⚠️ **C8 — carry equity metrics through the multi-instance loop.** As drafted it reports optimum,
> feasibility rate and improvement but **not G, not the Far/Near ratio, not price of fairness** — so
> the paper's central claim would rest on n=1. Nearly free once the loop exists.

> ⚠️ **C9 — the baselines are straw men and the audit's own request was dropped.** Audit §4.4 asked
> for *current ECG practice*; the drafted set is random, greedy-nearest, greedy-priority and
> zone-clustering — all weak, all beaten by construction. Comparing against the *mean* of feasible
> random draws also inflates the improvement. **Add:** (i) **best-of-20,000 random as an order
> statistic** (a much fairer bar), (ii) **2-opt/relocate local search on the greedy solution** — if
> the optimum only beats that by 3%, better to learn it now, and (iii) **ask the technician how
> dispatch is actually decided today** and encode it. Report improvement in absolute hours alongside
> %, against the 0.599 h teleportation floor so the reader sees the achievable range.

**Figures (target 7):** the route-reversal witness table (§A.2); crew Gantt on the real matrix;
ε-constraint frontier; SLA sweep; feasibility rate optimal vs baselines; Gini/Lorenz of $R_j$; solve
time vs n with the m-rule stated.

**Lead the Results with feasibility, not with a percentage.** *"Ad-hoc dispatch produces a
shift-feasible plan in X% of instances; the model produces one in 100% and is Y% faster"* is a much
stronger opening than any single improvement figure.

### 🔴 Is ten days enough? Not as originally scoped. Cut in this order:

1. **The position-indexed model** — 600 s, never closes, used only as a losing benchmark. Delete it.
2. **Scaling beyond n = 60**, and only after fixing the m-rule (C4).
3. **30 instances → 12–15.** The CI widens slightly; the claim survives.
4. **The full 24×24 matrix** → make the **13×13** the Wednesday target and 24×24 the stretch goal.
5. **The restocking scenario and the position-cap variant** if Thursday slips.

**Do not cut:** the §F verification checks, the feasibility-rate headline, the $w_H = 1$ confound
control, the Limitations section.

---

## I. Venue — the audit's advice is now wrong and must be inverted

**PowerAfrica 2026 ran this week in Nairobi (21–25 September); its paper deadline was 7 April 2026,
and no 2027 edition is announced.** Conference-first now means submitting ~March 2027 and appearing
~September 2027. **A journal is faster.**

> ### Recommendation: **Scientific African** (Elsevier, gold OA), with an **IEEE AFRICON 2027** short version in parallel.

**Why.** Its stated mission is publishing African primary data — exactly the project's strongest
asset. Scopus + ESCI + DOAJ. APC reported ~USD 720 (one source said ~200 — **verify**). CiteScore
~3.3, ~4 days to desk decision. **Risk:** ~13% acceptance and a fast desk screen, so the cover letter
and abstract must carry the contribution in the first three sentences.

**AFRICON 2027 — 23–25 September 2027, Kumasi, Ghana** (verified). IEEE Xplore indexed, **in your own
country**, CFP expected Feb–Mar 2027 — exactly when an October journal submission will be in review.
Short version at the conference, full version in the journal, cite across to avoid self-plagiarism.

**Fallbacks:** JESIT (SpringerOpen, **zero APC permanently** — verify Scopus status first); Decision
Analytics Journal (USD 2,190); International Transactions in Operational Research (Wiley/IFORS,
**subscription route is free**, higher bar); Socio-Economic Planning Sciences (the true disciplinary
home of the equity argument — the right aspiration for a follow-up with a second district).

> ⚠️ **Verify before committing money: is Ghana Research4Life Group A (full Elsevier waiver) or Group
> B (50%)?** Two sources said Group A, but Ghana's GNI per capita (~USD 2,370) suggests it may not
> qualify. **This single fact decides whether three of the five candidate venues cost zero or several
> thousand dollars.** Practical route: start a submission in Elsevier's system — it quotes the
> waiver-adjusted APC automatically. **Do not commit to a USD 2,000+ venue assuming a waiver.**

**Does the reformulation lift the tier?** Partly, and less than it feels like. It moves the paper from
unsubmittable to genuinely submittable — the big move. But depot-origin multi-vehicle routing with
capacity, duration and equity constraints is a **textbook class**. What lifts the tier is the
*empirical package*: the real matrix, calibration against 23 field legs, 12–15 instances, a
feasibility-aware baseline, the frontier. **With that package this is a solid Q2 applied case study.**
**Claim the application, the data and the trade-off curve; explicitly disclaim methodological novelty.**
Reviewers punish overclaiming far harder than modest scope.

---

## J. References and claims

86 candidate references across 7 themes are in
[`docs/appendix_literature_research.md`](docs/appendix_literature_research.md).

> ⚠️ **The `[verified]` flags are unearned.** Nothing was checked against a publisher record. Four of
> the riskiest were spot-checked and **all four are real**, so fabrication risk is lower than feared —
> but **relabel to `[title/venue corroborated, DOI+pages unchecked]` and keep the two-hour verification
> task.** Note the correct spelling **Çavdar**.

> ⚠️ **One characterisation is wrong, which is worse than a wrong page number.** Diadelmo et al. (2026)
> is cited as *"one of very few papers in the routine, non-disaster regime this project studies."* Its
> abstract opens on *"the increasing frequency of natural disasters"* — it is a post-event
> inspection-dispatch paper. **Re-read the abstract before citing**; either drop the "routine regime"
> framing or find a real exemplar. That framing is one of the few genuine novelty claims, so a free hit
> there is expensive.

> ⚠️ **Pre-empt the grid-topology objection.** Çavdar et al. argue disruption time depends on the
> routing sequence's interaction with *both* the road network and the power grid — restoring an
> upstream fault can restore customers downstream of another. A referee will ask why $R_j$ ignores grid
> topology. **One sentence in Limitations:** faults are treated as electrically independent;
> feeder-level dependency is Future Work. (Another argument for obtaining customers-per-fault.)

**🚩 Do NOT claim as novel:** the model class; the site-to-site protocol (standard TRSP); equity in
routing; the ε-constraint method; set partitioning.

**✅ You CAN legitimately claim:** the application to a rural sub-Saharan distribution district; 23
field-measured travel legs as primary data; a **customer-side** spatial-equity treatment (vs the
literature's crew-side workload balance); the measured efficiency–equity frontier as a decision aid;
the SLA feasibility threshold; the demonstrated efficiency-bias-against-far-customers result; and the
matrix-bracket methodology for utilities without GIS.

---

## K. Questions for ECG — send tonight

**On operations (each changes the model or the framing):**
1. Do crews return to the post **at end of shift**, and is that drive inside the paid 8 hours?
2. How often does a mid-job return for a tool or material actually happen — 1 job in 5, or 1 in 20?
3. **Which fault types require material stocked only at the post?**
4. Is Q = 3 faults/crew a real limit or an assumption?
5. Is H = 8 h the real shift? Is there paid overtime? **Is there a break or non-productive allowance
   inside it?** (shrinks effective H)
6. Are all five crews Hohoe-based and identically skilled? **How many crews are actually on duty on a
   typical day, and how many vehicles?** (if 5 crews share 3 vehicles the whole model changes)
7. **Do the 3 technicians ever split into 2 sub-teams?**
8. Does ECG use a formal Near/Far kilometre threshold?
9. Does ECG have a **published restoration target** for high-priority faults? *(This becomes D and
   turns the study's best result into a statement about whether the utility meets its own standard.)*

**On the problem's actual shape (from the critic — these were missing):**
10. **Are the day's faults known at shift start (overnight log), or do they come in live? Roughly what
    split?** — decides static vs dynamic framing (§E).
11. **What happens to a fault not reached before end of shift** — carried over, overtime, escalated? If
    carried over, "infeasible" is not a real operational state and the feasibility headline needs
    rewording.
12. **Who decides dispatch today, and by what rule?** — this is the missing baseline (C9).
13. Does travel time differ materially in rainy season or at peak hours? — the model assumes
    deterministic travel.
14. **Is Fodome's 0.65 km an odometer reading from the post or from somewhere else?** Ask the
    *measurement procedure*, not just the value — it may explain Fodome and Gbledi at once.

**Also request:** a historical fault log (even 1–3 months), **customers affected per fault or feeder**,
and ECG's own SAIDI/SAIFI/CAIDI for Hohoe or Volta.

> ⚠️ **C10 — the anonymisation fallback does not work.** The risk register said "anonymise to 'a rural
> district in the Volta Region' if ECG refuses." **You cannot anonymise 23 named towns with real road
> distances** — one search identifies the district. Treat ECG permission as **binary** and plan the
> refusal branch properly: publish the model plus a synthetic-geography instance, withhold the dataset.

---

## L. Corrections applied from adversarial review

An adversarial critic re-derived the recommendations and found ten material defects, all integrated
above rather than appended. The most important:

| # | Defect | Severity |
|---|---|---|
| **C1** | The arc model's $R_j$ was pinned only by minimality, so at β=1 it reported **G = 0.000 while its routes had a 0.588 h gap**, and the ε-constraint understated the gap by 24% — the number destined for the frontier figure. **The same class of defect as the original paper.** Verified numerically. | 🔴 P0 |
| **C2** | Lemma 2's triangle-inequality precondition contradicted the matrix policy in the same document. | 🔴 P0 |
| **C3** | The in-model Gini machinery computed nothing (120 vars, 225 rows) and its GMD formula was off by 2×. | 🔴 P0 |
| **C4** | The scaling study ran on **infeasible** instances from n ≥ 30 (m held at 5). | P1 |
| **C5** | Q-free enumeration is 3.55 **trillion** routes without prefix-pruned DFS. | P1 |
| **C6** | The zone-threshold fix silently invalidates constants marked *(field data)* — Liati flips. | P1 |
| **C7** | The paired statistical test is undefined where the baseline is infeasible. | P1 |
| **C8** | Equity metrics were not carried through the multi-instance loop, leaving the central claim at n=1. | P1 |
| **C9** | Baselines were straw men; the audit's request for *current ECG practice* had been dropped. | P1 |
| **C10** | The anonymisation fallback is not achievable with 23 named towns. | P2 |

Plus: the dynamic-arrival contradiction in the interview quote (§E), and **missing ethics/consent for
the interview** (§H) — both on the critical path and neither previously noticed.

**The lesson worth keeping:** C1 survived three design agents and three judge panels, and was caught
only by recomputing the model's outputs from its own decisions. That is why §F is non-negotiable and
why it is the first thing built on Wednesday.
