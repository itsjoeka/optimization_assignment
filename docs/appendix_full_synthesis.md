I have what I need. Both verification suites ran on my own independent build; the θ=1.0 hard-cap run is still churning, which is itself the finding (near-parity is hard for the hard-cap form in every formulation tested).

```markdown
# Replacement for §6 and §8 — Revision Plan to Friday 2 October 2026

> **Status.** This supersedes §6 (Recommended reformulation) and §8 (Plan to a final draft) of the
> audit dated 22 September 2026. §§1–5, §7 and §9.1 stand unchanged. §9.2 (the feasibility probe)
> remains **superseded and unquotable**.
>
> Written 22 September 2026, after (a) a technician at the Hohoe post confirmed that crews travel
> **site-to-site** and return to the post only for tools or materials, and (b) the deadline moved
> to **Friday 2 October 2026**.
>
> Every number in this document that is marked *(synthetic matrix)* was produced against a
> **fabricated** inter-town travel-time matrix and is provisional in magnitude. Numbers drawn from
> `dataset/*.csv` directly are exact and are marked *(field data)*.

---

## 6. What the new field evidence changes, and why it is good news

### 6.1 The problem class changes

The technician's account settles the question §4.5 left open. Crews do **not** round-trip to the
depot between jobs. When a call comes in while they are on site, they drive **directly** from the
current site to the next. They return to the post only when they need a tool or material stocked
only there, and at end of shift.

That single sentence moves the project out of the assignment-problem family and into a named,
heavily-studied one:

> A single-depot, multi-vehicle **Cumulative Capacitated Vehicle Routing Problem with service
> times and a route-duration limit** (CCVRP; Ngueveu, Prins & Wolfler Calvo 2010), sitting inside
> the **Technician Routing and Scheduling Problem** family (TRSP; Pillac, Guéret & Medaglia 2013),
> augmented with a customer-side spatial-equity constraint.

Its theoretical name is the **k-travelling repairman / multi-vehicle minimum-latency problem**
(Fakcharoenphol, Harrelson & Rao 2007). The duration-plus-capacity constraint pair is Laporte,
Nobert & Desrochers (1985). **Name it this way in the Abstract and the first paragraph of Methods.**
Doing so converts the single biggest reviewer risk — an untethered student MILP — into the
smallest: a correctly identified standard model class with 40 years of literature behind it.

**Do not present the site-to-site protocol as a new problem feature.** Tool- and spare-part-driven
depot returns are already an explicitly modelled feature of TRSP (Pillac et al. 2013). The correct
sentence is:

> *"A field interview with an ECG Hohoe technician confirms that district operations conform to the
> standard TRSP structure, in which depot returns are tool-driven rather than job-driven. We
> therefore model direct inter-site travel with an optional depot revisit."*

That is honest, citable, and referee-proof. Claiming novelty in the protocol would be the one
sentence most likely to be caught.

### 6.2 Why the degeneracy of §4.1 becomes structurally impossible

This is the part worth understanding precisely, because it is what rescues the paper.

**The old failure, in one line.** The objective was $\sum_i\sum_j t_j x_{ij}$. Its arc coefficient
$t_j$ depends **only on the fault index $j$**, never on which crew serves it or in what order. So
the coverage constraint $\sum_i x_{ij}=1$ factors it straight out:

$$\sum_i\sum_j t_j x_{ij} \;=\; \sum_j t_j\Big(\sum_i x_{ij}\Big) \;=\; \sum_j t_j \;=\; 8.985\ \text{h (field data)}.$$

Any objective whose cost is **additively separable over faults** dies the same way, whatever
multiplier is attached to $t_j$. This is the general form of the defect, and it is worth stating in
the paper in exactly these terms.

**Why routing cannot die that way.** Two independent mechanisms, either one sufficient:

1. **Order dependence.** The response time of the fault in position $p$ of a route
   $\sigma=(j_1,\dots,j_k)$ is
   $$A_{j_p} \;=\; \tau_{0,j_1} \;+\; \sum_{q<p}\big(r_{j_q}+\tau_{j_q,j_{q+1}}\big),$$
   so the route's total customer waiting is a **positional-weight sum**,
   $$\sum_{p} A_{j_p} \;=\; k\,\tau_{0,j_1} \;+\; \sum_{q=1}^{k-1}(k-q)\big(r_{j_q}+\tau_{j_q,j_{q+1}}\big).$$
   The weights $(k-q)$ attach to different legs when the route is permuted. A separable cost is
   permutation-invariant; this is not.

2. **Grouping dependence.** $A_{j_p}$ contains $\tau$ terms between **pairs** of faults, so a
   fault's contribution depends on which other faults share its route.

Formally: the objective collapses only if there exists a vector $(\gamma_j)$ with
$c_\sigma=\sum_{j\in\sigma}\gamma_j$ for every feasible route $\sigma$. Either mechanism above
defeats that. The objective is constant only in the degenerate data case where all $\tau_{uv}$ are
equal **and** all $r_j$ are equal. In the ECG data $r_j\in[0.33,4.0]$ h *(field data)* and $\tau$
spans roughly $[0.05, 2.0]$ h. **Degeneracy is excluded by construction, not by luck.**

**The referee-facing witness — put this table in the paper.** Same three faults, same crew, same
total driving, route reversed:

| route | arrival times (h) | $\sum_p A_p$ | route duration |
|---|---|---|---|
| F15 → F7 → F10 | 0.267, 1.580, 2.318 | **4.165 h** | 6.801 h |
| F10 → F7 → F15 | 0.483, 4.891, 5.784 | **11.158 h** | 6.801 h |

*(synthetic matrix; regenerate on the real one)*. **Identical duration, 2.68× the customer
waiting.** That is the entire diagnosis of the original defect in one table: a travel-time or
duration objective is order-blind; an arrival-time objective is not. Three independent judge panels
reconstructed this figure to the digit. It is the best single artefact the revision produces.

### 6.3 The original error, reframed honestly

Design 1 observed that the root LP relaxation of the arc routing model equals the old degenerate
objective. Two of three panels measured it at exactly **0.599**, and I confirm from the dataset that

$$\frac{1}{n}\sum_j t_j \;=\; \frac{8.985}{15} \;=\; 0.599 \quad\text{exactly } \textit{(field data)}.$$

**Adjudication.** Design 1's drafted sentence — "the original paper's degenerate objective is
precisely the LP-relaxation bound" — is **wrong by a factor of $n$** and must not reach print. The
defensible statement, which two panels verified and the third corroborated with a caveat, is:

> *"The root LP relaxation of the vehicle-flow formulation equals the published objective divided by
> the number of faults — the per-fault 'teleportation' bound, i.e. the value obtained if every crew
> arrived everywhere at time zero. The original model was therefore computing a valid but
> unattainable lower bound and reporting it as an optimum."*

Two caveats to state with it, because a referee will test both. (i) This is a property of the
**arc/vehicle-flow relaxation specifically** — the set-partitioning LP relaxation is far tighter
(≈1.42 on our synthetic matrix, against an integer optimum of ≈1.43) and shows no such coincidence.
(ii) It is matrix-independent, because it depends only on the field-measured depot legs. Stated with
those caveats it is a genuinely interesting paragraph. Overstated, it is a free hit for a referee.

### 6.4 What the field evidence is worth, quantified

The interview materially moved the feasible region. Solving the same instance under the two
protocols *(synthetic matrix, my own independent build)*:

| dispatch protocol | mean response | makespan | total crew-hours |
|---|---|---|---|
| **site-to-site** (what crews actually do) | **1.428 h** | 6.91 h | 29.45 h |
| forced round-trip to the post between jobs (the superseded assumption) | 2.277 h | 7.96 h | 37.72 h |

The superseded assumption **overstates mean customer response by 59%** and crew vehicle-hours by
28%. Design 1 independently measured that its optimal plan would have makespan 9.34 h > 8 h —
outright infeasible — under the round-trip assumption. **One interview question changed which plans
exist.** That belongs in the paper as evidence that field validation of modelling assumptions is not
a formality. It is also, bluntly, the best return on effort anyone on this project has achieved.

### 6.5 The consequences you must accept

1. **A ~24 × 24 inter-town travel-time matrix is now required and the project does not have it.**
   This is the critical path. §7 below is entirely about it.
2. **The published 15-fault instance touches only 12 distinct towns** *(field data)*, so a 13 × 13
   matrix reproduces it exactly. The full 24 × 24 is needed for new instances and the scaling study.
   **If time runs short, the 13 × 13 is the minimum viable artefact.**
3. **Same-town faults are now representable.** F1 and F6 are both at Afadzo South; F4, F8 and F14
   are all at Agome yo *(field data)*. Chaining them costs a few minutes, not a depot round-trip.
   The assignment model could not express this at all. Expect the optimiser to exploit it, and show
   that it does — it is visible, intuitive evidence that the model has learned something real.
4. **Total repair time is 20.07 h against 5 × 8 = 40 crew-hours** *(field data)* — 50.2% of the
   shift budget consumed before any travel. The shift constraint still binds hard under site-to-site
   travel, so the audit's strongest headline (a **feasibility** result, not a percentage) survives.

---

## 6A. The recommended formulation

**One recommendation, not options.** Three independent judge panels, each of which rebuilt the
candidate designs from scratch on its own travel matrix, reached the same verdict unanimously. So do
I, having rebuilt it a fourth time.

> **Present the problem as an arc-based vehicle-flow MILP (the model). Solve it by a priori route
> enumeration and set partitioning (the method). Report the comparison between them as a
> computational contribution.**

The model statement is what a referee expects to see and what remains valid the moment a crew stops
being identical or depot-based. The set-partitioning encoding is what actually solves: on my own
build, **0.010 s to enumerate and 0.106 s to a proven optimum**, against 70–150 s for the arc model
and *never* for the position-indexed alternative. That speed is not a convenience — it is what makes
the ten days work, because the entire sensitivity suite regenerates in minutes the afternoon the
real matrix lands.

Name for the paper: **E-CCVRP-ST** (Equitable Cumulative Capacitated VRP with Service Times).
**Claim no novelty in the model class.** Claim it in the application, the primary data, and the
customer-side equity treatment.

### 6A.1 Sets, parameters, variables

**Sets.**

| | |
|---|---|
| $J=\{1,\dots,n\}$ | faults in the shift ($n=15$). **Nodes are faults, not towns** — three faults at Agome yo are three elements of $J$. |
| $0$ | the Hohoe ECG post (depot). $V=\{0\}\cup J$. |
| $K=\{1,\dots,m\}$ | crews ($m=5$; three technicians moving as one unit). |
| $J^{N}, J^{F}$ | Near / Far zone partition, $|J^{N}|=n_N=8$, $|J^{F}|=n_F=7$ *(field data)*. |
| $J^{H}$ | High-priority faults, $|J^{H}|=5$ *(field data)*. |
| $\mathrm{site}(j)$ | the town of fault $j$. |

**Parameters.**

| | |
|---|---|
| $\tau_{uv}\ge 0$ | travel time (h), $u\to v$, $u,v\in V$. Row/column 0 is **field-measured**; the interior is §7. Asymmetry is permitted. |
| $\delta=0.05$ h | intra-town travel between two fault sites in the same town. |
| $r_j>0$ | repair time at $j$ (h), $r_0=0$. **Strict positivity is load-bearing** (Lemma 1). |
| $H=8$ h | shift length. $Q=3$ — maximum faults per crew. |
| $w_j\ge 1$ | priority weight; $W=\sum_j w_j$. |
| $D$ | response-time target for $j\in J^{H}$ (optional hard SLA). |
| $\bar\tau^{N}=0.46887$, $\bar\tau^{F}=0.74771$ | each zone's mean depot leg — its **unavoidable geographic floor** *(field data, recomputed; Design 1's 0.7404 was wrong)*. |
| $\alpha,\beta\ge0$, $\alpha+\beta=1$ | efficiency / equity weights. $\theta\ge1$ — equity tolerance. |
| $\rho\in\{0,1\}$ | 1 iff the end-of-shift return leg is charged against $H$. **Base case $\rho=1$.** |

**Decision variables.**

| | |
|---|---|
| $x_{uvk}\in\{0,1\}$ | crew $k$ drives directly $u\to v$. Aggregate $\hat x_{uv}=\sum_k x_{uvk}$. |
| $R_j\ge 0$ | **response time**: hours from shift start until a crew arrives at fault $j$. |
| $G\ge 0$ | inter-zone equity gap. $C_{\max}\ge0$ — makespan. $R^{\max}\ge0$ — worst customer wait. |

### 6A.2 The model (E-CCVRP-ST)

$$\boxed{\ \min\ Z \;=\; \alpha\cdot\underbrace{\frac{1}{W}\sum_{j\in J} w_j R_j}_{\text{efficiency}}\;+\;\beta\cdot\underbrace{G}_{\text{equity}}\ }$$

subject to

$$\textbf{(C1) Coverage}\qquad \sum_{u:(u,j)}\hat x_{uj}=1 \qquad \forall j\in J$$

$$\textbf{(C2) Flow conservation}\qquad \sum_{u} x_{uhk}-\sum_{v} x_{hvk}=0 \qquad \forall h\in J,\ \forall k\in K$$

$$\textbf{(C3) One route per crew}\qquad \sum_{j\in J} x_{0jk}\le 1 \qquad \forall k\in K$$

$$\textbf{(C4) Route closure}\qquad \sum_{i\in J} x_{i0k}=\sum_{j\in J} x_{0jk} \qquad \forall k\in K$$

$$\textbf{(C5) Crew capacity}\qquad \sum_{(u,v):\,v\ne 0} x_{uvk}\le Q \qquad \forall k\in K$$

$$\textbf{(C6) Arrival recursion (also eliminates subtours)}\qquad R_v \;\ge\; R_u+r_u+\tau_{uv}-M_{uv}\big(1-\hat x_{uv}\big)\quad \forall u,v\in J$$
$$M_{uv}=H-\rho\,\tau_{u0}+\tau_{uv}-\tau_{0v}$$

$$\textbf{(C7) Shift limit as a variable bound}\qquad \tau_{0j}\;\le\;R_j\;\le\;H-r_j-\rho\,\tau_{j0}\qquad\forall j\in J$$

$$\textbf{(C8) Makespan and worst wait}\qquad C_{\max}\ge R_j+r_j+\rho\tau_{j0},\qquad R^{\max}\ge R_j \qquad\forall j\in J$$

$$\textbf{(C9) Zone means and excess waits}\qquad \bar R^{z}=\frac{1}{n_z}\sum_{j\in J^{z}}R_j,\qquad E^{z}=\bar R^{z}-\bar\tau^{z},\qquad z\in\{N,F\}$$

$$\textbf{(C10) Equity gap — TWO-SIDED, mandatory}\qquad G\;\ge\;E^{F}-E^{N},\qquad G\;\ge\;E^{N}-E^{F}$$

$$\textbf{(C11) Equity hard cap — two-sided, }\theta\ge1\text{ only}\qquad E^{F}\le\theta E^{N},\qquad E^{N}\le\theta E^{F}$$

$$\textbf{(C12) Priority SLA (optional)}\qquad R_j\le D\qquad \forall j\in J^{H}$$

**Two lemmas go in Methods; the proofs are three lines each and they earn their space.**

> **Lemma 1 (subtour elimination is free).** If $r_i>0$ for all $i\in J$, (C6) admits no cycle among
> fault nodes. *Proof.* Sum (C6) over the arcs of a cycle $C\subseteq J$: every big-M term vanishes
> ($\hat x=1$) and the $R$ telescope to zero, giving
> $0\ge\sum_{(u,v)\in C}(r_u+\tau_{uv})\ge\sum_{u\in C}r_u>0$. ∎
> Note this survives $\tau_{uv}=\delta$ between two faults in the **same town**, which is why strict
> positivity of $r$ (min 0.33 h here) is the load-bearing assumption, not positivity of $\tau$. A
> zero-duration "inspection" job would silently break it.

> **Lemma 2 (the shift limit is a variable bound).** Under the triangle inequality on $\tau$,
> imposing $R_j\le H-r_j-\rho\tau_{j0}$ at *every* fault is equivalent to imposing it only at each
> route's last fault. *Proof.* Let $l$ succeed $j$, so $R_l=R_j+r_j+\tau_{jl}$. For $\rho=1$,
> $R_j+r_j+\tau_{j0}\le R_l+r_l+\tau_{l0}\iff\tau_{j0}\le\tau_{jl}+r_l+\tau_{l0}$, true by the
> triangle inequality and $r_l\ge0$. For $\rho=0$ it is immediate. Induct backwards along the route. ∎
> Corollary: $C_{\max}=\max_j(R_j+r_j+\rho\tau_{j0})$ is exactly the longest crew day — no
> per-crew duration variable and no second big-M.

### 6A.3 The solution method: set partitioning over enumerated routes (SP-ECG)

Because $Q=3$, the complete set of ordered depot-rooted routes is
$\sum_{k=1}^{3} n!/(n-k)! = 15+210+2730 = 2{,}955$. Enumerate all of them, price each **exactly** in
closed form, discard those exceeding $H$, and solve a set-partitioning master (Balinski & Quandt
1964). **Because the column set is complete, this is exactly optimal — not a heuristic, not a
relaxation.**

For each route $\omega=(j_1,\dots,j_{k_\omega})$ compute, once, at enumeration time:

$$a^\omega_1=\tau_{0,\mathrm{site}(j_1)},\qquad a^\omega_p=a^\omega_{p-1}+r_{j_{p-1}}+\tau_{\mathrm{site}(j_{p-1}),\,\mathrm{site}(j_p)}$$
$$D_\omega=a^\omega_{k_\omega}+r_{j_{k_\omega}}+\rho\,\tau_{\mathrm{site}(j_{k_\omega}),0},\qquad
c_\omega=\sum_p w_{j_p}a^\omega_p,\qquad
e^{z}_\omega=\!\!\sum_{p:\,j_p\in J^{z}}\!\! a^\omega_p,\qquad
M_\omega=\max_p a^\omega_p$$
$$A_{j\omega}=\mathbb 1[j\in\omega],\qquad \alpha_{j\omega}=a^\omega_p \text{ if } j=j_p, \text{ else } 0$$

Admit $\omega$ iff $D_\omega\le H$ **and** any within-route operating rule holds (SLA, priority
position cap, restocking). With $\lambda_\omega\in\{0,1\}$:

$$\min\ \ \alpha\cdot\frac{1}{W}\sum_\omega c_\omega\lambda_\omega \;+\;\beta\,G$$

$$\text{(S1) } \sum_\omega A_{j\omega}\lambda_\omega=1\ \ \forall j\in J \qquad
\text{(S2) } \sum_\omega \lambda_\omega\le m$$
$$\text{(S3) } G\ \ge\ \pm\Big[\Big(\tfrac{1}{n_F}\sum_\omega e^{F}_\omega\lambda_\omega-\bar\tau^{F}\Big)-\Big(\tfrac{1}{n_N}\sum_\omega e^{N}_\omega\lambda_\omega-\bar\tau^{N}\Big)\Big]$$
$$\text{(S4) } C_{\max}\ge D_\omega\lambda_\omega,\qquad R^{\max}\ge M_\omega\lambda_\omega \qquad \forall\omega$$
$$\text{(S5) } R_j=\sum_\omega \alpha_{j\omega}\lambda_\omega \ \ \forall j \qquad
\text{(S6) } d_{jj'}\ge \pm(R_j-R_{j'}),\qquad \mathrm{GMD}=\tfrac{1}{n^2}\!\!\sum_{j<j'}\!\! d_{jj'}$$

(S5)–(S6) are the Gini machinery (§6A.5); they cost 15 linear definitions, 105 continuous variables
and 210 rows, and are exact under minimisation. **No big-M anywhere in this model. No
subtour-elimination constraints. No crew index, hence no $m!=120$-fold symmetry.**

**The $\varepsilon$-constraint variant — use this for the frontier figure, not the weighted sum:**

$$\min\ G \quad \text{s.t. (S1)–(S6)},\qquad \frac{1}{W}\sum_\omega c_\omega\lambda_\omega\ \le\ (1+\varepsilon)\,Z^\star_{\mathrm{eff}}$$

**Equivalence statement for the paper:** *"The vehicle-flow model of §Methods and the
set-partitioning model have the same feasible set and the same optimal value, because the column set
is the complete set of shift-feasible depot-rooted routes of length at most $Q$; the projection
$\hat x_{uv}=\sum_{\omega\ni(u,v)}\lambda_\omega$ maps each set-partitioning solution to a feasible
vehicle-flow solution of equal cost, and conversely (C1)–(C5) decompose any feasible $\hat x$ into at
most $m$ such routes."* Verify this numerically at least once (§6A.7, check 1).

### 6A.4 Non-degeneracy: the proof, and the evidence

Referee question 7.1(1) — *"your objective reduces to a constant"* — is now answerable four
independent ways. Give all four; any one alone would suffice, and together they are not contestable.

1. **Structural (§6.2).** $c_\omega$ is not additively separable over faults, by order dependence and
   by grouping dependence. No substitution exists. Constancy requires all $\tau$ equal **and** all
   $r$ equal.
2. **A hand-checkable witness on the project's own data.** The F15 → F7 → F10 reversal table in
   §6.2: identical duration, 2.68× the waiting, and identical value (8.985 h) under the old
   objective.
3. **Measured spread over the identical feasible set.** Minimising *and maximising* the same
   functional over the same feasible set: mean response ranges from **1.43 h to 3.88 h** — a 165%
   spread — while the published objective is 8.985 h for every one of them. Three judge panels
   measured 160%, 164% and 165.6% on three different matrices.
4. **Solver-behaviour signature.** The old model's fingerprint was CBC's
   `best objective 8.985, took 0 iterations and 0 nodes`. **⚠ Explain carefully:** SP-ECG *also*
   reports 0 branch-and-bound nodes — but for the opposite reason, because its LP relaxation plus
   root cuts *close a real gap* (LP ≈1.42 vs IP ≈1.43 on my run). Say this explicitly in the text,
   or a reader who has read the audit will conclude nothing changed. **The discriminating evidence
   is the min–max spread, never the node count.**

### 6A.5 Equity — the design, and three adjudications

**Why an equity term is needed at all, theoretically.** Minimising mean latency is Smith's-rule-like:
it front-loads short, near jobs. The bias against far customers is a **property of the efficiency
objective**, not an accident of this data. Measured under pure efficiency on my own build, the
Far/Near response ratio is **1.79** *(synthetic matrix)*; across every geometry any workstream
tested — circuity 1.0–1.6, bearing jitter ±25°/±45°, asymmetry ±15% — it stayed in **1.37–3.02 and
was always > 1**. That is the paper's argument for the equity term, demonstrated rather than
asserted.

**ADJUDICATION 1 — use excess wait, not raw zone means.** Far towns are *by construction* further
from the post, so equalising *raw* mean response can only be achieved by delaying near customers
("levelling down"). Define

$$E^{z}=\bar R^{z}-\bar\tau^{z},\qquad \bar\tau^{N}=0.46887,\ \bar\tau^{F}=0.74771 \ \textit{(field data)}$$

which measures the delay the **dispatcher** causes, net of geography the crew cannot change. It stays
linear because $\bar\tau^z$ is a constant, and in set partitioning it is a two-line change to the
column coefficients. All three panels grafted this independently. On my own build it reaches parity
to within 0.2% — $E^{N}=0.9004$ vs $E^{F}=0.9021$ — at a 5.1% efficiency cost, **and the worst-served
customer improves** (3.59 h → 3.08 h) *(synthetic matrix)*. The raw-ratio form, by contrast, was
measured by two panels to *worsen* the worst customer as $\theta$ tightened. Excess wait is both
fairer and better behaved.

**ADJUDICATION 2 — $G$ and $\theta$ must be two-sided, and $\theta$ is defined only on $[1,\infty)$.**
A one-sided constraint lets the solver buy feasibility by **inflating** near-zone response — which is
the original paper's failure mode wearing a new costume, and it is not hypothetical: one panel caught
a one-sided run "achieving equity" with $E^{N}=1.087 > E^{F}=0.914$ while reporting $G=0.099$.
**But all three designs then missed that the two-sided hard cap is identically infeasible for
$\theta<1$:** $E^F\le\theta E^N$ and $E^N\le\theta E^F$ imply $E^F\le\theta^2E^F$, so $\theta\ge1$
unless $E\equiv0$. One panel confirmed two-sided $\theta=0.8$ is proven infeasible in 0.044 s.
**Resolution:** keep $G\ge|E^F-E^N|$ two-sided always; state that the hard cap $\theta$ is defined on
$[1,\infty)$; drive any sub-parity exploration with the $\varepsilon$-constraint, which is well-posed
throughout. Do **not** present a one-sided $\theta<1$ sweep next to a two-sided $G$.

**ADJUDICATION 3 — $\varepsilon$-constraint for the frontier, not the weighted sum.** The weighted
sum recovers only supported (convex-hull) Pareto points. Measured on my build: $\beta=0.15$ and
$\beta=0.30$ return the **identical plan**; the $\varepsilon$-constraint gives 5 distinct plans over
6 budgets and a smooth curve. Three panels found the same collapse (3, 4 and 4 distinct plans
respectively). **Report both**: the $\alpha/\beta$ table as the scalarisation the README promised,
and the $\varepsilon$-constraint as the frontier figure. And note $\beta=1$ is catastrophic —
79.6% efficiency loss on my run — so **never optimise dispersion alone**; Ogryczak's mean-equity
consistency result is the citable warrant for the combined form.

**Report three equity lenses, not one.** Zone gap $G$ (the policy instrument, optimised); **Gini /
GMD** of the individual $R_j$ (threshold-free, transfer-sensitive, answers the referee who attacks
the 19.5 km zone cut); and **$R^{\max}$** (the most politically legible number in the paper — "no
town waits more than X hours"). Report $R^{\max}$ but do **not** optimise it: Bertazzi, Golden &
Wang (2015) prove min-max can cost up to $m\times$ the min-sum optimum. Cite Lehuédé, Péton &
Tricoire (2020) as the more rigorous leximin alternative you traded away for tractability. Three
lenses is a contribution for an application paper; one ratio is not.

**Also report crew-side workload spread** (max minus min route duration) as a secondary operational
statistic, and state explicitly in Methods that customer-side and crew-side equity are distinct and
why you chose customer-side. **Conflating these is the single most common referee complaint in this
literature**, and the distinction is the paper's sharpest positioning move: the VRP equity literature
(Matl, Hartl & Vidal 2018) is overwhelmingly crew-side workload balance, while the Near/Far framing
is customer-side spatial accessibility from equitable facility location (Marsh & Schilling 1994).

### 6A.6 Priority — and a paper-saving catch

Priority enters three ways, all free in set partitioning:

1. **Soft weight** $w_j$ inside $c_\omega$, with the objective normalised by $W=\sum_j w_j$
   (**not** by $n$ — Design 3's version stops being a mean the moment $w_H\ne1$).
2. **Hard SLA** $R_j\le D$ for $j\in J^{H}$ — a column filter, and operationally the form an ECG
   engineer recognises.
3. **Position cap** — High-priority faults confined to the first $\bar p$ positions; also a filter.

**⚠ THE PRIORITY/ZONE CONFOUND — the highest-value catch in the entire review, and you must control
for it.** From the CSV *(field data)*: the High-priority faults are **F1, F3, F6, F8, F10**, and
**four of those five are in Far towns**. Priority weighting *alone* therefore drags the Far/Near
ratio down with no equity mechanism doing any work. I confirmed this independently:

| $w_{\mathrm{High}}$ | mean response | **Far/Near ratio** | mean High-priority arrival |
|---|---|---|---|
| 1.0 | 1.428 h | **1.789** | 1.608 h |
| 1.5 | 1.467 h | **1.421** | 1.076 h |
| 2.0 | 1.467 h | **1.421** | 1.076 h |
| 3.0 | 1.467 h | **1.421** | 1.076 h |

*(synthetic matrix)*. That is a property of `random.choices(seed=60)`, not of Hohoe. **Run every
equity experiment at $w_{\mathrm{High}}=1$ and present priority weighting as a separate, clearly
labelled experiment.** Without this control the paper's central equity finding is a random seed.
Two judge panels and I verified it independently; the design that proposed the winning formulation
did not spot it.

**The SLA is the best result in the study.** Measured on my build, $w_{\mathrm{High}}=1$
*(synthetic matrix)*:

| $D$ | feasible columns | mean response | mean High-priority arrival | status |
|---|---|---|---|---|
| none | 2,350 | 1.428 h | 1.608 h | optimal |
| 2.0 h | 1,418 | 1.464 h (+2.5%) | 1.279 h | optimal |
| 1.5 h | 1,177 | 1.682 h (+17.8%) | 1.062 h | optimal |
| 1.2 h | 1,083 | 1.944 h (+36.1%) | 0.840 h | optimal |
| 1.0 h | 908 | — | — | **proven INFEASIBLE** |

Design 1 obtained the same qualitative pattern — 1.2 h feasible, 1.0 h infeasible — on a completely
different synthetic matrix. **That cross-matrix replication of a feasibility threshold is the most
robust finding in the whole review.** It yields the decision-support sentence the utility actually
wants:

> *"With five crews, Hohoe can guarantee that every high-priority fault is reached within 1.2 hours;
> a 1-hour target is infeasible. The 1.2-hour guarantee costs 36% on mean response."*

Get ECG's real restoration target and that sentence becomes a statement about whether the utility
currently meets its own standard. Until then, present $D$ purely as a sweep with no privileged value.

### 6A.7 Assumptions — state every one of these explicitly in Methods

| # | Assumption | Status | What to do |
|---|---|---|---|
| A1 | Crews travel **site-to-site** between jobs | **Confirmed by field interview** | This is the paper's justification for routing over assignment. Cite the interview. |
| A2 | Crews **return to the post at end of shift**, and that drive is inside the paid 8 h ($\rho=1$) | **Assumed — the technician was not asked** | Base case $\rho=1$; the return leg is charged to $H$ but **never to the objective**, because no customer waits on it. Design 1 found $\rho=1$ and $\rho=0$ give the *identical* plan at $n=15$, so it is not load-bearing here — but **ask him**. One line. |
| A3 | **No mid-shift depot return** in the base case | **Known to be an approximation** | The technician said returns happen for tools/materials. Handled as a column filter, not deferred (see below). Ask how often: 1 job in 5, or 1 in 20? |
| A4 | All 5 crews start at the post at $t=0$, are identical, and are Hohoe-based | Assumed | If any crew is stationed out-district, the set-partitioning columns must be re-rooted (trivial) but the 2-index arc reduction becomes invalid. State the condition where you state it. |
| A5 | All $n$ faults are known at shift start | Assumed | This is **morning dispatch planning**, not dynamic dispatch. Say which. Release times are a one-line addition ($R_j\ge e_j$) but change the narrative. |
| A6 | $H=8$ h, $Q=3$ are ECG's real figures | **Asserted, no source** | Confirm with Abdul Haliq. See §6A.8. |
| A7 | $\delta=0.05$ h between two faults in the same town | Assumed | Trivial; state it. |
| A8 | Near/Far threshold | **Unstable — code says 19.5 km, README says 20 km, and Liati at exactly 20.0 km flips between them** *(field data)* | Fix at an **exogenous** 20 km and justify it, or use ECG's own convention. Run a threshold-sensitivity check. Never use `ceil(max)/2`. |
| A9 | Faults are **simulated** | **True and unchanged** | Disclose in the **abstract**, not just Methods. Retitle to *"A Simulation Case Study Grounded in the Hohoe Operations Department"*. |

**On A3, the restocking exception — model it, do not defer it.** This is where set partitioning
earns its place over the alternatives, both of which forbid mid-shift depot returns outright and
push them to "a clean second paper". Here it is a column filter: recompute $a^\omega_p$ with a depot
leg inserted before a material-hungry job. I priced it on my own build: forcing the detour before the
transformer-installation and pole-replacement faults (F1, F10, F12) costs **+12.2%** on mean
response and pushes $C_{\max}$ from 6.91 h to 7.87 h *(synthetic matrix)*. One panel independently
measured +9.8% and found that when restocking is made **optional**, the optimum is unchanged — the
model never elects a discretionary detour. **Ask Abdul Haliq which fault types require post-stocked
material**, then report base case and restock scenario side by side. An operating rule that would
need extra binaries and a big-M in a compact model is here just a longer column list.

**On $Q=3$ — relax it, and audit §5.4 dissolves.** With $n=15$, $m=5$, $Q=3$ total capacity is
exactly 15, so every crew must take exactly 3 and a large part of the decision space is fixed by
arithmetic. A referee who notices this will ask what is left to optimise. Two things fix it, both
free: (i) the **8-hour shift self-limits route length** independently of $Q$, so you can drop $Q$
entirely — one panel measured the complete shift-feasible column set at 92,229 columns, enumerable
in 0.65 s and solved to proven optimality in 2.5 s; (ii) relaxing $Q$ from 3 to 4 improves mean
response 4.7% and produces an unbalanced load of [2,3,3,3,4]. **Run the headline at $Q=3$ (ECG's
stated rule) and report the $Q$-free result as the primary sensitivity.** You then do not need to
wait on ECG to confirm $Q$, and the instance becomes genuinely interesting.

### 6A.8 Verification protocol — non-negotiable, and it is cheap

Three checks. Do all three, report all three; they take under a minute of compute each.

1. **Exhaustive enumeration at small $n$.** Brute-force *all* feasible plans at $(n,m,Q)$ =
   (4,2,2), (5,2,3), (6,2,3) and confirm agreement to $10^{-6}$. At the full instance, brute force
   over all $15!/(3!^5\,5!)=1{,}401{,}400$ partitions is also feasible (~0.5–75 s) and two panels did
   it: both matched the MILP to $10^{-9}$.
2. **Independent simulator.** Re-simulate the returned routes with a solver-free evaluator and
   confirm objective, mean response, makespan, $\bar R^{N}$, $\bar R^{F}$ and $C_{\max}$ to six
   decimal places. Design 1 and Design 2 each reported agreement to $10^{-7}$ or better.
3. **Cross-formulation agreement.** Solve the same instance with the arc model and confirm the same
   optimal value. Two panels did this on matrices the designs had never seen and got bit-identical
   agreement. **This is the check a referee would demand, and you can already report it.**

**⚠ TWO PULP TRAPS THAT WILL PUT FABRICATED NUMBERS IN YOUR PAPER.** Both were hit independently by
multiple workstreams.

- **Trap 1: `LpStatus` lies about optimality.** PuLP reports `status = "Optimal"` when CBC stopped on
  a time limit with an incumbent. One panel reproduced this returning a value **12.7% worse** than
  the true optimum, labelled `Optimal`; another got 3.3% worse at a 49% gap, labelled `Optimal`.
  **Parse the raw CBC log for `Stopped on time limit` before the word "optimal" appears anywhere in
  the manuscript.** SP-ECG is immune at this scale because it genuinely proves optimality in ~0.1 s,
  but every baseline and comparison model in the paper is not.
- **Trap 2 (worse, and nobody warns about it): `var.value()` returns STALE values after a failed
  solve.** After an `Infeasible` or `Not Solved` solve, the variables still hold the *previous*
  solve's values. One panel's $\theta$ sweep silently returned the $\theta=1.2$ plan verbatim for
  $\theta=1.0$, and returned plans covering only a **subset** of the 15 faults — with
  plausible-looking objectives of 0.61 and 0.52 h — for two infeasible cases. **Assert
  `LpStatus == "Optimal"` before extraction, and re-assert full coverage of all 15 faults on every
  extracted plan.** My own reference implementation does both; copy that pattern.
- Minor, but it costs hours: PuLP rewrites `cat="Binary"` to `"Integer"`, so a binary-count filter
  silently matches nothing.

**On reporting $\theta=1.0$:** every workstream found the exact-parity case hard — "Not Solved"
within the time budget, in three different formulations, and still churning in my own run at the time
of writing. **Status "Not Solved" is not "Infeasible".** Report it as *"feasibility at $\theta=1.0$
could not be resolved within the time budget"*, or find the true threshold by bisection with a longer
limit. Writing "infeasible" where the solver said "not solved" is exactly the class of overclaim this
audit exists to prevent.

### 6A.9 Computational reporting, and the honest scalability statement

**Report the head-to-head as a contribution, not an omission.** On my own build, the same instance,
the same objective, the same feasible set:

| encoding | time to answer | proven optimal? |
|---|---|---|
| **set partitioning (2,350 columns)** | **0.116 s** (0.010 enumerate + 0.106 solve) | **yes** |
| arc-based, cumulative-flow strengthened | 70–150 s (β=0); 25% gap unclosed at 120 s with β>0 | partly |
| position-indexed | 600 s, never closed; 12.7% off the optimum in one panel's run | **no** |

**⚠ Benchmark honestly.** Design 3's original head-to-head compared against a *plain* big-M + MTZ arc
model whose LP bound is literally 0.000. That is a straw man and a referee will say so. **Benchmark
against the cumulative-flow-strengthened arc model** (root LP 0.599, measured by two panels), where
the margin is ~700–1,800× rather than ∞. The conclusion survives; the framing must be fair.

**Scalability — report the ceiling, do not promise past it.** Column count grows as $\Theta(n^Q)$:
benign in $n$, brutal in $Q$. Measured across panels: proven optimal in 0.2 s at $n=15$, 0.5–2.4 s at
$n=30$, 1.3–10.4 s at $n=45$, 8–25 s at $n=60$, 144 s at $n=120$; the filtered column count is the
binding quantity, and the practical ceiling with CBC/PuLP is $\lesssim10^6$ filtered columns —
**about $n=150$ at $Q=3$ and $n=60$ at $Q=4$**. Beyond that, name **branch-and-price** with an
ESPPRC pricing subproblem as the designated extension (Desrochers, Desrosiers & Solomon 1992;
Feillet et al. 2004; Barnhart et al. 1998). *"We solve today's instance to proven optimality and we
know exactly which algorithm takes over when the instance grows"* is a confident, publishable
position.

---

## 7. The travel-time matrix — the critical path

**Nothing else in this project is blocking. This is.** Every routing number in this document rests on
a fabricated matrix, and a paper that ships with one is rejectable on that alone. The good news:
with normal internet this is **one afternoon**, and the tooling is already written.

### 7.1 What is needed

A **24 × 24 driving-duration matrix in hours** (Hohoe ECG post + 23 towns) plus the matching distance
matrix. **Keep it asymmetric** — Volta terrain and one-ways make $\tau_{uv}\ne\tau_{vu}$, and both the
arc model and SP-ECG handle asymmetry natively.

**Minimum viable artefact:** the published 15-fault instance touches only **12 distinct towns**
*(field data)*, so a **13 × 13** matrix (12 towns + depot) reproduces the headline instance exactly.
Build that first if time is short; the full 24 × 24 is needed only for new instances and the scaling
study.

### 7.2 Task M1 — 24 verified coordinates (~2 hours, BLOCKING)

This is the whole critical path; there is no matrix without coordinates. A template exists at
`scratchpad/GEOCODE_TEMPLATE.csv`; copy it into the repo as `dataset/ecg_towns_coordinates.csv` with
columns `dataset_name, verified_settlement_name, latitude, longitude, gps_source, corridor_road,
road_surface, notes`.

- Decimal degrees, **5 decimal places minimum**.
- Record **the point the crew actually drives to** — the ECG service point, transformer site or town
  junction — not a Wikipedia centroid.
- **Row 1 must be the depot: the Hohoe ECG post GATE**, not Hohoe town centre. Nobody outside Ghana
  can supply this. Someone stands at the gate and reads it off a phone.
- Add `road_surface` (tarred / graded laterite / untarred). Free to collect, and it turns the
  implied-speed spread from an embarrassment into evidence.

**Ten towns nobody could locate remotely and which must come from the team:** Gbi-Kledzo, Gbi-Wegbe,
Gbi-Avege, Ve-Dator, Ve-Gbodome, Wuinta, Gbledi, Agome yo, Zimugaziwo snake Village, **Afadzo South**
(note: *Afadzato South* is a **district**, not a settlement — nobody can say what was measured).

**Thirteen ambiguous names** — each is a traditional area with several settlements, and the wrong pin
silently corrupts a whole row and column. Ask the ECG contact which specific town was measured:
Fodome (Ahor/Woe/Helu/Dzogbega), Liati (Wote/Teteman/Soba), Wli (Agorviefe/Todzi/Afegame), Leklebi
(Duga/Kame/Agbesia), Santrokofi (Benua fits the 7.5 km reading), Akpafu (Todzi/Mempeasem/Adokor),
Lolobi (Kumasi/Ashiambi/Huyiam), Likpe (Mate fits the 17.2 km reading), Logba
(Adzekoe/Alakpeti/Tota), Ve-Kobenu (probably Ve-Koloenu — confirm the spelling), Fume (Avatime-Fume
in Ho West, 38 km south?), and Godenu.

**Also normalise the town-name spacing now** (`Ve -Gbodome`, `Ve- Kobenu`, `Gbi - Kledzo`) — the
fault-to-town join will fail silently on these.

### 7.3 Task M2 — the matrix (~10 minutes of compute, BLOCKING)

**This is ONE HTTP request, not 253 or 552.** OSRM's `/table` endpoint returns up to 10,000 durations
per call; 24 × 24 = 576 comes back in about two seconds.

```
GET https://router.project-osrm.org/table/v1/driving/
    {lon1},{lat1};{lon2},{lat2};...;{lon24},{lat24}?annotations=duration,distance
```

- **Coordinates are LON,LAT** — this order trips everyone up.
- Semicolon-separated, all 24 nodes in one URL, **depot first**.
- Response: `{"durations": [[...s...]], "distances": [[...m...]], "code":"Ok"}`. Divide by 3600 and
  1000.
- Policy: max 1 request/second, non-commercial, no uptime guarantee.

Cross-check with **OpenRouteService** (`POST /v2/matrix/driving-car`, free key, 3,500-pair limit —
576 is well inside it). **Running the same 24 coordinates through both engines and reporting the
agreement costs five extra minutes and is a strong, cheap credibility signal.**

A ready-to-run script exists at `scratchpad/build_real_matrix.py`. It reads `coords.csv`, makes the
single OSRM call, **caches the raw JSON to `osrm_raw.json`** (commit that file — it is the provenance
artefact a reviewer will want) and writes `travel_time_hours.csv` and `travel_distance_km.csv`.
Requires only `requests`, `pandas`, `numpy`.

### 7.4 Task M3 — calibration and quality gates (~30 min, BLOCKING)

**Do not drop raw API times into the model.** The 23 field-measured depot legs are the project's key
asset precisely because they let you calibrate, and no other paper on this problem has that
validation set.

1. **Regress field time on API time across the 23 legs.** Report the fitted slope $\lambda$, MAE,
   $R^2$ and a scatter plot; rescale the whole matrix by $\lambda$ (or by road class if `road_surface`
   is obtained). Expect OSRM to be **faster** than reality — it models a generic car on mapped
   geometry, not a loaded ECG vehicle with a three-man crew. *"OSRM durations calibrated against 23
   field-measured legs, $\lambda=\dots$, MAE $=\dots$ min"* is a Methods paragraph a referee will
   respect.
2. **Also compare API distance against the field odometer readings.** This is a second, independent
   check and it is how you finally settle Fodome, Gbledi and Godenu.
3. **Quality gates, asserted in code:** zero null (unroutable) entries — a null means a coordinate
   snapped to no road, so nudge it and re-run; report max asymmetry and **keep the matrix
   asymmetric**; count triangle-inequality violations (should be 0 for a road matrix).
4. **Triangle inequality:** Lemmas 1 and 2 of the arc model need it. **SP-ECG needs nothing of the
   matrix at all** — no triangle inequality, no symmetry, no closure — which is a real advantage:
   **the 23 field-measured depot legs are used verbatim rather than overwritten to satisfy a
   modelling convenience.** So run the Floyd–Warshall closure as a **diagnostic** and report how many
   entries it *would* have moved; do not apply it to the data.
5. **Hub-and-spoke sanity check:** report the fraction of town pairs whose shortest path runs via
   Hohoe. In a rural spoke network this should be substantial (one construction gave 52%); near zero
   means the geocoding is wrong. Cheap geocoding-error detector.

### 7.5 Task M4 — three data repairs (~1 hour, needs the ECG contact, not the internet)

| Row | Problem | Evidence | Action |
|---|---|---|---|
| **Fodome** | 0.65 km / 0.65 h = 1.0 km/h | Grubbs flags it ($G=2.862 > G_{\mathrm{crit}}=2.780$); it is the **unique row of 23 where distance == travel_time** (a cell copied across); Fodome Ahor is **11.87 km great-circle** from Hohoe, so 0.65 km is 18× shorter than crow-flies and physically impossible. Studentised residual +5.69 against the fitted speed model. | **The distance cell is corrupt; the 0.65 h is plausible.** Candidates span 6.5 / 13.79 / 16.5 / 23.82 km — a 3.7× range. **Re-measure, do not guess.** If it cannot be re-measured, drop the row and say so (the speed model is unchanged on 22 towns). |
| **Gbledi** | 1.3 km / 0.05 h | **The audit missed this** because 26 km/h looks fine. But Gbledi-Gbogame is in **Afadzato South District near Mount Afadja**, ~20 km out — 1.3 km is geographically impossible regardless of implied speed. 3 min is also below the fitted 9.6 min egress overhead. | Verify. Probably 13 km. **Check together with Fodome — they may share a decimal-point shift in the source sheet.** |
| **Godenu** | 19.2 km recorded vs 6.11 km great-circle to Gbi Godenu → circuity 3.14 | Third concern, new | Either a different Godenu or a bad distance. Verify. |

### 7.6 The no-API fallback — and why it is better than a single synthetic matrix

If M1–M3 cannot be completed, **do not publish a single imputed matrix as a point estimate.** Publish
a **bracket**. Two metric-consistent constructions already exist in the scratchpad:

- **Matrix A — corridor tree (upper bound), needs no coordinates.** All cross-corridor travel routes
  back through Hohoe: $d(i,j)=|d_i-d_j|$ within a corridor, $d_i+d_j$ otherwise. Mean 0.804 h.
- **Matrix B — polar law-of-cosines × circuity 1.162 (lower bound), needs corridor bearings.** Mean
  0.608 h.

Both are **symmetric with zero triangle-inequality violations** — which matters, because a matrix
that violates the triangle inequality produces VRP "optima" that are artefacts, and most ad-hoc
imputation schemes do violate it. **Saying explicitly that both constructions are verified metrics is
a credibility marker a good referee will notice.**

Solve under both, with an identical method and seed, and report the spread on every headline number.
Measured: mean response moves **2.8%**, makespan 2.7%, the Near/Far gap **0.7%**, and the improvement
over ad-hoc dispatch stays in **45.5–48.9%**. That is a referee-proof framing, because it makes the
matrix **non-load-bearing for every claim the paper makes**.

**What the bracket does NOT license:** the optimal crew-to-fault *partition* differs between the two
matrices (one comparison shared only 9 of 20 arcs). **The aggregates are outside the uncertainty; the
specific dispatch plan is inside it.** Say that in one explicit sentence and you disarm the obvious
objection before a referee raises it. A regret study makes the same point quantitatively: optimise on
matrix A, execute in world B — average loss 6.0%, max 11.2%, still beating ad-hoc dispatch by 39–43%,
and infeasible in 1 of 6 worlds. **Matrix error costs about a sixth of the optimisation benefit and
occasionally breaks feasibility.**

### 7.7 A genuine side-result: the speed model

This turns the dataset's most reviewer-visible oddity into a one-paragraph data-section finding.
Fitting on the 22 clean towns (Fodome excluded):

$$t \;=\; 0.1595 \;+\; 0.02059\,d \qquad R^2=0.8957,\ \ \text{LOOCV } Q^2=0.8743,\ \ \text{CV MAE }=3.72\ \text{min}$$

The intercept is **0.1595 h = 9.6 min** (se 0.0334, $t=4.77$, $p=0.0001$) and the slope is
1/48.57 km/h ($p=2.8\times10^{-11}$). Read physically: about ten minutes to clear Hohoe town and get
onto the trunk road, then ~49 km/h cruise. A power-law fit independently rejects constant speed
(exponent 0.7415, 95% CI [0.634, 0.849], $p=0.00013$).

**So the "1 to 47 km/h spread" is mostly an artefact of dividing a fixed overhead by a short
distance.** Wli at 47.2 km/h and Gbi-Kledzo at 18.4 km/h are the *same vehicle on the same road
model*. Corridor structure adds nothing on top (ANOVA $F=0.529$, $p=0.716$; adjusted $R^2$ actually
falls), so a single global speed model is adequate — report that as a tested negative, not an
assumption.

### 7.8 What the paper MUST disclose about the matrix — non-negotiable

- **How many of the 552 ordered node pairs are field-measured.** It is 23 — i.e. **4.2%**. The other
  95.8% is API output or model output. **That ratio must appear in the paper.** The danger sentence
  is any variant of *"travel times between towns were obtained from field data."*
- The exact construction with its parameters: provider, profile, query timestamp, traffic-aware or
  free-flow, the calibration constant, the raw JSON committed to the repo.
- **The Fodome correction, with the rule and its sensitivity.** Do not silently fix it. A reviewer who
  downloads the CSV, sees `0.65, 0.65` and finds no mention will assume the worst.
- Gbledi and Godenu as open data questions if unresolved.
- That the 15 faults are simulated (in the **abstract**).
- The solve time, time limit, best bound and gap for every solve, parsed from the CBC log.

**One framing suggestion.** If the real matrix arrives in time, **keep the bracketed fallback in the
paper anyway** as a comparison. *"How well can you do a routing study with nothing but depot-to-town
odometer readings?"* is a question that matters to every utility in the region with no GIS
department, and answering it with a measured error (bearing substitution costs +1.01 km MAE; headline
metrics move under 3%) is a better contribution than quietly deleting the fallback.

---

## 8. Plan to a complete draft by Friday 2 October 2026

Ten days, five people. **Three tracks run in parallel from Wednesday morning so that nobody is
blocked on the matrix.** The optimisation track develops against the bracketed fallback matrices from
day one and swaps in the real matrix by changing one function; because every experiment re-runs in
seconds, the entire results suite regenerates the same afternoon the matrix lands.

**Owners.**

| Person | Role | Track |
|---|---|---|
| **Jonathan Kalami** | Lead modeller — SP-ECG engine, arc model, experiments | **O** (optimisation) |
| **Sally Gli** | Baselines, statistics, verification, scaling | **O** |
| **Tayyiba Amartey** | Data owner — coordinates, matrix, data repairs, figures | **M** (matrix/data) |
| **Dr. Ali Abubakar** | ECG liaison, permissions, TRSP/routing literature, Methods review | **W** (writing) |
| **Dr. Bright Owusu** | Equity/power literature, Intro & Related Work, venue, compliance | **W** |

> **Note on the deadline.** 2 October is the **lecturer's** deadline and the target for a complete,
> internally reviewed draft. **It is not a submission date.** Journal submission follows supervisor
> review, and rushing a submission risks a desk reject that costs months. Say this to the lecturer
> now so expectations match.

### Today — Tuesday 22 September, evening (30 minutes, in parallel)

- [ ] **Dr. Abubakar — email Abdul Haliq / ECG Hohoe tonight.** This is the only critical-path item
      outside the team's control. Request written permission to publish district operational data,
      **plus answers to eight one-line questions**:
      (1) Do crews return to the post **at end of shift**, and is that drive inside the paid 8 hours?
      (2) How often does a mid-job return to the post for a tool or material actually happen — 1 job
      in 5, or 1 in 20?
      (3) **Which fault types require material stocked only at the post?**
      (4) Is $Q=3$ faults/crew a real limit or an assumption?
      (5) Is $H=8$ h the real shift, and is there paid overtime?
      (6) Are all five crews Hohoe-based and identically skilled?
      (7) Does ECG use a formal Near/Far kilometre threshold?
      (8) Does ECG have a published restoration target for High-priority faults? *(This becomes $D$
      in the SLA constraint and converts the study's best result into a statement about whether the
      utility meets its own standard.)*
      Also ask for: a historical fault log (even 1–3 months), **customers affected per fault or per
      feeder**, and ECG's own SAIDI/SAIFI/CAIDI for Hohoe or Volta.
- [ ] **Dr. Owusu — email the CIRED 2027 secretariat** asking whether the 14 September abstract
      deadline was extended (it closed eight days ago; CIRED often extends). It costs a 500-word
      abstract and CIRED is the single best domain match in the world.
- [ ] **Tayyiba — start the coordinate sheet** (§7.2). Every hour of delay here is an hour off the end.
- [ ] **All — agree authorship order, corresponding author, and CRediT roles.** Do it now, in writing.

### Wednesday 23 September — engine, matrix start, literature start

| Track | Owner | Task | Done when |
|---|---|---|---|
| **O** | Jonathan | Build `src/model_setpart.py`: column enumeration + SP master with $\alpha/\beta$, two-sided $G$ on **excess wait**, $\theta$ cap, GMD, $R^{\max}$, $C_{\max}$, SLA and position filters, restocking. **Status assertion + full-coverage re-assertion on every extract** (§6A.8). A 174-line CLI reference implementation already exists in the scratchpad — start from it. | Solves the case instance against a fallback matrix; objective **varies**; all 15 faults covered |
| **O** | Jonathan | Run the three-way verification (§6A.8): brute force at $n\le6$, independent simulator, arc-model cross-check | Agreement to $10^{-6}$ on all three |
| **O** | Sally | Build `src/baselines.py`: ≥20,000 random round-robin draws (report **feasibility rate** and mean ± 95% CI over feasible draws only), greedy nearest-available, greedy priority-first, zone clustering. **Label infeasible baselines as infeasible, never as slower feasible alternatives** | Each baseline returns a metric **and a feasibility verdict** |
| **M** | Tayyiba | Finish coordinates (§7.2); **fetch the OSRM matrix (§7.3)**; cross-check against ORS; run calibration + quality gates (§7.4) | `dataset/ecg_intertown_matrix.csv` + `osrm_raw.json` committed with a provenance header |
| **M** | Tayyiba | Fix Fodome / Gbledi / Godenu (§7.5); normalise town names; replace `ceil(max)/2` with a fixed 20 km threshold; **uncomment the two `to_csv` calls**; repair the `03_diagnostics.ipynb` syntax error; delete `codes.txt` | `01_data.ipynb` runs clean end-to-end and regenerates both CSVs |
| **W** | Abubakar | Related Work clusters (i) TRSP/WSRP and (ii) latency routing — §9 list, 4–6 refs each | Cluster drafts exist |
| **W** | Owusu | Related Work clusters (iii) equity and (iv) utility crew dispatch. **Read Dey & Ornik (2022) and Rodriguez-Garcia et al. (2024) first — they are the closest prior art and must be cited and differentiated** | Cluster drafts exist |

### Thursday 24 September — 🚦 GATE 1 (model)

| Track | Owner | Task |
|---|---|---|
| **O** | Jonathan | $\theta$ sweep ($\theta\ge1$, two-sided, $w_H=1$); $\alpha/\beta$ table; **$\varepsilon$-constraint frontier**; priority experiments (weight, SLA, position cap) as a **separate** experiment at $w_H=1$ controls |
| **O** | Sally | Multi-instance study: **30 independent simulated days**, pinned and disclosed generator, reporting the optimum, the feasibility rate of ad-hoc dispatch, and improvement with 95% CIs |
| **M** | Tayyiba | If the matrix landed: re-run everything on it. If not: build the **bracket** (matrices A and B, §7.6) and hand both to Track O |
| **W** | Both supervisors | Draft Introduction + Related Work; write the **SAIDI bridge** subsection (§8.1 below) |

> ### 🚦 GATE 1 — Thursday 24 September, 18:00. Do not proceed until all six are true.
> 1. The objective **differs** between the optimal solution and a random feasible one, and the
>    min-vs-max spread over the identical feasible set is reported.
> 2. The equity term **binds**: tightening $\theta$ or $\varepsilon$ changes the plan.
> 3. $\alpha/\beta$ produce **different** solutions — and you know how many distinct ones (expect
>    collapse; that is why the $\varepsilon$-constraint exists).
> 4. All three verification checks pass to $10^{-6}$.
> 5. Every extracted plan has been asserted `Optimal` **and** covers all 15 faults.
> 6. All four notebooks execute top-to-bottom from a clean kernel.
>
> **If Gate 1 fails, stop and fix it. Do not let anyone draft Results.** A draft built on an unsound
> model is worse than no draft.

### Friday 25 September — 🚦 GATE 2 (matrix)

| Track | Owner | Task |
|---|---|---|
| **O** | Jonathan | Scaling study: $n\in\{15,30,45,60,90,120\}$; report filtered column count, enumeration time, solve time, LP-vs-IP gap and **proof status** at each. State the ceiling honestly (§6A.9) |
| **O** | Jonathan | Head-to-head vs the **cumulative-flow-strengthened** arc model (not plain big-M + MTZ — §6A.9) |
| **O** | Sally | Sensitivity: $Q\in\{2,3,4,\text{free}\}$; $H\in\{6,7,8,10\}$; $\rho\in\{0,1\}$; **Near/Far threshold sensitivity**; restocking on/off |
| **M** | Tayyiba | Fit and report the **speed model** (§7.7); write the data-provenance paragraph |
| **W** | Owusu | Venue decision locked; template downloaded; author guidelines read |

> ### 🚦 GATE 2 — Friday 25 September, 18:00.
> **Either** the real OSRM matrix exists, is calibrated against the 23 field legs, and has passed the
> quality gates — **or** the team formally adopts the **bracketed fallback** (§7.6) and writes the
> paper in bounded form: aggregates reported with a spread, the specific dispatch plan explicitly
> **not** offered as an operational recommendation.
>
> **Do not spend the weekend hoping.** Decide on Friday. The bracketed paper is defensible; a single
> imputed matrix presented as data is not.

### Saturday 26 – Sunday 27 September — buffer and writing

Light days. Whoever is furthest behind catches up. Supervisors draft Methods against §6A in the
README's existing notation. **If the matrix slipped past Gate 2, Tayyiba's whole weekend is the
matrix** — it is still worth having by Monday, and every experiment re-runs in minutes.

### Monday 28 September — full results suite on the final matrix

| Owner | Task |
|---|---|
| Jonathan | **Re-run every experiment on the final matrix** (the whole suite is minutes of compute — this is why set partitioning was chosen). Save every run to `result/` as JSON with solver status, bound, gap and time limit |
| Sally | Statistical comparison across the 30 instances: paired test, effect size, CIs. **Lead with the feasibility argument** (§8.2) |
| Tayyiba | Figures F1–F7 (§8.3) |
| Supervisors | Methods and Data sections drafted |

### Tuesday 29 September — 🚦 GATE 3 (results freeze)

| Owner | Task |
|---|---|
| All | Finish figures and tables. **Every number that will appear in the paper exists on disk in `result/` by 18:00** |
| Jonathan | `requirements.txt` with pinned PuLP and CBC versions; README rewrite (fill the empty **Project Overview** and **References**; fix the equity linearisation; add Install/Run/Results; add the data licence and provenance statement) |
| Tayyiba | Data licence (CC-BY-4.0 for `dataset/`, separate from the code's MIT); tagged repository release |

> ### 🚦 GATE 3 — Tuesday 29 September, 18:00: **results freeze.**
> **No figure gets made after this point. No number changes after this point.** If something is
> wrong, it gets fixed now or it gets written into Limitations.

### Wednesday 30 September – Thursday 1 October — write

Wednesday (parallel, to a shared document):
- **Abstract + Introduction** — *must state in the abstract that the fault instances are synthetic*
- **Related Work** — the four clusters from §9
- **Methods** — §6A in the README's notation: name the model class, state the arc formulation, prove
  Lemmas 1–2, present set partitioning as the solution method, state **every** assumption in §6A.7
- **Data** — provenance, the 23-of-552 disclosure, the speed model, the Fodome/Gbledi/Godenu
  corrections, the zone-threshold justification
- **Results** — Gate 3 artefacts only

Thursday:
- **Discussion** — the SAIDI bridge, the price of fairness, the SLA feasibility result
- **Limitations — write it honestly and prominently.** Single district; **synthetic faults**;
  **imputed or API-derived inter-town matrix**; deterministic travel times; single-day static
  horizon; no fault arrivals during the shift; no crew unavailability; no multi-day rostering; no
  re-dispatch; equity measured over two zones on a 7/8 split; priority weights and $D$ with no ECG
  source. **A frank Limitations section is the cheapest credibility available and it pre-empts the
  referee's best objections.**
- **Future Work** — mid-shift depot revisits as a modelled decision; rolling-horizon re-optimisation
  (genuinely realistic at 0.13 s re-solve); branch-and-price beyond $n\approx150$; customers-weighted
  objective; stochastic travel times.

> ### 🚦 GATE 4 — Thursday 1 October, 18:00: complete draft, all sections, all figures placed.

### Friday 2 October — review and hand in

- Morning: **internal read-through by all five authors**, each reading a section they did not write.
- **Hunt for overclaims specifically.** Search the manuscript for: "optimal" (is it *proven*?),
  "first" (is it *scoped*?), "field data" (is it *really*?), "novel" (see §9 red lines), "improves
  travel time" (that was the constant). Every "optimal" must be backed by a parsed CBC log.
- Cover letter, CRediT statement, data-availability statement, ORCIDs for all five, funding
  statement (or "none"), competing-interests statement.
- Tag the repository at the submitted state and cite the tag in the data-availability statement.
- Hand in to the lecturer.

### 8.1 The SAIDI bridge — one subsection, worth more than another sensitivity sweep

IEEE Std 1366 defines SAIDI as total customer-interruption-minutes divided by customers served.
Outage duration decomposes as notification + dispatch + travel + repair, and the model's $R_j$ is
**precisely the dispatch-controllable share**. So

$$\text{dispatch-attributable customer-minutes} \;=\; \sum_j n_j\,(R_j+r_j)\Big/N_{\text{total}}$$

where $n_j$ is customers affected by fault $j$. This converts *"we cut mean response by x%"* into
*"we cut the controllable component of SAIDI by y customer-minutes"* — **the same currency ECG uses
in its own PURC tariff filings.** Report results in both units.

**$n_j$ is the highest-value data item after the matrix.** ECG holds distribution-transformer and
feeder customer counts; request them with everything else. Weighting $R_j$ by customers is a one-line
change ($w_j \leftarrow n_j$) and it makes the objective speak the utility's own language. It also
pre-empts the referee who asks why a fault affecting 40 customers counts the same as one affecting
4,000. **If $n_j$ cannot be obtained, still write the subsection**, state the equal-customers
assumption plainly, sensitivity-test it, and put the weighted version in Future Work.

### 8.2 Lead the Results with feasibility, not with a percentage

Every workstream measured this independently and it replicated everywhere: **ad-hoc dispatch produces
a shift-feasible plan only 3–8% of the time** (measured 2.9%, 3.4%, 4.08%, 5.5%, 14.2% across
matrices and protocols), and the optimiser produces one **every time, or proves that none exists**.
Meanwhile the natural human rules break outright: **priority-first — the most intuitive thing a
dispatcher does — produced no feasible plan at all** in one study, because a 4-hour transformer
installation could not be fitted into any crew's remaining shift; zone clustering broke the shift by
34 minutes; greedy nearest-available was shift-infeasible in several runs.

So the headline sentence is:

> *"Ad-hoc dispatch yields a workable day roughly one time in twenty. The model yields one every time
> a workable day exists, and proves it when none does — and it is ~40% faster."*

Then the percentage, **with a confidence interval, never as a single number**, and with an explicit
note that part of the improvement is over plans that could not have been executed.

**Two things to drop, and one to pin.** Design 3's *"19 of 30 simulated days admit no feasible plan
with 5 crews"* is the most dramatic operational sentence available and the **least reproducible** —
an independent 30-day replication got 2/30. **Pin and disclose the fault generator or cut the
claim.** Likewise, the superseded §9.2 probe numbers (2.549 h, $C_{\max}$ 7.982 h, "1 in 3,000
feasible", "14.6% faster") **must not appear anywhere.**

**What replicated across every workstream and independent check, and is therefore safe to write
(once regenerated on the real matrix):** ad-hoc dispatch is shift-feasible 3–8% of the time;
optimisation beats the mean feasible random plan by 40–47% in every geometry tested; near-parity
costs roughly 3–7% of mean response; the Far/Near penalty under pure efficiency is always > 1; and a
1-hour High-priority SLA is infeasible while 1.2 h is achievable at a large but bounded cost.

### 8.3 Figures (target 7)

| | Figure |
|---|---|
| F1 | Map/schematic of the 23 towns with Near/Far zones and the Hohoe depot |
| F2 | **Gantt chart of the five crew routes** under the optimal plan — the figure that makes the routing visible, and where a reader sees the two Afadzo South faults chained |
| F3 | **$\varepsilon$-constraint efficiency–equity frontier** (mean response vs $G$), with the weighted-sum points overlaid to show the collapse |
| F4 | Equity vs $\theta$: $\bar R^{N}$ and $\bar R^{F}$ plotted **separately**, plus $R^{\max}$ and Gini on a secondary axis |
| F5 | Distribution of baseline outcomes vs the optimum, with **infeasible plans shaded** |
| F6 | Solve time and column count vs $n$, with proof status annotated |
| F7 | **Calibration scatter: 23 field-measured depot legs vs API durations**, with $\lambda$, MAE and $R^2$ — this figure validates the field data and the API against each other in one panel, and it is the cheapest credibility win in the paper |

### 8.4 Risk register

| Risk | Likelihood | Mitigation |
|---|---|---|
| **The real matrix does not arrive** | Medium | Gate 2 forces the decision on Friday 25. The bracketed fallback (§7.6) is built, metric-verified, and defensible. **Decide; do not hope.** |
| ECG permission does not arrive | Medium | Draft anyway; hold **submission**, not drafting. Anonymise to "a rural district in the Volta Region" if refused. |
| Coordinates prove harder than expected (10 towns unlocatable remotely) | **High** | Phone GPS readings on site are the fallback *and* the more defensible provenance. Start Tuesday evening, not Wednesday. |
| A wrong number reaches the paper via the PuLP status or stale-value traps | **High if unguarded** | Assertions in code (§6A.8), CBC log parsing, and the Friday overclaim hunt. |
| Reference gathering underestimated | High | Both supervisors start Wednesday, not Thursday. §9 already lists ~45 candidates. |
| Scope creep into branch-and-price / dynamic dispatch | Medium | Explicitly out of scope. Named in Future Work. |
| Draft ≠ submission-ready on 2 October | **Expected — accept it** | Target a complete internal draft for the lecturer; submit after supervisor review. Rushing a submission risks a desk reject costing months. |

### 8.5 Explicitly out of scope

Branch-and-price / column generation; stochastic or dynamic fault arrivals; multi-day rostering;
real-time re-dispatch; mid-shift depot revisits as an endogenous *decision* (they are handled as an
exogenous scenario); crew-specific skills; customers-weighted objective if $n_j$ does not arrive.
**Name all of them in Future Work** — they are what makes this a first paper with a sequel rather
than a one-off.

---

## 8B. Venue recommendation

**The audit's advice is now wrong and must be inverted.** It said "conference first, PowerAfrica."
**PowerAfrica 2026 is running this week in Nairobi (21–25 September) and its paper deadline was
7 April 2026.** No 2027 edition is announced. Going conference-first now means submitting ~March 2027
and appearing ~September 2027. **A journal is faster.**

> ### Recommendation: submit to **Scientific African** (Elsevier, gold OA, ISSN 2468-2276), with an
> **IEEE AFRICON 2027** short version in parallel.

**Why Scientific African.** Best fit × indexing × cost. Its stated mission is publishing African
primary data, which is exactly the project's strongest asset. Scopus + ESCI + DOAJ. APC reported at
~USD 720 (one source said ~USD 200 — **verify**), and likely waived or halved under Research4Life.
CiteScore ~3.3; ~4 days to first decision on the desk screen. **Risk:** a reported ~13% acceptance
rate and a fast desk screen, so the cover letter and the abstract must carry the contribution in the
first three sentences.

**Why AFRICON 2027 in parallel, not instead.** 18th IEEE Region 8 AFRICON, **23–25 September 2027,
Kumasi, Ghana** — the audit missed it and it is the best conference fit on practical grounds: IEEE
Xplore indexed, **in the team's own country** (no travel or visa cost), CFP expected ~Feb–Mar 2027,
which is exactly when a journal submission made in October 2026 will be in review. Make the
conference paper the short version and the journal paper the full one, and cite across to avoid
self-plagiarism.

**Fallbacks, in order.**
1. **JESIT** (SpringerOpen) — **zero APC for everyone, permanently**, funded by a third party. No
   waiver paperwork, no surprise invoice. Power/electrical scope fits. **Verify its Scopus status
   first**; if it is not Scopus-indexed it may not count for the university's purposes.
2. **Decision Analytics Journal** (Elsevier) — if the team wants to be read as OR rather than power
   engineering. "Optimization modelling" is an explicit scope term. APC USD 2,190 — binding unless
   waived.
3. **International Transactions in Operational Research** (Wiley/IFORS) — the audit missed it, and
   its scope text ("regional OR work with potential for application in other nations") reads as
   though written for this paper. **Subscription route is free.** Higher bar; hold in reserve.
4. **Socio-Economic Planning Sciences** — the true disciplinary home of the equity argument, IF ~6.2.
   A genuine stretch on this data; the right aspiration for the follow-up paper with a second
   district.
5. Results in Engineering / Heliyon / IEEE Access as paid fallbacks (USD 1,080–2,320).

**Do today:** email CIRED 2027 (Stockholm, 14–17 June 2027) asking whether the 14 September abstract
deadline was extended. It is the world's main electricity-distribution conference and a near-perfect
domain match; it costs a 500-word abstract.

**⚠ Verify before committing money:** whether Ghana is Research4Life **Group A** (full Elsevier APC
waiver) or **Group B** (50%). Two search summaries said Group A, but Ghana's GNI per capita (~USD
2,370) and HDI (0.628) against the published criteria suggest it may not qualify. **This single fact
decides whether three of the five candidate venues cost zero or several thousand dollars.** Practical
route: start a submission in Elsevier's system — the author system quotes the waiver-adjusted APC
automatically. **Do not commit to a USD 2,000+ venue on the assumption of a waiver.**

### Does the reformulation lift the tier?

Partly, and less than it feels like it should. It moves the paper from unsubmittable to genuinely
submittable, which is the big move. But a depot-origin multi-vehicle routing problem with capacity,
duration and equity constraints is a **textbook model class**. What actually lifts the tier is the
empirical package: the real inter-town matrix, the calibration against 23 field legs, 30 instances
instead of one, a feasibility-aware baseline, and the efficiency–equity frontier. **With that
package this is a solid Q2 applied case study. Without it, it stays at the fast-and-broad end.**

**Claim the application, the data and the trade-off curve. Explicitly disclaim methodological novelty
in the model class.** Reviewers punish overclaiming far harder than modest scope.

---

## 9. References, by theme — with confidence flags

**⚠ HOW TO USE THIS LIST.** Every entry below was assembled in a sandbox where `arxiv.org`,
`link.springer.com`, `sciencedirect.com`, `onlinelibrary.wiley.com`, `ideas.repec.org`,
`semanticscholar.org` and most publisher domains were **blocked**. Citations were corroborated from
multiple independent search-result snippets, **not from full text or publisher landing pages**.
Authors, titles, venues and years are solid. **Page ranges and DOIs on anything not marked
[verified] must be checked against the publisher record before submission.** The team has
unrestricted internet; this is a two-hour task and it protects the whole bibliography.

Target 20–30 references in the manuscript. Roughly 5–7 per cluster.

### 9.1 Problem class — TRSP / workforce scheduling and routing

- **[verified]** Cordeau, J.-F., Laporte, G., Pasin, F., & Ropke, S. (2010). Scheduling technicians
  and tasks in a telecommunications company. *Journal of Scheduling*, 13(4), 393–409.
  DOI: 10.1007/s10951-010-0188-7
- **[verified]** Kovacs, A. A., Parragh, S. N., Doerner, K. F., & Hartl, R. F. (2012). Adaptive large
  neighborhood search for service technician routing and scheduling problems. *Journal of
  Scheduling*, 15(5), 579–600. DOI: 10.1007/s10951-011-0246-9
- **[verified]** Pillac, V., Guéret, C., & Medaglia, A. L. (2013). A parallel matheuristic for the
  technician routing and scheduling problem. *Optimization Letters*, 7(7), 1525–1535.
  DOI: 10.1007/s11590-012-0567-4 — **cite at the point where you say depot returns are tool-driven;
  this paper already models tools and spare parts held centrally.**
- **[verified]** Castillo-Salazar, J. A., Landa-Silva, D., & Qu, R. (2016). Workforce scheduling and
  routing problems: literature survey and computational study. *Annals of Operations Research*,
  239(1), 39–67. DOI: 10.1007/s10479-014-1687-2
- **[likely-real — VERIFY issue/year]** Gamst, M., & Pisinger, D. (2024). Decision support for the
  technician routing and scheduling problem. *Networks*, 83(1), 169–196. DOI: 10.1002/net.22188
- **[uncertain — VERIFY AUTHOR LIST]** Bangerter, E., et al. (2026). A column-generation approach for
  an electricity technician routing and scheduling problem with a lexicographic objective.
  arXiv:2604.05153 — **closest paper in scope (electricity-utility TRSP on real EDF data). Engage
  with it or a referee will ask why you did not.**

### 9.2 Routing with cumulative / latency objectives and duration limits

- **[verified]** Ngueveu, S. U., Prins, C., & Wolfler Calvo, R. (2010). An effective memetic algorithm
  for the cumulative capacitated vehicle routing problem. *Computers & Operations Research*, 37(11),
  1877–1885. DOI: 10.1016/j.cor.2009.06.014 — **this is your problem, named and defined.**
- **[verified]** Fischetti, M., Laporte, G., & Martello, S. (1993). The delivery man problem and
  cumulative matroids. *Operations Research*, 41(6), 1055–1064. DOI: 10.1287/opre.41.6.1055
- **[verified]** Fakcharoenphol, J., Harrelson, C., & Rao, S. (2007). The k-traveling repairmen
  problem. *ACM Transactions on Algorithms*, 3(4), Article 40. DOI: 10.1145/1290672.1290677 — cite
  for NP-hardness.
- **[verified]** Corona-Gutiérrez, K., Nucamendi-Guillén, S., & Lalla-Ruiz, E. (2022). Vehicle routing
  with cumulative objectives: A state of the art and analysis. *Computers & Industrial Engineering*,
  169, 108054. DOI: 10.1016/j.cie.2022.108054
- **[verified]** Lysgaard, J., & Wøhlk, S. (2014). A branch-and-cut-and-price algorithm for the
  cumulative capacitated vehicle routing problem. *EJOR*, 236(3), 800–810.
  DOI: 10.1016/j.ejor.2013.08.032
- **[verified]** Laporte, G., Nobert, Y., & Desrochers, M. (1985). Optimal routing under capacity and
  distance restrictions. *Operations Research*, 33(5), 1050–1073. — the $Q$ + $H$ constraint pair.
- **[verified]** Laporte, G., Desrochers, M., & Nobert, Y. (1984). Two exact algorithms for the
  distance-constrained vehicle routing problem. *Networks*, 14(1), 161–172.
  DOI: 10.1002/net.3230140113
- **[verified]** Toth, P., & Vigo, D. (Eds.) (2014). *Vehicle Routing: Problems, Methods, and
  Applications* (2nd ed.). MOS-SIAM Series on Optimization 18. SIAM. ISBN 978-1-611973-58-7
- **[verified]** Laporte, G. (2009). Fifty years of vehicle routing. *Transportation Science*, 43(4),
  408–416. DOI: 10.1287/trsc.1090.0301
- **[verified]** Campbell, A. M., Vandenbussche, D., & Hermann, W. (2008). Routing for relief efforts.
  *Transportation Science*, 42(2), 127–145. DOI: 10.1287/trsc.1070.0209 — the classic demonstration
  that arrival-time objectives produce structurally different routes from travel-cost ones.

### 9.3 Solution method — set partitioning, column generation, subtour elimination

- **[verified]** Balinski, M. L., & Quandt, R. E. (1964). On an integer program for a delivery
  problem. *Operations Research*, 12(2), 300–304. DOI: 10.1287/opre.12.2.300 — **the citation for
  SP-ECG.**
- **[verified]** Baldacci, R., Mingozzi, A., & Roberti, R. (2012). Recent exact algorithms for solving
  the vehicle routing problem under capacity and time window constraints. *EJOR*, 218(1), 1–6.
  DOI: 10.1016/j.ejor.2011.07.037
- **[verified]** Desrochers, M., Desrosiers, J., & Solomon, M. (1992). A new optimization algorithm
  for the vehicle routing problem with time windows. *Operations Research*, 40(2), 342–354.
- **[verified]** Feillet, D., Dejax, P., Gendreau, M., & Gueguen, C. (2004). An exact algorithm for
  the elementary shortest path problem with resource constraints. *Networks*, 44(3), 216–229.
- **[verified]** Barnhart, C., Johnson, E. L., Nemhauser, G. L., Savelsbergh, M. W. P., & Vance, P. H.
  (1998). Branch-and-price: column generation for solving huge integer programs. *Operations
  Research*, 46(3), 316–329.
- **[verified]** Miller, C. E., Tucker, A. W., & Zemlin, R. A. (1960). Integer programming formulation
  of traveling salesman problems. *JACM*, 7(4), 326–329. DOI: 10.1145/321043.321046
- **[verified]** Gavish, B., & Graves, S. C. (1978). The travelling salesman problem and related
  problems. Working Paper GR-078-78, MIT Operations Research Center. — single-commodity flow; the
  recommended compact SEC if the arc model is ever solved at scale.
- **[verified]** Öncan, T., Altınel, İ. K., & Laporte, G. (2009). A comparative analysis of several
  asymmetric TSP formulations. *Computers & Operations Research*, 36(3), 637–654.
  DOI: 10.1016/j.cor.2007.11.008 — the citable justification for flow over MTZ.
- **[verified]** Kara, I., Laporte, G., & Bektaş, T. (2004). A note on the lifted MTZ subtour
  elimination constraints for the CVRP. *EJOR*, 158(3), 793–795. DOI: 10.1016/S0377-2217(03)00377-1
  — **a real trap: the Desrochers–Laporte (1991) lifting cuts off optima in the capacitated case.**
- **[verified]** Dantzig, G. B., Fulkerson, D. R., & Johnson, S. M. (1954). Solution of a large-scale
  traveling-salesman problem. *JORSA*, 2(4), 393–410. DOI: 10.1287/opre.2.4.393
- **[verified]** Charnes, A., & Cooper, W. W. (1962). Programming with linear fractional functionals.
  *Naval Research Logistics Quarterly*, 9(3–4), 181–186. DOI: 10.1002/nav.3800090303 — **cite only to
  note it is NOT needed here, because with exogenous zone membership the ratio cross-multiplies into
  a linear inequality.** Say where it *would* be needed (per-crew equity, where the denominator
  becomes a variable). A referee who knows fractional programming will look for this.

### 9.4 Equity and fairness in optimisation

- **[verified]** Matl, P., Hartl, R. F., & Vidal, T. (2018). Workload equity in vehicle routing
  problems: A survey and analysis. *Transportation Science*, 52(2), 239–260.
  DOI: 10.1287/trsc.2017.0744 — **non-negotiable. It is also the proof that this literature is
  crew-side, which is what leaves the customer-side framing open to you.**
- **[verified]** Karsu, Ö., & Morton, A. (2015). Inequity averse optimization in operational research.
  *EJOR*, 245(2), 343–359. — **non-negotiable.** Its equitability-vs-balance distinction is your
  Related Work framing.
- **[verified]** Marsh, M. T., & Schilling, D. A. (1994). Equity measurement in facility location
  analysis: A review and framework. *EJOR*, 74(1), 1–17. DOI: 10.1016/0377-2217(94)90200-3 — **where
  the Near/Far notion actually comes from.**
- **[verified]** Ogryczak, W. (2000). Inequality measures and equitable approaches to location
  problems. *EJOR*, 122(2), 374–391. DOI: 10.1016/S0377-2217(99)00240-4 — the mean-equity warrant for
  the combined objective. *(The specific $\lambda\le1$ bound for GMD is **likely-real** — verify
  against Ogryczak (2009), Ann. Oper. Res. 167(1), 61–86, before writing it as a numbered condition.)*
- **[verified]** Chen, X., & Hooker, J. N. (2023). A guide to formulating fairness in an optimization
  model. *Annals of Operations Research*, 326(1), 581–619. DOI: 10.1007/s10479-023-05264-y — the
  how-to for every candidate metric, including group-parity metrics (the class the Far/Near ratio
  belongs to).
- **[verified]** Bertsimas, D., Farias, V. F., & Trichakis, N. (2011). The price of fairness.
  *Operations Research*, 59(1), 17–31. DOI: 10.1287/opre.1100.0865 — your one abstract-ready number.
- **[verified]** Bertazzi, L., Golden, B., & Wang, X. (2015). Min–max vs. min–sum vehicle routing: A
  worst-case analysis. *EJOR*, 240(2), 372–381. DOI: 10.1016/j.ejor.2014.07.025 — **the citable
  answer to "why not minimise the worst wait?"**
- **[verified]** Lehuédé, F., Péton, O., & Tricoire, F. (2020). A lexicographic minimax approach to
  the VRP with route balancing. *EJOR*, 282(1), 129–147. DOI: 10.1016/j.ejor.2019.09.010
- **[verified]** Mostajabdaveh, M., Gutjahr, W. J., & Salman, F. S. (2019). Inequity-averse shelter
  location for disaster preparedness. *IISE Transactions*, 51(8), 809–829.
  DOI: 10.1080/24725854.2018.1496372 — **published precedent for mean + GMD in a MILP; cite it
  instead of inventing the formulation.**
- **[verified]** Gutjahr, W. J., & Fischer, S. (2018). Equity and deprivation costs in humanitarian
  logistics. *EJOR*, 270(1), 185–197.
- **[verified]** Huang, M., Smilowitz, K., & Balcik, B. (2012). Models for relief routing: Equity,
  efficiency and efficacy. *Transportation Research Part E*, 48(1), 2–18.
- **[verified]** Jain, R., Chiu, D.-M., & Hawe, W. (1984). A quantitative measure of fairness and
  discrimination for resource allocation in shared computer systems. DEC TR-301. —
  **cite only if you report Jain's index post-hoc. Do not optimise it: it is a ratio of quadratics
  (MIQCP at best) and was designed for goods where more is better, not for waiting times.** That
  last point is our methodological judgement, not an established result — present it as a modelling
  choice.
- **[likely-real — VERIFY]** Matl, P., Hartl, R. F., & Vidal, T. (2019). Workload equity in vehicle
  routing: The impact of alternative workload resources. *Computers & Operations Research*, 110,
  116–129.

### 9.5 Power distribution, outage management and crew dispatch

- **[verified]** Arif, A., Wang, Z., Wang, J., & Chen, C. (2018). Power distribution system outage
  management with co-optimization of repairs, reconfiguration, and DG dispatch. *IEEE Transactions on
  Smart Grid*, 9(5), 4109–4118.
- **[verified]** Arif, A., Ma, S., Wang, Z., Wang, J., Ryan, S. M., & Chen, C. (2018). Optimizing
  service restoration in distribution systems with uncertain repair time and demand. *IEEE
  Transactions on Power Systems*, 33(6), 6828–6838. DOI: 10.1109/TPWRS.2018.2855102
- **[likely-real — VERIFY IEEE VENUE]** Dey, A., & Ornik, M. (2022). Post-disaster repair crew
  assignment optimization using minimum latency. arXiv:2206.00597; IEEE Xplore doc 9922070. Code at
  `github.com/leadcatlab/MWLP-Storm-Repair`. — **CRITICAL PRIOR ART. Closest existing paper to your
  reformulated model. Read it before writing the Introduction and differentiate explicitly.**
- **[verified]** Rodriguez-Garcia, L., Hassan, A., & Parvania, M. (2024). Equity-aware power
  distribution system restoration. *IET Generation, Transmission & Distribution*, 18, 401–412.
  DOI: 10.1049/gtd2.12982 — **you are NOT first to consider equity in power restoration. Cite and
  differentiate: they model network restoration, you model crew dispatch on a real road network.**
- **[likely-real — VERIFY]** Cavdar, B., He, Q., & Qiu, F. (2022). Repair crew routing for power
  distribution network restoration. arXiv:2204.04848 — argues explicitly that the objective must be
  service-disruption time, not travel distance. **The cleanest external justification for abandoning
  the constant travel-time objective.**
- **[likely-real — VERIFY]** Diadelmo, M. V. F., Batista, L. S., & Bessani, M. (2026). Dynamic
  framework for crew dispatch optimization in power distribution fault inspection. *Reliability
  Engineering & System Safety*, 272(P1), 112527. DOI: 10.1016/j.ress.2026.112527 — **one of very few
  papers in the routine, non-disaster regime this project studies. Cite it or a referee will ask why
  you claimed the regime is empty.**
- **[verified]** IEEE Std 1366-2022, *IEEE Guide for Electric Power Distribution Reliability Indices*.
  — **mandatory for the SAIDI bridge (§8.1).**

### 9.6 Ghana and sub-Saharan African context

- **[verified]** Osunmuyiwa, O., Odero, M., Wall, A., Goode, J., Flaspohler, G., Abrokwah, K.,
  Adkins, J., & Klugman, N. (2025). Mobilizing power quality and reliability measurements for
  electricity equity and justice in Africa. *Nature Energy*, 10(3), 395–403.
  DOI: 10.1038/s41560-025-01717-9 — **the single best motivating citation available: measured
  power-quality inequity in Accra, top-tier venue, same country. It measures; you optimise. That
  complementarity is the best sentence in your Introduction.**
- **[verified]** Klugman, N., Adkins, J., Berkouwer, S., Abrokwah, K., Podolsky, M., Pannuto, P.,
  Wolfram, C., Taneja, J., & Dutta, P. (2023). Measuring grid reliability in Ghana. In Madon, T.,
  et al. (Eds.), *Introduction to Development Engineering*, Ch. 6. Springer. Open access.
  DOI: 10.1007/978-3-030-86065-3_6 — **shows utility-reported outage statistics diverge from measured
  reality in Ghana. This simultaneously motivates your own field measurement AND gives principled
  cover for using simulated faults.**
- **[verified]** Amewornu, E. M., & Nwulu, N. I. (2021). Assessing the impact of demand response
  programs on the reliability of the Ghanaian distribution network. *PLOS ONE*, 16(3), e0248012.
  DOI: 10.1371/journal.pone.0248012
- **[likely-real — VERIFY]** Kumi, E. N. (2017). *The electricity situation in Ghana: Challenges and
  opportunities.* CGD Policy Paper 109. Center for Global Development.
- **[likely-real — VERIFY EXACT TITLE AND DATE]** Electricity Company of Ghana Ltd. (2022). *Proposal
  for the review of electricity distribution service charge / aggregate revenue requirement.*
  Submission to PURC, Accra. `purc.com.gh` — **primary-source evidence that ECG itself targets SAIDI,
  SAIFI and CAIDI. This is what ties your objective to the utility's own regulatory goals, and it is
  a document the team can obtain locally.**
- **[likely-real — VERIFY]** Cole, M. A., Elliott, R. J. R., Occhiali, G., & Strobl, E. (2018). Power
  outages and firm performance in sub-Saharan Africa. *Journal of Development Economics*, 134,
  150–159.
- **[likely-real — VERIFY]** African Development Bank (2021). *Electricity Regulatory Index for Africa
  2021.* AfDB, Abidjan.
- **[uncertain — AUTHOR LIST NOT CONFIRMED]** (2026). Assessing post-conflict electric power supply
  reliability in low voltage distribution networks of Aksum, Ethiopia. *Scientific Reports*.
  DOI: 10.1038/s41598-026-35599-y

### 9.7 Travel-distance estimation and geocoding

- **[verified]** Ballou, R. H., Rahardja, H., & Sakai, N. (2002). Selected country circuity factors
  for road travel distance estimation. *Transportation Research Part A*, 36(9), 843–848.
  DOI: 10.1016/S0965-8564(01)00044-1 — justifies the 1.162 circuity multiplier in the fallback.
- **[verified]** Giacomin, D. J., & Levinson, D. M. (2015). Road network circuity in metropolitan
  areas. *Environment and Planning B*, 42(6), 1040–1053. DOI: 10.1068/b130131p
- **[verified]** Nesbitt, R. C., et al. (2014). Methods to measure potential spatial access to
  delivery care in low- and middle-income countries: a case study in rural Ghana. *International
  Journal of Health Geographics*, 13, 25. DOI: 10.1186/1476-072X-13-25 — **the closest methodological
  precedent in the same country for why an imputed travel matrix is accepted practice in a data-poor
  setting. Cite this in §7.6 if you ship the bracket.**
- **[verified]** Boscoe, F. P., Henry, K. A., & Zdeb, M. S. (2012). A nationwide comparison of driving
  distance versus straight-line distance to hospitals. *The Professional Geographer*, 64(2), 188–196.
  DOI: 10.1080/00330124.2011.583586
- **[verified]** Luxen, D., & Vetter, C. (2011). Real-time routing with OpenStreetMap data. *ACM
  SIGSPATIAL GIS '11*, 513–516. DOI: 10.1145/2093973.2094062 — **cite this for OSRM if you use the
  `/table` endpoint.**
- **[verified]** Mennicken, E., Lemoy, R., & Caruso, G. (2024). Road network distances and detours in
  Europe: radial profiles and city size effects. *Environment and Planning B*.
  DOI: 10.1177/23998083231168870
- **[uncertain — SECONDHAND ONLY, VERIFY PAGE]** Cole, J. P., & King, C. A. M. (1968). *Quantitative
  Geography.* Wiley. — cited throughout the circuity literature as the origin of the 1.2–1.6 rural
  range.

### 9.8 Searches the team must run themselves before submission

Two 30-minute tasks with Google Scholar and Scopus access, which the audit environment did not have.
**They protect the paper's main novelty claim.**

1. `"equity" + "crew dispatch" + "distribution network"`, `"fairness" + "outage restoration" +
   "routing"`, `"energy justice" + "optimization" + Africa`. No study applying equity-aware routing
   to electricity fault repair in a low-income or rural African context was found — but absence of
   evidence from one blocked session is not proof.
2. Ghanaian institutional repositories (KNUST, University of Ghana, UEW), past IEEE PES/IAS
   PowerAfrica proceedings, and ECG/PURC annual reports, for **local reliability context**
   (SAIDI/SAIFI for ECG or the Volta Region). **Do not cite a Ghana reliability figure that is not
   verified** — none was confirmed in the audit environment.

### 9.9 🚩 Red lines — do NOT claim any of these as novel

Each would be refuted by a single search, and after an audit about overclaiming it would be fatal.

1. The **TRSP / CCVRP model class**, or any variant of "we propose a new formulation".
2. **Site-to-site crew movement with tool-driven depot returns** — a standard modelled TRSP feature.
3. **Minimising the sum of arrival/response times** — the cumulative/latency objective, 30+ years old.
4. **Simultaneous capacity + route-duration constraints** — Laporte, Nobert & Desrochers (1985).
5. **Equity or fairness constraints in routing** — surveyed at length by Matl et al. (2018).
6. **Minimum-latency repair-crew assignment for power restoration** — Dey & Ornik (2022) did exactly
   this, with public code.
7. **Equity in power restoration** — Rodriguez-Garcia et al. (2024). *"First to consider equity in
   power restoration"* is false and checkable in one minute.
8. **Set partitioning with route enumeration**, column generation, branch-and-price.
9. **Weighted-sum scalarisation, Pareto frontiers, the price of fairness.**
10. **Computing SAIDI/SAIFI/CAIDI for an African network** — many studies already do.
11. **MILP + CBC/PuLP** as a solution method.
12. **The Far/Near ratio as a "novel equity measure"** — it is a standard group-parity metric.

### 9.10 ✅ What you CAN legitimately claim

1. **Primary, field-measured road travel times for 23 towns in an operating rural sub-Saharan
   distribution district.** Almost all TRSP and equity-routing work uses synthetic, Solomon-derived
   or European commercial instances. **This is the paper's real asset — say so explicitly.**
2. **A field-validated dispatch protocol**, documented by interview with a named ECG Hohoe technician,
   with the modelling consequence **quantified** (§6.4). Frame it as case-study evidence that field
   validation of assumptions is not a formality.
3. **Customer-side spatial equity inside a routing model**, as distinct from the crew-side workload
   equity that dominates the VRP equity literature. **Cite Matl et al. to show you know the
   difference, and Marsh & Schilling to show where your notion comes from.** This is the thinnest
   intersection in the literature and the strongest defensible claim.
4. **A quantified efficiency–equity frontier and price of fairness for electricity restoration in a
   low-income rural context**, usable as a decision aid by a utility with stated regulatory targets.
5. **The regime.** Routine, day-to-day dispatch under a normal shift — not post-disaster restoration,
   which is where nearly all power-systems crew-routing work sits. Cite Diadelmo et al. (2026) as the
   main exception rather than ignoring it.
6. **Closing the descriptive-to-prescriptive loop for an African utility.** SSA distribution research
   measures reliability; it does not optimise dispatch. Going from indices to a dispatch model is a
   real, checkable claim.
7. **A modest, honest computational point.** At the district's actual operating scale the complete
   route set is small enough to enumerate exhaustively, so the problem is solved to **proven
   optimality with a free solver on commodity hardware**. That is a genuine deployment argument for a
   utility with no optimisation budget.
8. **An empirical comparison of equity metrics on a real network** — GMD, Gini, $R^{\max}$, range and
   the zone ratio computed on the same solution set, shown to rank plans differently. Small, real,
   and nearly free once the model runs.

### 9.11 ⚠️ The honesty constraint that governs every equity sentence

**The faults are simulated. No sentence may assert a measured real-world disparity.**

- ❌ *"Rural customers in Hohoe wait 1.6× longer for restoration."* — **not supportable, and it would
  be the single most damaging claim in the paper.**
- ✅ *"Under the fault scenarios considered, efficiency-only dispatch produces a rural response-time
  penalty of X, which the equity-constrained model reduces to Y at a cost of Z% in mean response."*

Equity results are statements about the **model's behaviour**, not about ECG's current performance,
until real fault logs are obtained. Put that sentence in Methods and repeat it in Limitations.
```

**Sources for the numbers I generated myself** (independent rebuild of the recommended formulation, nothing in the repo touched): `/tmp/claude-0/-home-user-optimization-assignment/09712f65-58f9-58af-a0a9-791748005b23/scratchpad/verify_spgraft.py` (enumeration, β-sweep, ε-frontier) and `verify2.py` → `verify2.out` (field-evidence value, restocking, priority confound, SLA sweep, θ hard cap). Field-data figures (Σt=8.985, τ̄_N=0.46887, τ̄_F=0.74771, 4-of-5 High faults are Far, Σr=20.07 h, 12 distinct towns) come straight from `dataset/*.csv` and are exact.