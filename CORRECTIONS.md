# Correction Register — Proof-of-Concept Assignment Model

**Scope decision (6 October 2026, by the team):** this is a **proof-of-concept** paper. The model
stays an **assignment** model. Crews dispatch from the Hohoe ECG base to sites. **Routing is
explicitly out of scope** and is named as Future Work.

This register supersedes the routing recommendation in [`REVISION_PLAN.md`](REVISION_PLAN.md) §B.
Everything else in that document — the equity design, the priority confound, the verification
protocol, the data corrections, the venue analysis and the reference pool — **still applies** and is
cross-referenced below.

---

## 0. The one thing that cannot be kept

Under base-to-site dispatch, travel to fault *j* costs the same whichever crew goes. The coverage
constraint then factors it straight out:

$$\sum_i\sum_j t_j x_{ij} \;=\; \sum_j t_j\Big(\sum_i x_{ij}\Big) \;=\; \sum_j t_j \;=\; 8.985\ \text{h}$$

**This holds for one-way travel and for round-trip travel alike**, and it is why CBC reported
`best objective 8.985, took 0 iterations and 0 nodes` and why the random baseline scored an identical
8.985 h. It is a property of the arithmetic, not of the dispatch protocol, so it survives every
version of the assignment story.

**What changes:** the objective becomes **response time** — hours from shift start until a crew
reaches each fault. **What does not change:** the model is still an assignment of faults to crews,
with a service order inside each crew's shift. No inter-site travel. No travel matrix. No subtour
elimination. No routing.

**Model class for the paper:** identical parallel machine scheduling, $P \,\|\, \sum_j w_j C_j$,
with crew capacity, a shift-duration limit and a spatial-equity constraint. Each fault is a job with
processing time $s_j = 2t_j + r_j$ (out, repair, back) on any of 5 identical machines. This is a
named, well-studied class with citable literature, and it is a **cleaner** proof-of-concept framing
than a VRP because it demands no data the project does not already hold.

> **Already validated.** This exact formulation was built and solved against the project's own data
> on 22 September: status `Optimal`, mean response 2.549 h, makespan 7.982 h of the 8 h shift, and the
> objective **varies** across feasible solutions. `AUDIT.md` §9.2 was marked superseded only because
> the depot-return assumption was in doubt; **the team's scope decision reinstates it.** Its numbers
> are provisional pending the corrections below, but the method is proven to work on this data.

---

## 1. Blocking — the paper cannot be submitted until these are done

| # | Correction | Why | Ref |
|---|---|---|---|
| **B1** | Replace the constant objective with weighted mean **response time** $\frac{1}{W}\sum_j w_j R_j$ | §0. The paper's central claim is currently unsupported | AUDIT §4.1 |
| **B2** | Rebuild the **equity constraint so it contains decision variables** | Current one constrains the input data, not the solution; vacuous at θ=1.6, infeasible at θ=1.5 | AUDIT §4.2 |
| **B3** | Make **α and β actually enter the objective**; add ε-constraint variant for the frontier | Defined, printed, never used. The multi-objective claim is undelivered | AUDIT §4.3 |
| **B4** | Build the **verification module first** — coverage, solver status, independent recomputation of every reported quantity | This class of defect has bitten the project twice. Nothing else is safe until it exists | PLAN §F |
| **B5** | Replace the single infeasible random draw with a **feasibility-aware benchmark suite** | n=1 baseline, and it violates the 8 h shift. Not a valid comparison | AUDIT §4.4 |
| **B6** | **Disclose that faults are simulated — in the abstract**, and retitle to *"A Simulation Case Study Grounded in the Hohoe Operations Department"* | Research integrity. Towns are real; faults are `random.choices(seed=60)` | AUDIT §4.6 |

## 2. Major — a referee will reject or demand revision without these

| # | Correction | Why | Ref |
|---|---|---|---|
| **M1** | **Decide the zone threshold exogenously** (19.5 vs 20 km vs ECG's own) **before generating any result** | Code says 19.5, README says 20, Liati at exactly 20.0 km flips between them. Changes $n_N$, $n_F$, both zone means, the Far/Near ratio and every equity constant | PLAN §C6 |
| **M2** | Use **excess wait** $E^z = \bar R^z - \bar\tau^z$, not raw zone means; two-sided gap $G \ge \lvert E^F - E^N\rvert$; θ defined on $[1,\infty)$ | Far towns are further *by construction*; equalising raw means can only be achieved by delaying near customers. One-sided θ lets the solver inflate near-zone response — the original failure mode in a new costume | PLAN §C |
| **M3** | **Use the `Priority` column**, and run every equity experiment at $w_{\text{High}} = 1$ | Currently generated and ignored. **4 of the 5 High-priority faults are Far**, so priority weighting alone moves the Far/Near ratio 1.789 → 1.421 with no equity mechanism working. Uncontrolled, the central finding is a random seed | PLAN §D |
| **M4** | **Sensitivity suite**: θ sweep, α/β sweep, ε-constraint frontier, Q ∈ {2,3,4,5}, H ∈ {6,8,10}, SLA sweep | One instance, one parameter setting. Most common desk-reject trigger after formulation errors | AUDIT §5.1 |
| **M5** | **Multi-instance study** (12–15 instances), carrying **equity metrics through the loop**, feasibility rate as the primary endpoint with a binomial CI, Wilcoxon signed-rank on the feasible subset | Otherwise the central claim rests on n=1 and the paired test is undefined where the baseline is infeasible | PLAN §C7, §C8 |
| **M6** | **Scaling study** with the crew count scaled as $m = \lceil n/3 \rceil$, and the rule stated in the table | At m=5 fixed, n≥30 is infeasible on repair time alone (40.1 h vs 40 h capacity) — every quoted solve time would be time-to-prove-infeasibility | PLAN §C4 |
| **M7** | **Fix the Fodome record** (0.65 km / 0.65 h ⇒ 1.0 km/h), document the rule and its sensitivity | Near-certain transcription error. Do not fix silently | AUDIT §5.3 |
| **M8** | **Literature: 20–30 references.** `# References` is currently empty | No literature engagement anywhere. Disqualifying on its own | AUDIT §5.7 |
| **M9** | **Figures (6–7)** — all generated before any writing begins | Zero figures exist | PLAN §H |
| **M10** | **Ethics, consent and ECG permission**; data availability statement; data licence distinct from the code's MIT | Not started. University ethics offices take days even for a waiver | PLAN §H |

## 3. Housekeeping — cheap, and each one is a visible credibility signal

| # | Correction | Ref |
|---|---|---|
| **H1** | `requirements.txt` with pinned versions | AUDIT §5.6 |
| **H2** | `src/` module importing into the notebooks — kills the θ=1.6 / θ=1.5 drift between notebooks 02 and 03 | AUDIT §5.6 |
| **H3** | Repair `03_diagnostics.ipynb` — syntax error at line 33, no imports, θ mismatch | AUDIT §5.6 |
| **H4** | Uncomment the `to_csv` cells in `01_data.ipynb` so the committed datasets are regenerable | AUDIT §5.6 |
| **H5** | Normalise town names (`Ve -Gbodome`, `Ve- Kobenu`, `Zimugaziwo snake Village`) | AUDIT §5.3 |
| **H6** | Delete `notebooks/codes.txt`; fold into the README | AUDIT §2 |
| **H7** | Fill the README's empty **Project Overview** and **References**; add Install / Run / Results; state the speed model | AUDIT §5.7 |
| **H8** | Report solve time, status, best bound and gap for every solve, parsed from the CBC log | PLAN §G |

## 4. Deliberately out of scope — name all of these as Future Work

Routing / inter-site travel · the travel-time matrix · dynamic fault arrivals · stochastic travel
times · multi-day rostering · grid-topology dependency between faults · crew skill heterogeneity.

> **Why the paper is stronger for saying so.** A proof-of-concept that states its boundary precisely
> reads as disciplined; one that hides a limitation reads as unaware. The routing extension is a
> genuine second paper, and the field evidence that motivates it is already in hand.

---

## 5. Order of work

Foundations first, because every number generated before the verification module exists has to be
regenerated afterwards anyway.

**Day 1 — foundations.** H1, H2, **B4**, M1 (threshold decision), M7, H3, H4, H5, H6.
**Day 2 — the model.** B1, B2, B3 — then Gate 1 below.
**Day 3 — evidence.** B5, M3, M4, M5, M6.
**Day 4 — figures and data section.** M9, the speed-model result, H7, H8.
**Day 5 — writing.** B6, M8, limitations, M10.

### 🚦 Gate 1 — do not generate a single paper number until all four hold

1. The objective value **differs** between the optimal solution and a feasible random one.
2. The equity constraint **binds** for some θ — tightening θ changes the solution or reports
   infeasibility for a reason involving the decision variables.
3. The α/β sweep produces **different** solutions at different weights.
4. The verification module's independent recomputation **agrees with the model's own reported
   values to 1e-6**.

Check 4 is the one that catches the defect class that has twice nearly sunk this project: a quantity
that looks optimised but is decoupled from the decision.
