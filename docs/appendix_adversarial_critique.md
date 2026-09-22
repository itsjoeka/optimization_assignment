Background job note: the full 15-fault arc run is still solving after ~8 minutes (corroborating the plan's own "70–150 s" claim as optimistic); the 6-fault result below is conclusive and the argument is general.

---

# Completeness critique — prioritised gaps

Verification scripts: `/tmp/claude-0/-home-user-optimization-assignment/09712f65-58f9-58af-a0a9-791748005b23/scratchpad/critic_arc_Rinflation.py` (full instance) and `critic_small.py` (6-fault, ran to completion). Nothing under `/home/user/optimization_assignment` was touched.

## P0 — The plan repeats the exact defect it was written to fix

**1. The arc model of §6A.2 does NOT pin $R_j$ to the routes. Its equity term is inert in precisely the way the audited constraint was inert. [VERIFIED NUMERICALLY]**

$R_j$ appears only in `≥` constraints (C6, C7's lower bound, C8) plus a box upper bound. It is driven to the true arrival time *only* by the efficiency term. So whenever the objective does not monotonically push $R_j$ down, the solver inflates $R_j$ freely and buys equity with fiction. Built exactly as §6A.2 specifies, on the repo's real fault data:

| run | model reports G | TRUE gap recomputed from the routes it chose |
|---|---|---|
| α=1, β=0 | 0.1080 | 0.1080 ✓ |
| **α=0, β=1** | **0.000000** | **0.587667** |
| ε-constraint, ε=0.05 | 0.042467 | 0.052800 |

At α=0 the model reports *perfect equity* while the routes it selected have a gap of 0.59 h; `R_j` was inflated on 2 of 6 faults, and model mean-response (3.17) diverged from true mean-response (2.87). The ε-constraint understates the gap by 24% — and **that is the number the plan puts in Figure F3**, the paper's headline frontier.

This is the same disease as v1: a quantity that *looks* optimised but is decoupled from the decision. A referee reproducing the stated model gets a fake frontier. The plan's §6A.4 promises four independent non-degeneracy defences; none of them tests this, because all four test the *efficiency* objective.

**Fix (mandatory, cheap):** add the reverse big-M so $R$ is pinned by equality, not minimality:
$R_v \le R_u + r_u + \tau_{uv} + M(1-\hat x_{uv})\ \forall u,v\in J$, and $R_j \le \tau_{0j} + M(1-\sum_k x_{0jk})\ \forall j$.
Then state in Methods that $R_j$ equals the arrival time in *every* feasible solution, not just optimal ones. Add to Gate 1: *recompute every reported $R_j$, $G$, $\bar R^N$, $\bar R^F$ from the extracted arcs and assert agreement to 1e-6* — the plan's verification check 2 (independent simulator) would have caught this and is listed only for the SP model.

**2. The §6A.3 equivalence statement is false as written, and Gate 1's cross-formulation check will fail without anyone understanding why.**

"Same feasible set and the same optimal value" holds only for objectives that drive $R$ to its lower bound — i.e. α>0 and no ε-constraint. It is false for β=1, false for min-$G$, false for the ε-constraint form. Two further breakages:

- **C7 is imposed at every fault. Lemma 2 makes that equivalent to a route-duration limit *only under the triangle inequality*.** §7.4 point 4 then explicitly instructs the team **not** to enforce triangle inequality ("SP-ECG needs nothing of the matrix… run Floyd–Warshall as a diagnostic; do not apply it"). With violations present, C7 cuts off routes that SP admits → different feasible sets, arc optimum worse than SP optimum, cross-check disagrees. The plan contradicts itself across two sections.
- Violations are not hypothetical here: §7.4 prescribes a matrix that is *field-measured on row 0* and *λ-rescaled API elsewhere*. Mixing two measurement processes with a fitted 9.6-min egress overhead on the depot legs all but guarantees $\tau_{0v} > \tau_{0u}+\tau_{uv}$ somewhere. §7.4's assertion "triangle violations should be 0 for a road matrix" is true of a pure engine matrix, not of this hybrid.

**Fix:** state Lemma 2's triangle precondition *and* the §7.4 policy as one decision, not two. Either (a) enforce metric closure on the interior only, keep depot legs verbatim, re-check, or (b) drop C7-at-every-fault, add an explicit per-route duration constraint, and lose Lemma 2's corollary. Run the cross-check at n≤8 where it is cheap and *before* Gate 1, not as a headline.

**3. (S5)–(S6), the Gini machinery, is a third inert construct — 120 variables and 225 rows that compute nothing.**

$d_{jj'} \ge \pm(R_j-R_{j'})$ equals $|R_j-R_{j'}|$ **only if GMD carries a positive objective coefficient**. §6A.5 explicitly says report Gini as a lens and do *not* optimise it. So $d$ is unbounded above, GMD is whatever the basis happens to return, and anyone reading GMD off the solver prints a meaningless number. S5 exists only to feed S6 (the SLA is a column filter, $R^{\max}$ comes from $M_\omega$ via S4), so both are dead weight.

**Fix:** delete S5 and S6 from the model. Extract the route plan, recompute $R_j$ in Python, compute GMD/Gini/$R^{\max}$/range post-hoc. Also: the plan's $\mathrm{GMD}=\frac{1}{n^2}\sum_{j<j'}d_{jj'}$ is **half** the standard population GMD (the sum is over unordered pairs, the normaliser assumes ordered), so every reported Gini would be wrong by 2×.

## P1 — Results a referee will break

**4. The scaling study is run on infeasible instances from n=30 onward.** The plan holds m=5, H=8 (40 crew-hours) while scaling n. Mean repair time is 1.338 h/fault:

| n | Σ repair alone | crew-hours @ m=5 | feasible? | m actually needed |
|---|---|---|---|---|
| 15 | 20.1 h | 40 | yes | 3 |
| 30 | 40.1 h | 40 | **no** | 6 |
| 60 | 80.3 h | 40 | **no** | 11 |
| 120 | 160.6 h | 40 | **no** | 21 |

Every solve time quoted for n≥30 ("0.5–2.4 s at n=30… 144 s at n=120") is a time-to-prove-infeasibility, not a time-to-optimum, unless m was silently scaled — which the plan never states. **Fix:** scale $m=\lceil n/3\rceil$ or hold crew utilisation constant at the n=15 level, state the rule, and report it in the table. Re-run; the numbers will change.

**5. "Drop $Q$ entirely" is a trap without prefix pruning.** The complete ordered route set at n=15 with Q free is **3,554,627,472,075**, not 92,229. The 92,229 figure is only reachable by DFS with pruning on partial route duration (valid, because prefix arrival times are monotone increasing). The plan says "the complete set of shift-feasible depot-rooted routes" and never says how. A student writing `itertools.permutations` hangs forever, on Friday. **Fix:** specify prefix-pruned DFS explicitly and state the monotonicity lemma that makes it exact — one sentence, and it is *required* for the "complete column set ⇒ exactly optimal" claim to hold at Q-free.

**6. The recommended zone fix invalidates the plan's own "(field data), exact" constants.** A8 says fix the threshold at an exogenous 20 km. Under 19.5 km (current code): $n_N=8$, $n_F=7$, $\bar\tau^N=0.468875$, $\bar\tau^F=0.747714$. Under 20 km: **F2 (Liati, exactly 20.0 km) flips to Near**, giving $n_N=9$, $n_F=6$, $\bar\tau^N=0.477889$, $\bar\tau^F=0.780667$. Every equity constant, every $E^z$, every $G$, the 1.789 Far/Near ratio and the priority-confound table all move. The plan marks these numbers *(field data)* — i.e. exempt from the synthetic-matrix caveat — which is false. **Fix:** decide the threshold *first*, on Wednesday, recompute all constants, and put a one-line threshold-sensitivity result (19.5 vs 20 vs ECG's own) in Results.

**7. The statistical comparison is undefined on the instances that matter most.** If ad-hoc dispatch is feasible 3–14% of the time, then on most of the 30 instances the baseline has *no* feasible draw and the paired difference does not exist. The plan says "paired test, effect size, CIs" and stops. **Fix:** make feasibility rate the primary endpoint with a binomial CI; run the paired efficiency test (Wilcoxon signed-rank, not t-test — 30 routing deltas will not be normal) on the subset where both are feasible, report that subset's n explicitly, and say plainly that the efficiency comparison is conditional on baseline feasibility.

**8. The equity headline rests on a single instance.** Thursday's 30-instance study reports optimum, feasibility rate and improvement — but not $G$, not the Far/Near ratio, not the price of fairness. The paper's central claim is therefore n=1. **Fix:** carry the equity metrics through the 30-instance loop; report the distribution. This is nearly free once the loop exists.

**9. The baseline set is a straw man and the audit's own request was dropped.** Audit §4.4 asked for *current ECG practice* as the counterfactual; the plan has random, greedy-nearest, greedy-priority and zone-clustering — all weak, all beaten by construction. Comparing against the *mean* of feasible random draws also inflates the improvement. **Fix:** add (i) best-of-20,000 random as an order statistic (a much fairer bar), (ii) a 2-opt/relocate local search on the greedy solution — if the optimum only beats that by 3%, better to learn it now, and (iii) ask the technician how dispatch is actually decided today and encode it. Report improvement in absolute hours alongside %, against the 0.599 h teleportation floor so the reader sees the achievable range.

**10. Two stated evidence items are invalid on the model the paper presents.** The §6A.4 min–max spread (1.43→3.88 h) is meaningless in the arc model — maximising $\sum R_j$ with $R$ only lower-bounded just pushes every $R_j$ to its C7 upper bound regardless of route. State that the spread is over *route-induced* arrival times (SP form). Likewise §6A.5's "$\beta=1$ costs 79.6% efficiency" is an SP number; the arc model returns G=0 at β=1, as shown above.

## P2 — Citations and claims

**11. The `[verified]` flags are unearned and will stop the team from checking.** The §9 header admits nothing was checked against a publisher record; the entries then carry a label that reads as "checked." I spot-checked four of the riskiest and **all four are real** — Bangerter et al., arXiv 2604.05153 (authors: Elise Bangerter, David Schindl, Meritxell Pacheco Paneque, Nour Elhouda Tellache, Rodolphe Griset — the plan's "et al." can now be completed); Çavdar, He & Qiu, arXiv 2204.04848; Diadelmo/Batista/Bessani, RESS 272 (2026); Osunmuyiwa et al., Nature Energy 10 (2025); and the un-authored Aksum entry is **Berhe, Tuka & Kebedew, Sci Rep, DOI 10.1038/s41598-026-35599-y**. So the fabrication risk is lower than the plan fears. **Fix:** relabel to `[title/venue corroborated, DOI+pages unchecked]` and keep the two-hour verification task. Note "Cavdar" is **Çavdar**.

**12. But one characterisation is wrong, and that is worse than a wrong page number.** The plan cites Diadelmo et al. (2026) as "one of very few papers in the routine, non-disaster regime this project studies." Its abstract opens on *"the increasing frequency of natural disasters"* and it is a post-event inspection-dispatch paper. Writing the plan's sentence hands a referee a free hit on the paper's regime claim (§9.10 item 5), which is one of the few genuine novelty claims. **Fix:** re-read the abstract before citing; either drop the "routine regime" framing or find a real exemplar.

**13. Çavdar et al. raises an objection the plan does not pre-empt.** Their point is that disruption time depends on the routing sequence's interaction with *both* the road network and the power grid — restoring an upstream fault can restore customers downstream of another. The plan cites them only as cover for abandoning the travel-time objective. A referee will ask why $R_j$ ignores grid topology. **Fix:** one sentence in Limitations — faults are treated as electrically independent; feeder-level dependency is Future Work — plus this is another argument for getting $n_j$ (customers per fault).

**14. Venue facts need the same scepticism as citations.** I confirmed **AFRICON 2027, Kumasi, 23–25 Sept 2027** ✓. **Research4Life Ghana Group A vs B remains unresolved** — Elsevier waives 100% for Group A and 50% for Group B, and the official eligibility list is the only source. The plan's own warning stands; do not commit to a paid venue on an assumed waiver. The Scientific African APC figure (720 vs 200 USD) is still unverified.

## P3 — Field evidence: the biggest interpretive miss, and what to ask NOW

**15. The technician's own words describe a *dynamic* problem, and the plan reads them only as a travel-protocol fact.** The quote is: *"when there's a call and they are already at a different site, they just move to the new place."* **"When there's a call"** means faults arrive *during* the shift. That directly contradicts assumption A5 ("all n faults are known at shift start"), which the plan lists as merely "Assumed." The same sentence that justifies routing over assignment also undermines the static horizon — and the plan celebrates the first half while filing the second under Future Work. A referee who reads the interview quote in the paper will see this immediately. **Fix:** either frame the model explicitly as *morning dispatch planning / an offline benchmark bound on achievable performance* (honest, defensible, one paragraph), or add a cheap rolling-horizon evaluation — re-solve on arrival, which at 0.13 s is genuinely realistic and would be a strong result. Do not leave the contradiction visible and unaddressed.

**16. Ethics and consent for the interview are missing entirely, and they are on the critical path.** The plan builds the paper's headline field-evidence claim (§6.4, §9.10 item 2) on an interview with a named individual, proposes to cite it, and names "Abdul Haliq" in the Acknowledgment — with **no informed consent, no ethics clearance or waiver, no anonymisation policy** anywhere in 10 days of tasks. Elsevier and most journals ask for this at submission; university ethics offices take days even for a waiver. **Fix tonight:** written consent from the technician (and from Abdul Haliq for being named), an ethics waiver/approval letter request to the university, an Ethics Statement section, and a default of *"an ECG Hohoe technician (name withheld)"* unless consent to be named is explicit.

**17. Questions nobody has asked that should go in tonight's email.** The plan's eight are good. These are missing and each changes the model or the framing:
- **Are the day's faults known at shift start (overnight log), or do they come in live? Roughly what split?** — decides static vs dynamic (item 15).
- **What happens to a fault not reached before end of shift** — carried over, overtime, or escalated? If carried over, "infeasible" is not a real operational state and the headline feasibility argument needs rewording.
- **How many crews are actually on duty on a typical day, and how many vehicles?** m=5 is asserted; if 5 crews share 3 vehicles the whole model changes.
- **Is there a break / non-productive allowance inside the 8 h?** — shrinks effective H.
- **Do the 3 technicians ever split into 2 sub-teams?**
- **Who decides dispatch today, and by what rule?** — the missing baseline (item 9).
- **Does travel time differ materially in rainy season / at peak hours?** — the paper assumes deterministic travel.
- **Is Fodome's 0.65 km / Gbledi's 1.3 km an odometer reading from the post or from somewhere else?** — ask the measurement procedure, not just the value; it may explain both anomalies at once.

**18. The anonymisation fallback does not work.** The risk register says "anonymise to 'a rural district in the Volta Region' if ECG refuses." You cannot anonymise a dataset of 23 named towns with real road distances — one search identifies the district. If permission is refused, the CC-BY dataset release, the data-availability statement and the case-study framing all change. **Fix:** treat ECG permission as binary and plan the refusal branch properly (publish the model + a synthetic-geography instance, withhold the dataset), rather than assuming a mitigation that is not available.

## P4 — Is 10 days enough? No, not as scoped. Here is where it slips.

**Wednesday is the first failure point.** Jonathan is assigned: build the full SP engine (α/β, two-sided G on excess wait, θ, GMD, R^max, C_max, SLA + position filters, restocking, status and coverage assertions) **and** run three-way verification including building an arc model **and** a brute-force enumerator. That is 3 days, not 1. Tayyiba is assigned: 24 verified coordinates (the plan itself rates this "High" risk, 10 towns unlocatable remotely, 13 ambiguous names needing an ECG callback) **plus** OSRM **plus** ORS cross-check **plus** calibration **plus** quality gates **plus** three data repairs **plus** name normalisation **plus** threshold fix **plus** notebook repair. That is 3 days for one person, and the coordinate task depends on an ECG reply that may not come Wednesday.

**Writing is 2 days for a full paper.** Methods/Data/Results have no drafting slot before Monday 28. There is no manuscript file, no template and no LaTeX-vs-Word decision in the repo at any point before 25 Sept.

**`requirements.txt` lands Tuesday 29 — day 7.** Every number in the paper is generated before the environment is pinned. Pin it Wednesday morning or the reproducibility claim is retrospective.

**Cut, in this order:**
1. **The position-indexed model** (600 s, never closes). It is a third encoding used only as a losing benchmark. Delete it; §6A.9's honest-benchmark point is already made by the cumulative-flow-strengthened arc model.
2. **Scaling beyond n=60**, and only after fixing m (item 4). n∈{15,30,45,60} with a stated m-rule is a sufficient scaling story.
3. **30 instances → 12–15.** The CI widens slightly; the claim survives. Keep the generator pinned and disclosed either way.
4. **The full 24×24 matrix.** The plan already identifies the **13×13** (12 fault towns + depot) as the minimum viable artefact — make that the Wednesday target and the 24×24 a stretch goal, not the reverse.
5. **The restocking scenario and the position-cap priority variant** if Thursday slips. Both are nice-to-have; the SLA sweep is the result worth protecting.

**Do not cut:** the three verification checks, the feasibility-rate headline, the priority/zone confound control ($w_H=1$), and the Limitations section.

**One schedule fix:** move `requirements.txt`, the `src/` module skeleton, and the threshold decision to Wednesday 09:00, before any result is generated. And add a smoke test — three asserts (all 15 faults covered, status=="Optimal" parsed from the CBC log, recomputed $R_j$ matches model $R_j$) — that every experiment script calls. That single test file is what would have caught defect #1.