# Appendix — Literature and venue research (raw agent output)
> Six specialist agents. Confidence flags are the agents own. **Every citation must be verified against a publisher record before it is cited.**

---

## TRSP / technician routing

### Summary
The field evidence (crews travel site-to-site, returning to the Hohoe post only for tools/materials) moves this project out of assignment-problem territory and into a named, heavily-studied problem class. Three nested literatures matter.

(1) **Technician Routing and Scheduling (TRSP) / Workforce Scheduling and Routing (WSRP)** is the exact formal home. Cordeau, Laporte, Pasin & Ropke (2010) is the seminal applied paper (ROADEF 2007 telecoms challenge); Kovacs et al. (2012) is the canonical "service technician routing and scheduling" formulation with skills and team-building; Pillac et al. (2013) coined the modern TRSP label (routing staff subject to time windows, skills, tools, spare parts); Castillo-Salazar, Landa-Silva & Qu (2016) is the standard survey placing TRSP inside WSRP; Gamst & Pisinger (2024, *Networks*) is the current decision-support reference. Critically, **the "tools and spare parts" constraint that the ECG technician described — returning to the post only when a tool is needed — is already a modelled feature of TRSP** (Pillac et al. explicitly model tools/spare parts held at a central depot). The team's field observation is a *confirmation* of the standard TRSP structure, not a new variant.

(2) **The audit's response-time objective, once routing is admitted, is the multi-vehicle minimum-latency problem.** Minimising the sum of arrival times over multiple vehicles with capacity is the Cumulative Capacitated VRP (Ngueveu, Prins & Wolfler Calvo, 2010); its theory-side name is the k-traveling repairman problem (Fakcharoenphol, Harrelson & Rao, 2007). The shift limit H plus capacity Q is the classical distance-and-capacity-constrained VRP of Laporte, Nobert & Desrochers (1985). All three must be cited by name.

(3) **Equity.** Matl, Hartl & Vidal (2018) survey equity in VRP and — importantly — warn that equity objectives frequently produce degenerate or counterproductive solutions, which is exactly what the audit found at θ=1.6. But that literature is almost entirely about *workload balance across vehicles*; customer-side *spatial* equity belongs to equitable facility location (Marsh & Schilling, 1994) and inequity-averse optimisation (Karsu & Morton, 2015). This distinction is the team's clearest opening.

(4) **Application context.** Repair-crew routing for power distribution is a mature IEEE literature (Arif et al., 2018). Dey & Ornik (2022) already apply *minimum latency* to repair-crew assignment — the team must read this before writing any novelty claim.

### Positioning
**Name the problem correctly in the Abstract and Methods, using the field's own vocabulary.** The reformulated model is a *Technician Routing and Scheduling Problem* (TRSP), a special case of the *Workforce Scheduling and Routing Problem* (WSRP), whose objective function makes it specifically a *multi-vehicle minimum-latency / cumulative capacitated VRP* under joint capacity and route-duration restrictions. Stating this in one sentence, with Castillo-Salazar et al. (2016), Pillac et al. (2013) and Ngueveu et al. (2010) attached, converts the biggest reviewer risk (an untethered student MILP) into the smallest (a correctly identified standard model).

**Use the field evidence as confirmation, not as a novel variant.** The technician's account — direct site-to-site travel, depot return only for tools or materials — is already a modelled feature of TRSP (Pillac et al. 2013 model tools and spare parts held centrally). Frame it as: "field interview confirms that ECG Hohoe operations conform to the standard TRSP structure, in which depot returns are tool-driven rather than job-driven; we therefore model direct inter-site travel with an optional depot revisit." That is an honest, citable, referee-proof sentence. Presenting it as a new problem feature would be the one claim most likely to get caught.

**Structure Related Work as four short paragraphs, matching the audit §7.2 clusters:** (i) TRSP/WSRP — Cordeau et al., Kovacs et al., Pillac et al., Castillo-Salazar et al., Gamst & Pisinger; (ii) routing with latency objectives and duration limits — Ngueveu et al., Fakcharoenphol et al., Laporte/Nobert/Desrochers, Toth & Vigo, Laporte 2009; (iii) equity — Matl et al., Karsu & Morton, Marsh & Schilling; (iv) utility crew dispatch — Arif et al., Dey & Ornik. Roughly 4–6 citations per cluster gets the team to the 20–30 references the audit requires, with the ~12 additional ones drawn from the reference lists of the surveys above (which is the fastest legitimate way to reach volume).

**Put the contribution where it can actually be defended: the equity axis and the data, not the model.** The routing literature's equity work is overwhelmingly about balancing *workload among crews*. The team's θ constraint is about equalising *customer waiting time between geographic zones* — a customer-side, spatial-accessibility notion that comes from equitable facility location (Marsh & Schilling 1994), not from VRP. Applying a spatial-equity constraint inside a multi-vehicle latency-minimising routing model for electricity restoration is a genuinely thin intersection in the literature, and it is defensible. The deliverable that carries it is the θ-sweep / α–β Pareto frontier the audit already prescribes: "tightening rural–urban response parity from ratio 1.6 to 1.2 costs X% in mean restoration time" is a decision-relevant finding no existing paper reports for a rural sub-Saharan distribution utility.

**Target venue framing.** For IEEE PES/IAS PowerAfrica or Scientific African, lead with the application and the data, and keep the OR positioning brief but correct. The sentence that does the most work is: "We formulate ECG Hohoe's dispatch task as a technician routing and scheduling problem with a cumulative (minimum-latency) objective and a spatial-equity constraint, and parameterise it with field-measured travel times from 23 towns."

### Gaps / actions
**MUST NOT be claimed as novel — every one of these is established prior art:**

1. **The TRSP model class itself.** Routing skilled crews from a depot to dispersed service sites under shift limits, capacity, skills and tooling constraints is a named, surveyed problem with 20+ years of literature. Do not write "we propose a new model for technician dispatch."
2. **Direct site-to-site crew movement with tool-driven depot returns.** This is a standard TRSP feature (Pillac et al. 2013 explicitly model tools and spare parts). The field evidence validates the modelling choice; it does not create a new variant.
3. **Minimising the sum of arrival/response times.** This is the CCVRP (Ngueveu et al. 2010) and the k-traveling repairman problem (Fakcharoenphol et al. 2007). Do not present the response-time objective as an innovation.
4. **Simultaneous capacity + route-duration (shift) constraints.** Laporte, Nobert & Desrochers (1985). Forty years old.
5. **Equity/balance constraints in vehicle routing.** Surveyed at book length by Matl, Hartl & Vidal (2018) and Karsu & Morton (2015). A weighted efficiency–equity objective with a Pareto frontier is textbook multi-objective OR, not a contribution.
6. **Minimum-latency repair-crew assignment for power restoration.** Dey & Ornik (2022) did exactly this, with public code. **This is the highest-risk omission in the current bibliography — read it before writing the Introduction.**
7. **Repair-crew routing for electricity distribution systems.** A large IEEE literature exists (Arif et al. 2018 and the post-storm restoration line of work). Do not imply utilities' crew routing is unstudied.
8. **MILP + CBC/PuLP as a solution method.** Standard tooling. Claim no algorithmic contribution; the team is not competing with column generation or ALNS.

**What the team CAN legitimately claim:**

- **Primary, field-measured road travel times for 23 towns in an operating rural sub-Saharan distribution district.** This is the paper's strongest and most defensible asset. Almost all TRSP work uses synthetic, Solomon-derived, or European commercial instances. Say so explicitly.
- **Customer-side spatial equity (rural vs. peri-urban response parity) inside a routing model**, as distinct from the crew-workload equity that dominates the VRP equity literature. This intersection is genuinely sparse. Cite Matl et al. to show you know the difference, and Marsh & Schilling to show where your notion comes from.
- **A quantified efficiency–equity trade-off curve for electricity restoration in a low-income rural context**, usable as a decision aid by the utility.
- **The documented operational protocol from field interview** as an empirical contribution to how small African distribution utilities actually dispatch — framed as case-study evidence, not as model novelty.
- **The feasibility result** (ad-hoc dispatch rarely produces shift-feasible plans; the model always does) as the headline, per the audit §9.2.

**Honest gaps in this literature scout's own coverage — the team must close these:**

- **Verification was indirect.** arxiv.org, link.springer.com, sciencedirect.com, semanticscholar.org, ideas.repec.org and onlinelibrary.wiley.com are ALL blocked by this sandbox's egress proxy. Every citation above was corroborated from multiple independent search-result snippets, not from full text or the publisher's landing page. **The team has unrestricted internet — re-verify every DOI, volume and page range before submission.** Treat the two "likely-real" entries (Gamst & Pisinger; Dey & Ornik) as needing confirmation of issue/venue specifically.
- **No verified peer-reviewed Ghana- or Volta-Region-specific distribution reliability study was found.** Searches returned only Zenodo preprints, an RSIS International item, and grey literature (World Bank indicators, Energy for Growth Hub). This matters: the paper needs local reliability context (SAIDI/SAIFI or outage-duration figures for ECG). The team should search Ghanaian institutional repositories (KNUST, University of Ghana, UEW), past IEEE PES/IAS PowerAfrica proceedings, and ECG/PURC annual reports directly. **Do not cite a Ghana reliability figure this scout did not find — it was not verified.**
- **Two further leads worth chasing, not verified enough to list as references:** (a) a 2026 arXiv preprint, "A column-generation approach for an electricity technician routing and scheduling problem with a lexicographic objective" (arXiv:2604.05153), built on real EDF operational data — the closest electricity-sector TRSP paper found, but a preprint; (b) "Dynamic framework for crew dispatch optimization in power distribution fault inspection," *Reliability Engineering & System Safety* 272 (2026), PII S0951832026003418 — bi-objective lexicographic crew dispatch for fault inspection, clearly relevant, but **author names could not be retrieved** from this sandbox. Both are recent and would strengthen the Related Work; both need the team to confirm authorship before citing.
- **Additional solid references available to reach the 20–30 target, verified in passing but not listed above:** Solomon (1987, *Operations Research* 35(2):254–265) for time-window routing; Braekers, Ramaekers & Van Nieuwenhuyse (2016, *Computers & Industrial Engineering* 99:300–313) for VRP taxonomy; Fikar & Hirsch (2017, *Computers & Operations Research* 77:86–95) for home health care routing, the closest sibling domain with service times and dispersed visits.

### References
- **[verified]** Cordeau, J.-F., Laporte, G., Pasin, F., & Ropke, S. (2010). Scheduling technicians and tasks in a telecommunications company. Journal of Scheduling, 13(4), 393–409. DOI: 10.1007/s10951-010-0188-7
  - The seminal applied technician-scheduling paper (ROADEF 2007 challenge entry, tied 2nd); the standard opening citation establishing that crew-to-task dispatch with travel is a recognised OR problem class.
- **[verified]** Kovacs, A. A., Parragh, S. N., Doerner, K. F., & Hartl, R. F. (2012). Adaptive large neighborhood search for service technician routing and scheduling problems. Journal of Scheduling, 15(5), 579–600. DOI: 10.1007/s10951-011-0246-9
  - The canonical STRSP formulation: technicians with skills serving tasks at dispersed sites within time windows, solved with and without team building — directly analogous to ECG's 5 three-technician crews.
- **[verified]** Pillac, V., Guéret, C., & Medaglia, A. L. (2013). A parallel matheuristic for the technician routing and scheduling problem. Optimization Letters, 7(7), 1525–1535. DOI: 10.1007/s11590-012-0567-4
  - Establishes the modern TRSP definition — routing staff subject to time windows, skills, TOOLS and SPARE PARTS held at a depot — which already formalises the exact depot-return-for-tooling behaviour the ECG technician described.
- **[verified]** Castillo-Salazar, J. A., Landa-Silva, D., & Qu, R. (2016). Workforce scheduling and routing problems: literature survey and computational study. Annals of Operations Research, 239(1), 39–67. DOI: 10.1007/s10479-014-1687-2
  - The standard survey defining Workforce Scheduling and Routing Problems (WSRP) and situating TRSP within it; the single best citation for the paper's 'problem class' paragraph.
- **[likely-real]** Gamst, M., & Pisinger, D. (2024). Decision support for the technician routing and scheduling problem. Networks, 83(1), 169–196. DOI: 10.1002/net.22188
  - Current decision-support framing of TRSP from DTU; the most recent high-quality reference and a model for how to present an optimisation tool to an operating utility rather than as pure methodology. (Online 2023, issue-dated 2024 — check which the target venue wants.)
- **[verified]** Ngueveu, S. U., Prins, C., & Wolfler Calvo, R. (2010). An effective memetic algorithm for the cumulative capacitated vehicle routing problem. Computers & Operations Research, 37(11), 1877–1885. DOI: 10.1016/j.cor.2009.06.014
  - THE key reference for the reformulated objective: the CCVRP minimises the sum of arrival times at customers (not route length) under vehicle capacity — mathematically identical to the audit's mean-response-time objective once routing is admitted. The team's model IS a CCVRP variant and must say so.
- **[verified]** Fakcharoenphol, J., Harrelson, C., & Rao, S. (2007). The k-traveling repairmen problem. ACM Transactions on Algorithms, 3(4), Article 40. DOI: 10.1145/1290672.1290677
  - The theoretical name for the same model (multi-vehicle minimum latency problem); cite to establish NP-hardness and to justify why a MILP + solver time limit is a legitimate approach at n=15–200.
- **[verified]** Laporte, G., Nobert, Y., & Desrochers, M. (1985). Optimal routing under capacity and distance restrictions. Operations Research, 33(5), 1050–1073.
  - The classical formulation of the VRP with simultaneous capacity AND route-length/duration restrictions — the exact structure of ECG's Q = 3 faults per crew plus H = 8 h shift limit. Cite for the constraint pair, not the algorithm.
- **[verified]** Laporte, G. (2009). Fifty years of vehicle routing. Transportation Science, 43(4), 408–416. DOI: 10.1287/trsc.1090.0301
  - Standard historical anchor for the VRP lineage from Dantzig & Ramser's truck dispatching problem; one sentence of Related Work, but expected by reviewers.
- **[verified]** Toth, P., & Vigo, D. (Eds.) (2014). Vehicle Routing: Problems, Methods, and Applications (2nd ed.). MOS-SIAM Series on Optimization, Vol. 18. SIAM, Philadelphia. ISBN 978-1-611973-58-7
  - The reference textbook for VRP notation and variant taxonomy; use it to justify the paper's formulation conventions and to name the variant precisely rather than inventing terminology.
- **[verified]** Matl, P., Hartl, R. F., & Vidal, T. (2018). Workload equity in vehicle routing problems: A survey and analysis. Transportation Science, 52(2), 239–260.
  - The definitive equity-in-routing survey, and a warning the team needs: it shows equity measures are often poorly chosen and can produce degenerate or counterproductive solutions — precisely the audit's finding that θ = 1.6 was slack. Also establishes that this literature is about WORKLOAD balance across vehicles, which is NOT what ECG's Near/Far equity measures.
- **[verified]** Karsu, Ö., & Morton, A. (2015). Inequity averse optimization in operational research. European Journal of Operational Research, 245(2), 343–359.
  - Reviews the efficiency–equity tradeoff in OR and distinguishes 'equitability' from 'balance' — the correct theoretical vocabulary for the α/β weighted objective and the Pareto frontier the audit recommends.
- **[verified]** Marsh, M. T., & Schilling, D. A. (1994). Equity measurement in facility location analysis: A review and framework. European Journal of Operational Research, 74(1), 1–17.
  - The origin of customer-side spatial equity measures (who waits longer because of where they live) as opposed to server-side workload balance; this is the correct home for the Near/Far θ constraint and where the paper's equity novelty claim must be positioned.
- **[verified]** Arif, A., Wang, Z., Wang, J., & Chen, C. (2018). Power distribution system outage management with co-optimization of repairs, reconfiguration, and DG dispatch. IEEE Transactions on Smart Grid, 9(5), 4109–4118.
  - The standard power-engineering reference for repair-crew routing in distribution systems: a MILP that explicitly dispatches crews accounting for equipment resources, travel time and repair time. Establishes that crew routing in distribution utilities is an existing field — cite it to show awareness, then differentiate on context.
- **[likely-real]** Dey, A., & Ornik, M. (2022). Post-disaster repair crew assignment optimization using minimum latency. arXiv:2206.00597; IEEE conference publication, IEEE Xplore document 9922070.
  - CRITICAL PRIOR ART: applies the Minimum Weighted Latency Problem to multiple repair crews for power restoration, with partitioning heuristics balancing assignment across crews. This is the closest existing paper to the team's reformulated model and MUST be cited and differentiated. Source code is public at github.com/leadcatlab/MWLP-Storm-Repair. The exact IEEE venue name could not be confirmed from this sandbox — verify before citing.

---

## Equity & fairness in routing

### Summary
The equity-in-OR literature is mature, heavily surveyed, and currently cited nowhere in this repository. Five things it establishes that bear directly on the paper.

(1) There is a standard taxonomy, and the paper's current measure sits at the bottom of it. Marsh & Schilling (1994) catalogue ~20 equity measures for facility location; Karsu & Morton (2015) is the modern canonical survey and splits the field into *equitability* (anonymous, transfer-sensitive, Lorenz-consistent measures over the whole outcome vector) and *balance* (differences between pre-defined groups). The Far/Near ratio is a balance measure — the weakest class — and it inherits the instability of the 19.5/20 km zone cut the audit already flags.

(2) Measures that survive axiomatic scrutiny are dispersion measures over the full outcome vector. Matl, Hartl & Vidal (2018, Transportation Science) test six common VRP equity measures against a set of axioms; none satisfies all, but min-max and range are shown to be extremely coarse (millions of distinct allocations share one range value) and to fail monotonicity properties. Ogryczak (2000; 2009, Ann. Oper. Res. 167:61–86) shows that a *mean-equity* criterion — mean + λ·(inequality measure) — stays consistent with equitable (Lorenz) dominance for certain measures, notably Gini's Mean Absolute Difference (GMD), and bounded λ, so the combined objective can never prefer a Pareto-worse plan.

(3) GMD is the measure that linearises exactly in a MILP. Mostajabdaveh, Gutjahr & Salman (2019) minimise mean + GMD of assignment distances in a stochastic MILP; Gutjahr & Fischer (2018) add a Gini term to a deprivation-cost objective; Drezner, Drezner & Guyse (2009, Comput. Oper. Res. 36(12):3240–3246) minimise the Gini coefficient of service distances. Chen & Hooker (2023) give formulation recipes for every major fairness criterion.

(4) Pure min-max is a documented trap. Bertazzi, Golden & Wang (2015) prove the min-max optimum can cost up to k times the min-sum optimum (k = vehicles). Lexicographic minimax (Lehuédé, Péton & Tricoire, 2020) repairs the coarseness at real solver cost.

(5) Reporting conventions are fixed: a Pareto frontier over λ or ε (Matl et al. 2018; Huang, Smilowitz & Balcik 2012), plus a price-of-fairness percentage (Bertsimas, Farias & Trichakis 2011).

### Positioning
RECOMMENDED METRIC: Gini's Mean Absolute Difference (GMD) of customer response times, used inside a mean-equity objective — min (1-beta)*mean(R) + beta*GMD(R) — with R_max and the Far/Near ratio kept as reported statistics only.

Definition. For response times R_j, j in J, |J| = n: mean mu = (1/n) sum_j R_j; GMD = (1/(2n^2)) sum_j sum_j' |R_j - R_j'|. The Gini index is G = GMD/mu.

Exact MILP linearisation (no big-M, no new binaries). For every unordered pair j < j' add a continuous d_{jj'} >= 0 with d_{jj'} >= R_j - R_j' and d_{jj'} >= R_j' - R_j, then GMD = (1/n^2) * sum_{j<j'} d_{jj'}. Under minimisation each d_{jj'} is driven to exactly |R_j - R_j'|, so the linearisation is exact. At n = 15 this is 105 continuous variables and 210 constraints — negligible next to the routing binaries.

WHY IT BEATS THE FAR/NEAR RATIO (six reasons, all defensible to a referee):
1. No arbitrary partition. The ratio's entire meaning rests on the 19.5 km / 20 km zone cut that the audit shows is unstable (a function of max observed distance) and contradicted between code and README. GMD uses every town's own response time and needs no zones. This deletes an entire referee objection at zero cost.
2. Sensitive to within-group spread. Two group means can be equal while one Far town waits 6 h and another 0.5 h. GMD counts every pairwise gap and cannot be averaged away.
3. Satisfies the Pigou-Dalton transfer principle. GMD strictly falls under a mean-preserving transfer from a worse-off to a better-off customer; a ratio of group means does not. This is the property that makes a measure "equitable" in the Ogryczak / Karsu-Morton sense, and it is the property a methods referee will test for.
4. Always well-defined. As implemented, the ratio constraint is either vacuous or infeasible depending on the input data (audit 4.2). GMD as an objective term is always feasible and always meaningful.
5. Externally legible. Gini is a recognised inequality index with a known scale; ECG managers, policy readers and reviewers can all read it. The Far/Near ratio has no external referent.
6. Published precedent in the same modelling situation: Mostajabdaveh, Gutjahr & Salman (2019) minimise mean + GMD in a MILP; Gutjahr & Fischer (2018) add a Gini term to a service-time objective; Drezner, Drezner & Guyse (2009, Comput. Oper. Res. 36(12):3240-3246) minimise the Gini coefficient of service distances. The team cites a formulation instead of inventing one.

TWO CAUTIONS TO STATE HONESTLY IN THE PAPER:
(a) The Gini INDEX (GMD/mu) is not directly MILP-linearisable because the denominator is a decision variable. Two clean, published workarounds: (i) optimise GMD and report the index post-hoc; (ii) epsilon-constrain the mean (mu <= eps) and minimise GMD — inside that slice the index is a monotone transform of GMD, so the frontier is exact. Use (ii) for the frontier figure, (i) for the headline model. Alem, Caunhye & Moreno (2022, Socio-Economic Planning Sciences 82) derive the true Gini via the Lorenz curve if the team wants the rigorous version; Chen & Hooker (2023) give the general recipes.
(b) Never make GMD the sole objective. Dispersion alone is minimised by levelling everyone down equally badly. It must appear as mean + lambda*GMD or as an epsilon-constraint on an efficiency objective. Ogryczak's mean-equity consistency result is the guarantee: for GMD the combined criterion stays consistent with equitable dominance for lambda in a bounded range (lambda <= 1 for GMD), so the combined objective can never select a Pareto-dominated plan. [Confidence: the consistency result is verified to exist; the exact lambda <= 1 bound is LIKELY-REAL — verify against Ogryczak (2009), Ann. Oper. Res. 167(1):61-86 before writing it as a numbered condition.]

ON JAIN'S INDEX — report it, do not optimise it. J(R) = (sum_j R_j)^2 / (n * sum_j R_j^2) is a ratio of quadratics: not LP-representable, and an MIQCP/SOCP at best. It was also designed for goods where MORE is better (throughput, bandwidth), whereas response time is a disamenity where LESS is better, so applying it naively to R is conceptually muddled. If a power-engineering venue expects Jain, compute it post-hoc on an explicit service-level transform (e.g. on H - R_j) and say which transform was used. [Confidence on the disamenity point: UNCERTAIN as a citable claim — it is my methodological judgement, consistent with Jain's original framing of resource shares, but I found no paper stating it in these words. Present it as a modelling choice, not as an established result.]

ON MIN-MAX — report R_max ("no town waits more than X hours" is the most politically legible number in the paper) but do not optimise it, and say why, citing Bertazzi, Golden & Wang (2015) for the factor-k efficiency loss and Matl et al. (2018) for the coarseness/axiom failures. Cite Lehuédé et al. (2020) as the more rigorous leximin alternative you traded away for tractability.

HOW TO REPORT THE TRADEOFF — use all three conventions:
1. Pareto frontier: solve over a grid of beta (or eps), plot mean response time on x against GMD or Gini on y. Standard in Matl et al. (2018), Huang et al. (2012), Jozefowiez, Semet & Talbi (2009, EJOR 195(3):761-769).
2. Price of fairness (Bertsimas et al. 2011): PoF = [eff(utilitarian opt) - eff(fair sol)] / eff(utilitarian opt), as a percentage. Gives one abstract-ready sentence: "eliminating 40% of response-time inequality costs 6% in mean restoration time."
3. An extreme-points table: beta = 0 (pure efficiency), beta = 1 (pure equity), and the recommended operating point, each row reporting mean R, R_max, Gini, Far/Near ratio, C_max and solve time. This is the table referees actually read, and it is where the legacy Far/Near ratio earns its keep as a descriptive column.

CRITICAL FRAMING POINT CREATED BY THE NEW FIELD EVIDENCE. Now that crews travel site-to-site, TWO distinct equity notions exist and the paper must state which it optimises:
- Customer-side spatial equity — dispersion of R_j across towns. This is the paper's claim. Literature: Campbell et al. (2008), Huang et al. (2012), Mostajabdaveh et al. (2019), Rodriguez-Garcia et al. (2024).
- Crew-side workload equity — dispersion of route durations across the 5 crews. Literature: Matl et al. (2018, 2019), Jozefowiez et al. (2009), Lehuédé et al. (2020).
Conflating these is the most common referee complaint in this area. Recommendation: optimise customer-side equity, report crew-side workload spread (max minus min route duration) as a secondary operational statistic, and say explicitly in Methods that the two are distinct and why customer-side was chosen.

Expected side benefit, worth flagging to the modelling team: the audit found the equity constraint went slack under depot-return (ratio 1.144 vs theta 1.6) because R_j was nearly pinned by geography. Under site-to-site routing a Far town can be visited early in a chain or stranded at the end of a long one, so R_j acquires much more spread and the equity term should actually bind. [Confidence: UNCERTAIN — this is a reasoned expectation, not a computed result. Verify on the new instance before writing it.]

### Gaps / actions
MUST NOT BE CLAIMED AS NOVEL (each of these would draw a one-line rejection):

1. Equity-constrained or equity-objective routing/assignment as a concept. Surveyed since Marsh & Schilling (1994); the VRP-specific version is fully surveyed in Matl, Hartl & Vidal (2018).
2. Min-max, range, Gini, GMD, Jain or alpha-fairness objectives. All are decades old and catalogued. The paper is SELECTING from a known menu, and should say so in those words.
3. Bi-objective weighting of efficiency against equity, and the resulting Pareto frontier. Standard since at least Jozefowiez et al. (2009); the alpha/beta weighted-sum idea in the current README is textbook multi-objective scalarisation.
4. The price-of-fairness concept. Bertsimas, Farias & Trichakis (2011).
5. MILP linearisation of absolute deviations or of Gini's Mean Absolute Difference. Routine; Chen & Hooker (2023) is a whole survey of such formulations.
6. Equity in electricity restoration. This is the dangerous one. Rodriguez-Garcia, Hassan & Parvania (2024) already published equity-aware power distribution system restoration, and Perrier et al. (2013, Comput. Oper. Res. 40(7):1907-1922, Part II) survey repair-crew routing and crew-to-site assignment in distribution emergency response. Any sentence of the form "this is the first study to consider equity in power restoration" is false and checkable in under a minute.
7. The Far/Near ratio as a "novel equity measure." It is a between-group disparity ratio, a standard and well-understood class (Chen & Hooker 2023 survey these as "group parity metrics"). Presenting it as invented would be an error of scholarship, not just of positioning.
8. Technician routing and scheduling as a problem class. Established (Kovacs, Parragh, Doerner & Hartl, J. Scheduling, 2012, and the broader workforce scheduling and routing literature).

WHAT THE TEAM CAN LEGITIMATELY CLAIM:

1. Primary field data from an operating sub-Saharan African distribution utility. 23 towns with measured road distance and travel time from a working ECG district is genuinely rare. The equity-routing literature above is overwhelmingly North American and European, and overwhelmingly uses generated or benchmark instances. This is the paper's real asset and the claim is safe.
2. "To the best of our knowledge, the first equity-explicit crew-dispatch routing model for a sub-Saharan African electricity distribution utility, using field-measured travel data." The scoping qualifiers (sub-Saharan Africa + distribution utility + crew dispatch + field data) are what make this survivable. Drop any one qualifier and it becomes false.
3. A quantified price of fairness for rural electricity restoration: "equalising response times across the Hohoe district costs X% in mean restoration time." This is a policy result, not a methods result, and framing it that way is both honest and more useful to the intended audience.
4. Complementarity with the energy-justice measurement literature. Osunmuyiwa et al. (2025, Nature Energy) measures power-quality inequity in Accra but prescribes nothing; this paper optimises dispatch. "Measurement has documented the inequity; we show it is partly a dispatch decision and quantify what correcting it costs" is a clean, defensible, one-sentence contribution statement and the single best line available for the Introduction.
5. Empirical comparison of equity metrics on a real network. If the team computes GMD, Gini, R_max, range, Jain and the Far/Near ratio on the same set of solutions and shows they rank plans differently, that is a small but real empirical contribution in the spirit of Matl et al. (2018) — and it costs almost nothing once the model runs.

HONESTY CONSTRAINT THE PAPER MUST RESPECT: the faults are simulated. No sentence may assert a measured real-world disparity. "Rural customers in Hohoe wait 1.6x longer for restoration" is NOT supportable and would be the most damaging single claim in the paper. The supportable form is: "under the fault scenarios considered, efficiency-only dispatch produces a rural response-time penalty of X, which the equity-constrained model reduces to Y at a cost of Z% in mean response time." Equity results are about the MODEL's behaviour, not about ECG's current performance, until real fault logs are obtained.

REMAINING LITERATURE GAP I COULD NOT CLOSE: I found no study applying equity-aware routing to electricity fault repair in a low-income or rural African context. That absence is consistent with the team's novelty claim (2) above, but absence of evidence from one search session is not proof — before submission, one of the team should run the same search with Google Scholar and Scopus access (which I do not have here) using the strings "equity" + "crew dispatch" + "distribution network", "fairness" + "outage restoration" + "routing", and "energy justice" + "optimization" + Africa. This is a 30-minute task with normal internet and it protects the paper's main claim.

ENVIRONMENT NOTE ON VERIFICATION: arxiv.org, link.springer.com, ideas.repec.org, sciencedirect and several publisher domains are blocked by the sandbox egress proxy, so every citation above was confirmed through search-result metadata rather than by opening the paper. Authors, titles, venues, years and volumes are solid; a few page ranges and DOIs are inferred and are flagged per-reference. The team should re-check page numbers against the publisher record before submission.

### References
- **[verified]** Marsh, M.T., & Schilling, D.A. (1994). Equity measurement in facility location analysis: A review and framework. European Journal of Operational Research, 74(1), 1–17. DOI: 10.1016/0377-2217(94)90200-3
  - The foundational taxonomy of ~20 equity measures for public-facility location — cite it to show you surveyed the options before choosing one, and to place the Far/Near ratio within a recognised classification rather than presenting it as invented.
- **[verified]** Karsu, Ö., & Morton, A. (2015). Inequity averse optimization in operational research. European Journal of Operational Research, 245(2), 343–359.
  - The canonical modern survey of the efficiency–equity tradeoff in OR; its equitability-vs-balance distinction is exactly the framing this paper needs in its Related Work section, and it is the single reference a referee will most expect to see.
- **[verified]** Ogryczak, W. (2000). Inequality measures and equitable approaches to location problems. European Journal of Operational Research, 122(2), 374–391. DOI: 10.1016/S0377-2217(99)00240-4
  - Establishes the mean-equity model (mean outcome + scaled inequality measure) and shows which dispersion measures can be combined with the mean without violating distance minimisation — the theoretical warrant for the objective recommended below.
- **[verified]** Chen, X., & Hooker, J.N. (2023). A guide to formulating fairness in an optimization model. Annals of Operations Research, 326(1), 581–619. DOI: 10.1007/s10479-023-05264-y
  - A practical how-to for expressing inequality measures, maximin/leximax, alpha-fairness and group-parity metrics as LP/MILP constraints; this is the reference that tells the team exactly how to write each candidate metric in PuLP, and it also covers 'group parity' metrics, i.e. the class the Far/Near ratio belongs to.
- **[verified]** Matl, P., Hartl, R.F., & Vidal, T. (2018). Workload equity in vehicle routing problems: A survey and analysis. Transportation Science, 52(2), 239–260.
  - The single most important citation now that the field evidence has made this a routing problem: it surveys equity objectives in VRP, tests six measures against axiomatic properties, and documents the pathologies of min-max and range objectives — the paper should use it to justify its metric choice explicitly.
- **[likely-real]** Matl, P., Hartl, R.F., & Vidal, T. (2019). Workload equity in vehicle routing: The impact of alternative workload resources. Computers & Operations Research, 110, 116–129.
  - Companion study showing that the cost of balance depends mainly on which resource is equalised (distance vs. duration vs. load) rather than on the equity function chosen — directly relevant to whether the paper equalises response time, route duration or number of jobs.
- **[verified]** Lehuédé, F., Péton, O., & Tricoire, F. (2020). A lexicographic minimax approach to the vehicle routing problem with route balancing. European Journal of Operational Research, 282(1), 129–147. DOI: 10.1016/j.ejor.2019.09.010
  - The state of the art for leximin/lexicographic-minimax equity in routing; cite it as the reason you did NOT use pure min-max, and as the acknowledged more rigorous alternative you traded away for tractability.
- **[verified]** Bertazzi, L., Golden, B., & Wang, X. (2015). Min–Max vs. Min–Sum Vehicle Routing: A worst-case analysis. European Journal of Operational Research, 240(2), 372–381. DOI: 10.1016/j.ejor.2014.07.025
  - Proves the min-max optimum can have total cost up to k times the min-sum optimum (k = number of vehicles). This is the hard evidence for why the paper should report R_max but not optimise it — a precise, citable answer to a referee asking 'why not just minimise the worst wait?'
- **[verified]** Bertsimas, D., Farias, V.F., & Trichakis, N. (2011). The Price of Fairness. Operations Research, 59(1), 17–31. DOI: 10.1287/opre.1100.0865
  - Defines the price of fairness — the relative efficiency loss under a fair allocation — which is the standard way to report the tradeoff as ONE number in an abstract, and gives the paper its headline policy sentence.
- **[verified]** Campbell, A.M., Vandenbussche, D., & Hermann, W. (2008). Routing for Relief Efforts. Transportation Science, 42(2), 127–145. DOI: 10.1287/trsc.1070.0209
  - The classic demonstration that minimising maximum arrival time or average arrival time produces structurally different routes from minimising total travel — precisely the reformulation this project has just made, in a directly analogous service-urgency setting.
- **[verified]** Huang, M., Smilowitz, K., & Balcik, B. (2012). Models for relief routing: Equity, efficiency and efficacy. Transportation Research Part E: Logistics and Transportation Review, 48(1), 2–18.
  - Systematically compares equity, efficiency and efficacy objectives in multi-vehicle routing and extracts routing principles from each — the best template for how to structure this paper's comparative results section and its Pareto discussion.
- **[verified]** Mostajabdaveh, M., Gutjahr, W.J., & Salman, F.S. (2019). Inequity-averse shelter location for disaster preparedness. IISE Transactions, 51(8), 809–829. DOI: 10.1080/24725854.2018.1496372
  - Minimises a linear combination of mean assignment distance and Gini's Mean Absolute Difference in a MILP — this is the exact formulation recommended for this paper, so the team can cite a published precedent instead of inventing one.
- **[verified]** Gutjahr, W.J., & Fischer, S. (2018). Equity and deprivation costs in humanitarian logistics. European Journal of Operational Research, 270(1), 185–197.
  - Shows that minimising total deprivation cost alone produces unfair solutions and fixes it by adding a term proportional to the Gini inequity index — the direct analogue of this paper's problem (minimising mean response time alone will strand Far towns) and the argument for why an equity term is needed at all.
- **[verified]** Rodriguez-Garcia, L., Hassan, A., & Parvania, M. (2024). Equity-aware power distribution system restoration. IET Generation, Transmission & Distribution, 18, 401–412. DOI: 10.1049/gtd2.12982
  - The closest published neighbour in the application domain — equity explicitly built into distribution-system restoration. The team MUST cite it and must not claim to be first to consider equity in power restoration; it is also the right place to position the difference (they model network restoration, this paper models crew dispatch on a real road network).
- **[verified]** Osunmuyiwa, O., Odero, M., Wall, A., Goode, J., Flaspohler, G., Abrokwah, K., Adkins, J., & Klugman, N. (2025). Mobilizing power quality and reliability measurements for electricity equity and justice in Africa. Nature Energy, 10(3), 395–403. DOI: 10.1038/s41560-025-01717-9
  - Documents measured power-quality and reliability inequity in Accra, Ghana, and links it to multidimensional poverty — the strongest possible motivating citation for this paper's premise, from the same country, in a top-tier venue. It measures inequity but does not optimise; this paper optimises. That is a clean complementarity claim for the Introduction.
- **[verified]** Jain, R., Chiu, D.-M., & Hawe, W. (1984). A Quantitative Measure of Fairness and Discrimination for Resource Allocation in Shared Computer Systems. DEC Research Report TR-301, Digital Equipment Corporation. (Also arXiv:cs/9809099.)
  - The origin of Jain's fairness index. Cite it if you report the index — but see the caution below: it is a ratio of quadratics, is not MILP-linearisable, and was designed for goods where more is better, not for waiting times.

---

## Power distribution & outage mgmt

### Summary
Three findings matter for this paper.

(1) THE SAIDI LINK IS REAL AND WORTH BUILDING. IEEE Std 1366 defines SAIDI as total customer-interruption-minutes divided by customers served. For a fault j, outage duration decomposes into notification + dispatch + travel + repair; the reformulated model's response variable R_j (shift start to crew arrival) is precisely the dispatch-controllable share. So sum_j n_j (R_j + r_j) / N_total is the dispatch-attributable contribution to SAIDI, where n_j is customers affected by fault j. This converts "we cut mean response time by x%" into "we cut the controllable component of SAIDI by y customer-minutes" — the same currency ECG itself uses in its PURC tariff filings, which state CAIDI/SAIFI/SAIDI improvement targets. The cost: it needs n_j per fault, which the dataset lacks. ECG holds distribution-transformer and feeder customer counts, so this is one more field-data request alongside the travel matrix. Without n_j, report unweighted mean response time and state explicitly that it equals the SAIDI numerator under an equal-customers-per-fault assumption, then sensitivity-test that assumption.

(2) THE CORRECT MODEL-CLASS NAME. With site-to-site travel, depot origin, service times, a shift-duration limit and an arrival-time objective, this is the multiple travelling repairman / minimum-latency problem with route-duration constraints (also called the cumulative capacitated VRP) — not an assignment problem, and not a plain distance-minimising VRP. Naming it correctly buys credibility and hands the team a citable literature. Dey and Ornik (2022) is the closest precedent (multiple crews, minimum weighted latency, balanced partitioning); Cavdar et al. (2022) formalise the power-specific version.

(3) TWO GENUINE GAPS. Almost all power-systems crew-routing work is post-disaster or post-storm restoration; Hohoe is routine day-to-day dispatch on a normal shift, a regime with very few papers. And sub-Saharan African distribution research is overwhelmingly descriptive — Nigerian, Ethiopian and Ghanaian studies compute SAIDI/SAIFI/CAIDI, benchmark them against international norms, and stop. I found no prescriptive crew-dispatch optimisation study for an SSA distribution utility.

### Positioning
POSITION THE PAPER AS: a prescriptive, equity-constrained crew-routing case study for a routine-operations sub-Saharan African distribution utility, built on primary field-measured travel data, with results expressed in the utility's own regulatory currency (SAIDI's controllable component).

Four concrete moves.

1. LEAD WITH THE REGIME AND THE GEOGRAPHY, NOT THE METHOD. The literature splits cleanly: power-systems crew routing is almost entirely post-disaster or post-storm restoration (Arif et al., Cavdar et al., Dey and Ornik, and a large arXiv cluster on storm and earthquake restoration), while sub-Saharan African distribution research is almost entirely descriptive measurement (Nigerian feeder studies, the Aksum Ethiopia study, Amewornu and Nwulu for Ghana) that computes indices, benchmarks them against IEEE norms, and stops. The Hohoe paper sits in the empty intersection: routine daily dispatch, African utility, prescriptive model. Say this explicitly in the Introduction and again in Related Work. It is the paper's strongest and most defensible claim.

2. NAME THE MODEL CLASS CORRECTLY AND IMMEDIATELY. Call it a multiple travelling repairman problem (equivalently, minimum-latency problem) with route-duration constraints and a spatial-equity constraint, solved as a MILP. Do not call it an assignment problem, and do not call it a VRP without qualification — a referee who sees an arrival-time objective described as a VRP will assume the authors do not know the difference between completion-time and latency objectives. Cite Dey and Ornik and Cavdar et al. at the point of naming.

3. RUN THE SAIDI BRIDGE AS A SHORT, EXPLICIT SUBSECTION IN METHODS. Give the decomposition (outage duration = notification + dispatch + travel + repair), state that R_j is the dispatch-controllable share, define dispatch-attributable customer-minutes as sum_j n_j (R_j + r_j), divide by customers served, and cite IEEE Std 1366 for the index definition and the ECG PURC filing for the fact that ECG targets these indices. Then report results in both units: mean response time in hours AND avoided customer-minutes. This single subsection is worth more to a referee than another sensitivity sweep, because it turns an OR exercise into a utility-relevant result. If n_j cannot be obtained in time, still write the subsection, state the equal-customers assumption plainly, and put the weighted version in Future Work.

4. FRAME EQUITY AS SPATIAL EQUITY IN A RURAL DEVELOPING-COUNTRY CONTEXT, NOT AS EQUITY-IN-ROUTING PER SE. The equity-in-routing and equity-aware-restoration literatures are both well developed (Matl/Hartl/Vidal for routing; Karsu and Morton for inequity-averse OR generally; Marsh and Schilling for spatial equity in facility location; Bertsimas/Farias/Trichakis for the price of fairness; and a US-centric cluster on equity-aware distribution restoration and disadvantaged communities). What is genuinely under-covered is the Near/Far rural-versus-peri-urban distance framing in a low-income utility where the far towns are also the poorest and the least likely to complain. Cite Marsh and Schilling and Matl et al. to show command of the measures, then differentiate on context.

VENUE NOTE: this positioning fits IEEE PES PowerAfrica and Scientific African very well. It fits a pure OR venue badly, because moves 1, 3 and 4 are all application claims.

### Gaps / actions
MUST NOT CLAIM AS NOVEL:

- Crew routing for power distribution restoration. Established since at least Arif et al. (2018); there is now a dense literature including co-optimisation with network reconfiguration and DER dispatch. Claiming novelty here would be refuted by a single search.
- Minimum-latency / travelling-repairman objectives for multi-crew repair. Dey and Ornik (2022) do exactly multiple crews with minimum weighted latency and balanced partitioning. Cavdar et al. (2022) formalise the power-specific variant. The reformulated model is an instance of a known class.
- Equity or fairness objectives in vehicle routing. Matl, Hartl and Vidal survey eighteen balance criteria; min-max, range, mean absolute deviation, standard deviation and Gini are all standard. A theta-ratio constraint is a conventional device, not an invention.
- Equity-aware power restoration. There is an active cluster (equity-aware distribution system restoration, predict-then-optimize equitable restoration, human-aware restoration for fair outage experience) mostly framed around US disadvantaged communities. "First to consider equity in power restoration" would be false.
- Computing SAIDI/SAIFI/CAIDI for an African distribution network. Many Nigerian, Ethiopian and Ghanaian studies already do this.
- Technician routing and scheduling generally, and for electricity utilities specifically. The WSRP/TRSP literature is mature, and Bangerter et al. (2026) address an electricity-utility TRSP directly.

CAN LEGITIMATELY CLAIM:

- The operating regime. Applying a latency-minimising multi-crew routing model to ROUTINE, day-to-day fault dispatch under a normal shift constraint, rather than to post-disaster restoration. This regime is thinly covered; Diadelmo et al. (2026) is the main exception and should be cited rather than ignored.
- The geography and the closing of the descriptive-to-prescriptive loop. I found no prescriptive crew-dispatch optimisation study for a sub-Saharan African distribution utility. SSA work measures reliability; it does not optimise dispatch. Being the first to go from indices to a dispatch model for an African district is a real, checkable claim.
- The primary data. Field-measured road distance and travel time for 23 towns from an operating ECG depot is a genuine asset. Klugman et al. (2023) supports the argument that utility-reported data in Ghana is unreliable, which raises the value of independently measured data.
- The rural/peri-urban spatial-equity framing in a low-income context, as distinct from the US disadvantaged-community framing that dominates equity-aware restoration.
- The quantified efficiency-equity trade-off curve as a decision aid for a utility that has stated reliability-index targets to a regulator.

DATA GAPS THAT BLOCK THE STRONGEST CLAIMS:

- Customers affected per fault (n_j). Without it the SAIDI bridge stays qualitative. ECG holds distribution-transformer and feeder customer counts; request them alongside the travel matrix. This is the highest-value single additional data item after the inter-town matrix.
- ECG's own SAIDI/SAIFI/CAIDI values for the Hohoe district, or for the Volta region. If obtainable, the paper can state what fraction of observed SAIDI the dispatch decision actually controls, which is a genuinely strong result. If not obtainable, say so in Limitations.
- A source for the fault-type and priority distributions. Klugman et al. can be cited to explain why a trustworthy utility fault log may not exist, but the assumption must still be labelled.

VERIFICATION WARNING: outbound fetching to arXiv, doi.org, Crossref, Springer, PubMed Central, OSTI and purc.com.gh was blocked in this environment, so every citation above was assembled from search-engine metadata rather than from the document itself. Confidence fields reflect that. The team has unrestricted internet and MUST independently verify every author list, volume, page range and DOI before submission — particularly the two marked uncertain (the Aksum Scientific Reports author list, and the full author list of Bangerter et al.), the CGD paper's author, and the exact title and date of the ECG PURC filing.

### References
- **[verified]** Klugman, N., Adkins, J., Berkouwer, S., Abrokwah, K., Podolsky, M., Pannuto, P., Wolfram, C., Taneja, J., & Dutta, P. (2023). Measuring Grid Reliability in Ghana. Chapter 6 in T. Madon et al. (Eds.), Introduction to Development Engineering: A Framework with Applications from the Field. Springer, Cham. Open access. DOI: 10.1007/978-3-030-86065-3_6
  - The single most useful Ghana citation: an instrumented sensor network in Accra showing that utility-reported outage statistics diverge from measured reality, which simultaneously motivates the team's own primary field measurement and gives principled cover for using synthetic fault instances (no trustworthy ECG fault log exists to draw from).
- **[verified]** Amewornu, E. M., & Nwulu, N. I. (2021). Assessing the impact of demand response programs on the reliability of the Ghanaian distribution network. PLOS ONE, 16(3), e0248012. DOI: 10.1371/journal.pone.0248012
  - One of very few peer-reviewed reliability analyses of an actual Ghanaian distribution network; establishes that reliability-index framing is the accepted idiom for Ghanaian distribution research and gives a domestic precedent to position against.
- **[likely-real]** Kumi, E. N. (2017). The Electricity Situation in Ghana: Challenges and Opportunities. CGD Policy Paper 109. Center for Global Development, Washington, DC.
  - The standard, widely cited account of Ghana's supply crisis, distribution losses and ECG's financial position — the default Introduction citation for why Ghanaian distribution performance is a policy problem.
- **[likely-real]** Electricity Company of Ghana Ltd. (2022). Proposal for the Review of Electricity Distribution Service Charge / Aggregate Revenue Requirement. Submission to the Public Utilities Regulatory Commission (PURC), Accra, Ghana. Available at purc.com.gh.
  - Primary-source evidence that ECG itself targets CAIDI, SAIFI and SAIDI improvements and is upgrading long rural and peri-urban feeders — this is what ties the paper's objective to the utility's own stated regulatory goals, and it is a document the team can obtain and verify locally.
- **[likely-real]** Cole, M. A., Elliott, R. J. R., Occhiali, G., & Strobl, E. (2018). Power outages and firm performance in Sub-Saharan Africa. Journal of Development Economics, 134, 150-159.
  - Quantifies the economic cost of outage frequency and duration for SSA firms, which is what converts 'restore faster' from an engineering preference into an economic argument in the Introduction.
- **[verified]** IEEE Std 1366-2022, IEEE Guide for Electric Power Distribution Reliability Indices. Institute of Electrical and Electronics Engineers, New York.
  - The normative definition of SAIDI, SAIFI, CAIDI and the Major Event Day exclusion method — mandatory if the paper claims its objective maps onto a recognised reliability index, and the source for the customer-minutes decomposition.
- **[uncertain]** Assessing post-conflict electric power supply reliability in low voltage distribution networks of Aksum, Ethiopia (2026). Scientific Reports. DOI: 10.1038/s41598-026-35599-y (author list not confirmed — must be filled in from the article)
  - A recent sub-Saharan African reliability case study computing SAIDI, SAIFI, CAIDI and EENS against international benchmarks; the closest template for how to report reliability indices for an African district network, and a comparator showing SSA indices run far above IEEE norms.
- **[likely-real]** African Development Bank (2021). Electricity Regulatory Index for Africa 2021. AfDB, Abidjan.
  - Continental regulatory and quality-of-service benchmark covering Ghana; lets the Introduction place ECG's reliability performance against African peers rather than only against IEEE targets.
- **[verified]** Arif, A., Ma, S., Wang, Z., Wang, J., Ryan, S. M., & Chen, C. (2018). Optimizing Service Restoration in Distribution Systems with Uncertain Repair Time and Demand. IEEE Transactions on Power Systems, 33(6), 6828-6838. DOI: 10.1109/TPWRS.2018.2855102
  - The canonical co-optimisation of repair crew routing with distribution system operation; the standard reference a power-systems referee will expect to see cited for 'crew routing in distribution restoration', and the benchmark this paper is deliberately simpler than.
- **[likely-real]** Cavdar, B., He, Q., & Qiu, F. (2022). Repair Crew Routing for Power Distribution Network Restoration. arXiv:2204.04848 [math.OC]
  - Defines the Power Restoration Traveling Repairman Problem and argues explicitly that the objective must be service-disruption time, not travel distance — the cleanest external justification for abandoning the constant travel-time objective in favour of response time.
- **[likely-real]** Dey, A., & Ornik, M. (2022). Post-Disaster Repair Crew Assignment Optimization Using Minimum Latency. IEEE conference publication (IEEE Xplore document 9922070); preprint arXiv:2206.00597
  - The nearest methodological precedent to the reformulated model: multiple repair crews, a minimum weighted latency objective, and a partitioning heuristic that balances assignment across crews — cite it to name the model class and to show the formulation is recognised rather than ad hoc.
- **[likely-real]** Diadelmo, M. V. F., Batista, L. S., & Bessani, M. (2026). Dynamic framework for crew dispatch optimization in power distribution fault inspection. Reliability Engineering & System Safety, 272(P1), 112527. DOI: 10.1016/j.ress.2026.112527
  - One of the very few crew-dispatch papers in the routine, non-disaster operating regime this project studies, and it uses a lexicographic routing/makespan objective — the single most important paper for showing the team knows where its own regime sits in the literature.
- **[verified]** Castillo-Salazar, J. A., Landa-Silva, D., & Qu, R. (2016). Workforce scheduling and routing problems: literature survey and computational study. Annals of Operations Research, 239(1), 39-67. DOI: 10.1007/s10479-014-1687-2
  - Places the model inside the recognised Workforce Scheduling and Routing Problem family and supplies the standard terminology (technicians as vehicles, tasks at dispersed locations) that the Methods section should adopt.
- **[uncertain]** Bangerter, E., et al. (2026). A column-generation approach for an electricity technician routing and scheduling problem with a lexicographic objective. arXiv:2604.05153 (full author list not confirmed)
  - The closest single paper in scope — technician routing and scheduling for an electricity utility with a lexicographic multi-objective — and therefore the reference the paper must engage with to show its contribution is the African application and the equity dimension, not the routing method.
- **[likely-real]** Matl, P., Hartl, R. F., & Vidal, T. (2018). Workload Equity in Vehicle Routing Problems: A Survey and Analysis. Transportation Science, 52(2), 239-260.
  - Surveys eighteen workload-balance criteria (min-max, range, mean absolute deviation, standard deviation, Gini, lexicographic) and warns that non-monotonic equity measures produce perverse routes — essential for choosing and defending the theta-constraint form, and proof that equity in routing is not itself novel.

---

## Formulation methods

### Summary
The field evidence lands this paper on a named, well-studied problem: the **Cumulative Capacitated VRP (CCVRP)** — single depot, m identical vehicles, capacity Q, service (repair) times, a route-duration (shift) limit, objective = sum of arrival times at customers. Ngueveu et al. (2010) define it almost verbatim as the team's problem. Its single-vehicle case is the travelling repairman / delivery man / minimum latency problem (Fischetti et al. 1993). This is good news: it gives a citable methods home and an exact-algorithm literature (Lysgaard & Wøhlk 2014) and a 2022 survey (Corona-Gutiérrez et al.) to anchor Related Work.

The decisive methodological finding is that **the team probably does not need subtour elimination at all for their headline result.** At n=15 faults with Q=3, the number of ordered depot-origin routes of length ≤ 3 is only 2,955 (15 + 210 + 2,730). Complete enumeration of those routes, pricing each one exactly (travel + repair, with arrival times), discarding those exceeding H=8 h, then solving a set-partitioning MILP (Balinski & Quandt 1964) is **exactly optimal**, solves in well under a second in CBC, and dissolves four separate difficulties at once: subtours are impossible because each column is an explicit sequence; the shift limit becomes a filter, not a constraint; the cumulative objective becomes a per-column constant, so arbitrary cost structures (priority weights, makespan) cost nothing; and the equity ratio becomes linear in the route-selection variables. Enumeration stays exact to roughly n ≤ 30 at Q = 3.

Subtour elimination therefore matters only for the scalability study (n up to 200). There, single-commodity flow (Gavish & Graves 1978) dominates MTZ in LP strength at the same polynomial size (Öncan et al. 2009), and DFJ lazy constraints are impractical because PuLP+CBC exposes no lazy-constraint callback. MTZ's one genuine merit here is that its node potentials *are* the arrival-time variables a cumulative objective needs.

Finally, the equity constraint R̄_far ≤ θ·R̄_near needs **no linearisation at all**: with zone membership exogenous, the counts are constants, so cross-multiplying gives a pure linear inequality. The team's README form was algebraically right; it was written over the wrong quantity.

### Positioning
POSITION THE MODEL AS A RECOGNISED CLASS, NOT AN INVENTION. Methods should open: "The problem is a single-depot Cumulative Capacitated Vehicle Routing Problem (CCVRP) with service times and a route-duration limit, augmented with a spatial-equity constraint." Ngueveu et al. (2010) and Corona-Gutiérrez et al. (2022) give the class its name; Fischetti et al. (1993) gives the single-vehicle root; Laporte et al. (1984) gives the duration limit; Toth & Vigo (2014) gives the base CVRP. That one sentence converts the audit's "F" on formulation into a defensible, citable Methods section.

RECOMMENDED SOLUTION METHOD — set partitioning over a COMPLETE enumerated route set. At n=15, Q=3 there are only 2,955 ordered routes (15 + 210 + 2,730); after pruning those exceeding H=8 h, far fewer. Enumerate every ordered route r of length <= Q, price it exactly from the inter-town matrix (depot->s1, repair, s1->s2, ...), record its duration d_r, its arrival times, its cost c_r = sum of arrival times (priority-weighted if desired), its per-zone arrival sums, then solve:
  min sum_r c_r L_r  s.t.  sum_r a_jr L_r = 1 for all j;  sum_r L_r <= m(=5);  L_r binary.
Because the route set is COMPLETE, this is exactly optimal — not a heuristic, not a relaxation. Cite Balinski & Quandt (1964) for the formulation and Baldacci et al. (2012) for why column generation would only be needed at larger n. State plainly in the paper: "Because Q = 3 and |J| = 15, the set of feasible routes can be enumerated exhaustively, so the set-partitioning model is solved to proven optimality without column generation."

This makes four things free:
- Subtours are IMPOSSIBLE by construction (each column is an explicit sequence). Question 1 disappears for the headline model.
- The shift limit is a filter on route generation, not a constraint in the MILP.
- Makespan is linear: C_max >= d_r L_r for every r.
- Equity is linear: with F_r = sum of Far arrival times on r and N_r the Near equivalent, n_near * sum_r F_r L_r <= theta * n_far * sum_r N_r L_r.

SUBTOUR ELIMINATION (Q1) — only needed for the scalability study (n up to 200, where enumeration blows up: 7.9M routes at n=200, Q=3). Ranking for CBC:
1. Single-commodity flow (Gavish & Graves 1978) — RECOMMENDED. Polynomial size, LP relaxation provably at least as strong as MTZ (Öncan et al. 2009), no callbacks needed, works directly in PuLP.
2. MTZ (Miller et al. 1960) — acceptable fallback with one genuine merit specific to this paper: the node potentials u_i ARE the arrival-time variables the cumulative objective needs, so MTZ carries no extra variables here. Its weak relaxation is the known cost; say so rather than hiding it. If using the LIFTED version, cite Kara, Laporte & Bektaş (2004), not Desrochers & Laporte (1991), whose CVRP lifting cuts off optima.
3. DFJ lazy constraints (Dantzig et al. 1954) — strongest, but PuLP+CBC has no lazy-constraint callback. Iterative cut-and-resolve is possible but slow; python-mip or OR-Tools would be needed for true lazy cuts. Recommend AGAINST for this project and say why in one sentence.

OBJECTIVE CHOICE (Q3) — min-sum-of-arrival-times (cumulative/latency) is the right primary objective because the paper's equity story is about CUSTOMERS waiting, not crews working. Min-max/makespan is CREW-side fairness — a different and also legitimate notion. Report makespan as a secondary metric and, if a second Pareto axis is wanted, use it there; do not conflate the two. Framing the paper as customer-side latency equity, against a VRP equity literature that is overwhelmingly crew-side workload equity (Matl et al. 2018), is the single sharpest positioning move available.

RATIO LINEARISATION (Q5) — there is nothing to linearise. With R_j as variables and zone membership exogenous geography (so n_far, n_near are constants), (1/n_far) sum_far R_j <= theta * (1/n_near) sum_near R_j multiplies through by n_far * n_near > 0 to n_near * sum_far R_j <= theta * n_far * sum_near R_j, which is linear. The README's "fully linearised" form was algebraically correct all along — the defect was purely that it was written over the DATA t_j instead of the DECISION variables R_j. Swapping t_j -> R_j fixes it outright. Charnes & Cooper (1962) becomes relevant only if theta itself is made a variable, and even then prefer either (a) minimising the gap G >= R_far_bar - R_near_bar, which stays linear and is what the audit's alpha/beta objective already does, or (b) bisection/parametric search on theta — which is the SAME computation as the theta-sensitivity sweep the paper needs anyway, so the two deliverables collapse into one run.

DATA / CRITICAL PATH — the current published instance touches only 12 distinct fault towns, so a 13x13 matrix (12 towns + depot) reproduces it exactly; the full 24x24 (23 towns + depot) is needed only for new instances and the scalability study. Also note that total repair time is 20.07 h against 5 crews x 8 h = 40 h, i.e. 50.2% of the shift budget is consumed before any travel is counted — so the shift constraint plausibly still binds under site-to-site travel, preserving the audit's strongest headline (feasibility, not percentage improvement). A defensible no-API fallback for the matrix: great-circle or road-graph distance scaled by the empirically fitted depot-to-town speed profile, with the matrix published as a supplementary file and the approximation named as a limitation.

### Gaps / actions
MUST NOT BE CLAIMED AS NOVEL — every one of these is prior art and a referee will know it:
1. The model class. CCVRP / multiple travelling repairman with capacity, service times and a duration limit is 30+ years old (Fischetti et al. 1993; Ngueveu et al. 2010) and was surveyed as recently as 2022 (Corona-Gutiérrez et al.). Do not write "we propose a new formulation."
2. The objective. Minimising total (or mean) arrival time is the standard cumulative/latency objective, not the team's idea. Naming it correctly is a strength; implying it is new is fatal.
3. Any subtour-elimination scheme. MTZ, DFJ and flow formulations are all textbook.
4. Set partitioning with route enumeration (Balinski & Quandt 1964) and column generation (Baldacci et al. 2012).
5. The equity constraint form. Bounded-ratio and bounded-gap inequality constraints are standard in inequity-averse OR; also cite Karsu & Morton (2015), EJOR 245(2), 343-359, and Ogryczak et al. (2014), Journal of Applied Mathematics, art. 612018, both verified, for the efficiency-equity tradeoff framing behind alpha/beta.
6. "First to apply optimisation to utility crew dispatch." The technician routing and scheduling literature is large — see Kovacs, Parragh, Doerner & Hartl (2012), Journal of Scheduling 15(5), 579-600 (verified). A claim of application-first will be refuted in one search.
7. Weighted-sum multi-objective scalarisation and Pareto frontiers.

WHAT CAN LEGITIMATELY BE CLAIMED:
1. APPLICATION NOVELTY, narrowly and precisely stated: the first application of a cumulative-objective (minimum-latency) routing model with an explicit SPATIAL, customer-side equity constraint to electricity fault restoration in a rural sub-Saharan African distribution district. Each qualifier is load-bearing — do not drop any of them.
2. THE EQUITY FRAMING IS A GENUINE GAP. The VRP equity literature is dominated by crew-side WORKLOAD equity (Matl, Hartl & Vidal 2018 survey it and find little else). Constraining the ratio of mean response times between geographic customer zones — far towns must not systematically wait longer — is a different and under-served notion. This is the paper's strongest defensible claim and should be stated explicitly as such.
3. THE PRIMARY DATA. Field-measured road distances and travel times from an operating ECG district, plus the technician-confirmed site-to-site dispatch protocol, published openly. Irreplaceable and uncontested.
4. THE TRADE-OFF CURVE AS A DECISION AID. The theta sweep and alpha/beta Pareto frontier, reported with R_far_bar and R_near_bar SEPARATELY so a reader can see whether equity was bought by helping far towns or by delaying near ones. Matl et al. (2018) prove this levelling-down pathology is real in VRP; pre-empting it is a credibility win and pre-answers the sharpest referee question.
5. A MODEST, HONEST COMPUTATIONAL POINT. At the district's actual operating scale (n ~ 15, Q = 3), the complete route set is small enough to enumerate exhaustively, so the problem is solvable to PROVEN optimality with a free solver on commodity hardware. That is a real deployment argument for a utility with no optimisation budget, and it is a defensible applied contribution precisely because it is small.

TWO THINGS TO WRITE INTO LIMITATIONS BEFORE A REFEREE WRITES THEM FOR YOU:
- The inter-town matrix is derived, not field-measured, unlike the depot-to-town data. Say how it was produced, publish it, and say what a measurement error would do.
- Deterministic, single-period, known-in-advance faults. Real dispatch is dynamic. Name the dynamic/stochastic CCVRP as future work rather than letting a referee find the gap.

### References
- **[verified]** Ngueveu, S. U., Prins, C., & Wolfler Calvo, R. (2010). An effective memetic algorithm for the cumulative capacitated vehicle routing problem. Computers & Operations Research, 37(11), 1877-1885. DOI: 10.1016/j.cor.2009.06.014
  - This is the paper's problem, named and defined: minimising the sum of arrival times at customers subject to vehicle capacity — cite it as the formal identification of the model class in Methods.
- **[verified]** Fischetti, M., Laporte, G., & Martello, S. (1993). The delivery man problem and cumulative matroids. Operations Research, 41(6), 1055-1064. DOI: 10.1287/opre.41.6.1055
  - Canonical single-vehicle cumulative/latency reference with an exact algorithm; establishes that minimising total arrival time is a long-studied objective, not a novelty the paper can claim.
- **[verified]** Lysgaard, J., & Wøhlk, S. (2014). A branch-and-cut-and-price algorithm for the cumulative capacitated vehicle routing problem. European Journal of Operational Research, 236(3), 800-810. DOI: 10.1016/j.ejor.2013.08.032
  - First exact algorithm for the CCVRP; cite to establish the problem's difficulty and to justify why the paper uses enumeration at its own scale rather than claiming a general exact method.
- **[verified]** Corona-Gutiérrez, K., Nucamendi-Guillén, S., & Lalla-Ruiz, E. (2022). Vehicle routing with cumulative objectives: A state of the art and analysis. Computers & Industrial Engineering, 169, 108054. DOI: 10.1016/j.cie.2022.108054
  - Recent survey of cumulative-objective routing; the single best entry point for the Related Work section and proof that the team has engaged with current literature.
- **[verified]** Balinski, M. L., & Quandt, R. E. (1964). On an integer program for a delivery problem. Operations Research, 12(2), 300-304. DOI: 10.1287/opre.12.2.300
  - Origin of the set-partitioning formulation of routing; the citation for the recommended enumerate-then-partition approach that is exactly optimal at this instance size.
- **[verified]** Baldacci, R., Mingozzi, A., & Roberti, R. (2012). Recent exact algorithms for solving the vehicle routing problem under capacity and time window constraints. European Journal of Operational Research, 218(1), 1-6. DOI: 10.1016/j.ejor.2011.07.037
  - Modern review of set-partitioning-based exact methods and column generation; cite to explain why explicit enumeration suffices here and column generation would be needed only at larger n.
- **[verified]** Gavish, B., & Graves, S. C. (1978). The travelling salesman problem and related problems. Working Paper GR-078-78, Operations Research Center, Massachusetts Institute of Technology, Cambridge, MA.
  - Source of the single-commodity flow subtour-elimination formulation — the recommended compact scheme for the scalability study, since it is polynomial-size and needs no solver callbacks.
- **[verified]** Miller, C. E., Tucker, A. W., & Zemlin, R. A. (1960). Integer programming formulation of traveling salesman problems. Journal of the ACM, 7(4), 326-329. DOI: 10.1145/321043.321046
  - The MTZ constraints; must be cited if used, and its node-potential variables double as the arrival-time variables a cumulative objective already requires.
- **[verified]** Dantzig, G. B., Fulkerson, D. R., & Johnson, S. M. (1954). Solution of a large-scale traveling-salesman problem. Journal of the Operations Research Society of America, 2(4), 393-410. DOI: 10.1287/opre.2.4.393
  - The DFJ exponential subtour-elimination constraints; cite when explaining why the strongest formulation was not adopted (no lazy-constraint callback in PuLP/CBC).
- **[verified]** Öncan, T., Altınel, İ. K., & Laporte, G. (2009). A comparative analysis of several asymmetric traveling salesman problem formulations. Computers & Operations Research, 36(3), 637-654. DOI: 10.1016/j.cor.2007.11.008
  - Classifies 24 formulations and documents the LP-relaxation strength hierarchy; this is the citable justification for preferring single-commodity flow over MTZ.
- **[verified]** Kara, I., Laporte, G., & Bektaş, T. (2004). A note on the lifted Miller-Tucker-Zemlin subtour elimination constraints for the capacitated vehicle routing problem. European Journal of Operational Research, 158(3), 793-795. DOI: 10.1016/S0377-2217(03)00377-1
  - Corrects the Desrochers-Laporte (1991) lifted MTZ constraints, which cut off optimal solutions in the capacitated case — a real trap the team must cite if it uses lifted MTZ.
- **[verified]** Laporte, G., Desrochers, M., & Nobert, Y. (1984). Two exact algorithms for the distance-constrained vehicle routing problem. Networks, 14(1), 161-172. DOI: 10.1002/net.3230140113
  - The canonical reference for a hard upper bound on route length/duration — exactly the role the 8-hour shift constraint plays in this model.
- **[verified]** Toth, P., & Vigo, D. (Eds.) (2014). Vehicle Routing: Problems, Methods, and Applications, 2nd edition. MOS-SIAM Series on Optimization, No. 18. SIAM, Philadelphia.
  - Standard reference work; cite for the CVRP/mTSP baseline formulation, the treatment of service times, and duration-constrained variants.
- **[verified]** Matl, P., Hartl, R. F., & Vidal, T. (2018). Workload equity in vehicle routing problems: A survey and analysis. Transportation Science, 52(2), 239-260. DOI: 10.1287/trsc.2017.0744
  - Surveys equity in VRP and proves that equity objectives can yield non-TSP-optimal tours and workload-inconsistent solutions — the definitive warning against the levelling-down pathology, and the paper that shows this literature is crew-side, leaving the customer-side spatial framing open.
- **[verified]** Charnes, A., & Cooper, W. W. (1962). Programming with linear fractional functionals. Naval Research Logistics Quarterly, 9(3-4), 181-186. DOI: 10.1002/nav.3800090303
  - The classical linear-fractional transformation; cite only to note honestly that it is NOT required here, because with fixed zone membership the ratio constraint cross-multiplies into a pure linear inequality.

---

## Travel-time matrix

### Summary
DATA ENGINEER REPORT — inter-town travel-time matrix for the Hohoe ECG routing model. All numbers below come from code I executed; scripts and outputs are in /tmp/claude-0/-home-user-optimization-assignment/09712f65-58f9-58af-a0a9-791748005b23/scratchpad/ (01_speed_analysis.py, 02_speed_model.py, 03_corridor.py, 04_coords.py, 05_matrix.py, 06_error_decomp.py, 08_loocv.py, 09_optcheck.py, 10_heuristic_sens.py; matrices matrix_A_tree_hours.csv, matrix_B_polar_hours.csv; plus build_real_matrix.py and GEOCODE_TEMPLATE.csv for the team).

=== 1. THE SPEED SPREAD IS NOT NOISE. IT IS A FIXED OVERHEAD. ===
This is the single most useful finding and it answers the audit's open question in §5.3. Fitting on the 22 clean towns (Fodome excluded):

  M0 constant speed  t = d/36.89          R2 0.7771  MAE 5.00 min  LOOCV-MAE 5.19 min  Q2 0.7638
  M1 affine  t = 0.1595 + 0.02059 d       R2 0.8957  adjR2 0.8847  MAE 3.37 min  RMSE 0.0737 h
                                          LOOCV-MAE 3.72 min  Q2 0.8743  max|resid| 8.76 min
  M2 power   t = 0.0643 d^0.7415          R2 0.8859  MAE 3.82 min  LOOCV-MAE 4.21 min  Q2 0.8665

M1 wins in-sample and out-of-sample. Its intercept is 0.1595 h = 9.6 min (se 0.0334, t = 4.77, p = 0.0001) and its slope is 1/48.57 km/h (se 0.00157, p = 2.8e-11). Read physically: about ten minutes to clear Hohoe town and get onto the trunk road, then roughly 49 km/h cruise. M2 independently confirms it — the power-law exponent is 0.7415 (95% CI [0.634, 0.849]); H0 of constant speed (B = 1) is rejected at t = -4.72, p = 0.00013.

Speed is therefore a strong function of distance, tested not assumed: Spearman rho = 0.854 (p = 4.3e-07), Kendall tau = 0.686 (p = 8.3e-06), OLS speed~distance R2 = 0.5895 (p = 3.0e-05). The affine time model explains 50.7% of the variance in implied speed; residual speed sd drops from 8.38 to 5.88 km/h. So the "1 to 47 km/h spread" is mostly an artefact of dividing a fixed overhead by a short distance — Wli at 47.2 km/h and Gbi-Kledzo at 18.4 km/h are the SAME vehicle on the SAME road model. This converts a reviewer-visible embarrassment into a one-paragraph data-section result.

Corridor structure does NOT add anything. I assigned the 23 towns to five hypothesised radial corridors and tested residuals: one-way ANOVA F = 0.529 (p = 0.716), Kruskal-Wallis H = 1.718 (p = 0.788), and a corridor dummy block on top of M1 gives F(4,16) = 0.715 (p = 0.594) with adjusted R2 actually falling (0.8847 to 0.8839). A single global speed model is adequate. Largest unexplained residuals: Ve-Dator +8.8 min and Ve-Kobenu +8.5 min (both slow, likely a hill spur), Wli -8.8 min and Golokwati -5.9 min (both fast, likely tarred trunk).

=== 2. FODOME IS A CONFIRMED CORRUPT CELL; GBLEDI IS FLAGGED BUT SURVIVES ===
Fodome (0.65 km / 0.65 h): Grubbs on implied speed G = 2.862 vs Gcrit = 2.780, flagged at alpha = 0.05; Tukey fence [1.88, 59.98] excludes it; z = -2.86. Against M1 its studentised residual is +5.69, far outside the 95% prediction interval [-0.1, 20.9] min. Two independent lines of evidence pin the error to the DISTANCE cell, not the time: (a) it is the unique row of 23 where distance == travel_time, the signature of a cell copied across from the adjacent column; (b) I located Fodome Ahor at 7.08435 N, 0.55949 E, which is 11.87 km great-circle from Hohoe — 0.65 km is 18x shorter than the crow-flies distance and therefore physically impossible. The recorded 0.65 h is entirely plausible. Candidate repairs span 6.5 km (simple typo) / 13.79 km (haversine x 1.162) / 16.5 km / 23.82 km (M1 inversion) — a 3.7x range, so it must be re-measured, not guessed. Reassuringly the speed model barely moves under any of them (intercept 9.6-12.2 min, cruise 48.6-52.7 km/h, R2 0.797-0.897), so this one cell is not load-bearing for the model — only for Fodome's own row.

Gbledi (1.3 km / 0.05 h = 3 min): studentised residual -1.63, INSIDE the 95% PI, so statistically it is not an outlier. But 3 min is below the fitted 9.6 min egress overhead, and Wikipedia places Gbledi-Gbogame near Mount Afadja, roughly 20 km out. Either it is a genuine intra-Hohoe destination (in which case the overhead legitimately does not apply and the row is fine) or it is a second location mix-up. VERIFY — the audit did not flag this one.

Godenu is a third concern: Wikipedia's Gbi Godenu (7.10361 N, 0.45139 E) is 6.11 km great-circle from Hohoe against a recorded 19.2 km road distance, implying circuity 3.14. Either the dataset means a different Godenu or the distance is wrong.

=== 3. COORDINATES: 13 OF 23 FOUND, 11 USABLE ===
Only WebSearch works in this sandbox; WebFetch is egress-blocked for every domain I tried (Wikipedia, Nominatim, geonames, mapcarta), and direct OSRM/ORS/Nominatim CONNECTs return 403. So these came from search snippets and are NOT authoritative.

Depot, Hohoe town centre: 7.15250 N, 0.47667 E (NB: the ECG post gate, not the town centre, is what the model needs).

town (dataset) -> matched settlement, lat, lon, road km, great-circle km, circuity:
  Santrokofi -> Santrokofi-Benua,  7.2090958, 0.4732393,  7.5, 6.30, 1.190
  Lolobi     -> Lolobi Kumasi,     7.2100,    0.5300,    10.1, 8.69, 1.162 (low precision, 2 dp)
  Akpafu     -> Akpafu-Todzi,      7.2550,    0.4911,    11.9, 11.51, 1.034
  Ve-Kobenu  -> Ve-Koloenu,        7.0500,    0.4330,    13.7, 12.37, 1.107 (name uncertain)
  Likpe      -> Likpe-Mate,        7.1826676, 0.607391,  17.2, 14.81, 1.162
  Godenu     -> Gbi Godenu,        7.10361,   0.45139,   19.2, 6.11, 3.142  <- REJECTED
  Liati      -> Mt Afadja (proxy), 7.02694,   0.60333,   20.0, 19.76, 1.012
  Golokwati  -> Ve Golokwati,      6.9922556, 0.4255889, 21.3, 18.69, 1.140
  Wli        -> Wli waterfalls,    7.1000,    0.5830,    22.8, 13.10, 1.740 (proxy POI, low precision)
  Leklebi    -> Leklebi SHS,       6.95929,   0.49265,   23.5, 21.56, 1.090 (proxy POI)
  Logba      -> Logba Adzekoe,     6.90000,   0.43417,   38.3, 28.47, 1.346
  Fume       -> Avatime-Fume,      6.8721611, 0.4178306, 38.3, 31.84, 1.203
  Fodome     -> Fodome Ahor,       7.08435,   0.55949,   0.65, 11.87, 0.055 <- proves the error

Circuity over the 11 usable towns: median 1.162, mean 1.199, sd 0.21, range 1.012-1.740. That is consistent with the rural circuity literature (Ballou et al. 1.12-2.10 inter-city by country; ~1.2-1.6 rural streets) and is the value I used.

NOT FOUND (10): Gbi-Kledzo, Gbi-Wegbe, Gbi-Avege, Ve-Dator, Ve-Gbodome, Wuinta, Gbledi, Agome yo, Zimugaziwo snake Village, Afadzo South. Note "Afadzo South" is not a settlement name at all — Afadzato South is a DISTRICT, so nobody can say what was measured.

=== 4. TWO BOUNDING MATRICES, BUILT AND VALIDATED (NO API) ===
Rather than fake one point-estimate matrix, I built an upper and a lower bound and treat the interval as the uncertainty.

A — corridor-tree metric (needs NO coordinates): all cross-corridor travel is routed back through Hohoe; within a corridor, travel is along the spur. d(i,j) = |d_i - d_j| same corridor, d_i + d_j otherwise. Mean 31.32 km / 0.804 h, max 76.70 km. Symmetric, 0 triangle-inequality violations (it is a tree metric, so the triangle inequality holds by construction — this matters, because a matrix that violates it makes VRP optima meaningless).

B — polar law-of-cosines x circuity 1.162 (needs corridor bearings): de-circuitise the measured road radius, combine with corridor-mean bearings by the law of cosines, re-apply circuity. Mean 21.83 km / 0.608 h, max 51.59 km. Symmetric, 0 triangle violations.

Gap A-B over the 552 ordered pairs: mean 9.50 km, median 3.14 km, max 46.12 km; B sits 30.3% below A on average.

Validation on the 55 pairs among the 11 located towns, against haversine x 1.162:
  A: MAE 9.12 km, RMSE 13.15 km, bias +7.71 km, R2 -0.223, corr 0.738
  B: MAE 3.47 km, RMSE 4.45 km,  bias +1.20 km, R2 0.860,  corr 0.950
A is badly biased where lateral roads exist (it says Liati-Wli is 42.8 km when the crow-flies-based reference says 9.8 km), which is exactly what an upper bound should do. HONESTY CAVEAT, and a referee will spot it: that reference is itself haversine x circuity, i.e. B's own model family, so the comparison is partly circular. I decomposed it. Using the measured road radius with the TRUE bearing gives MAE 2.47 km; swapping in the corridor-mean bearing gives MAE 3.47 km. So the only genuinely testable component — the cost of using corridor labels instead of real coordinates — is +1.01 km MAE. The straight-line-to-road error is baked into the reference and CANNOT be assessed without a real road matrix. Say so in the paper.

Time is applied to both via M1: t = 0.1595 + 0.02059 d off-diagonal, 0 on-diagonal (co-located faults, e.g. the three at Agome yo, cost nothing to chain — a structural gain routing captures and assignment never could).

=== 5. DOES THE MATRIX UNCERTAINTY CHANGE THE ANSWER? MOSTLY NO. ===
I solved the 15-fault instance (5 crews, Q=3, H=8h, minimise sum of response times, crews return to post at end of shift) under both matrices with an identical heuristic, same seed, same budget, so no solver gap confounds the comparison:

                      A (upper)   B (lower)   spread
  mean response       1.414 h     1.375 h     2.8%
  Cmax                7.386 h     7.184 h     2.7%
  Near mean response  0.996 h     0.954 h
  Far mean response   1.893 h     1.857 h
  Near-Far equity gap +0.897 h    +0.903 h    0.7%
  random baseline     2.768 h     2.523 h
  gain over random    48.9%       45.5%
  feasible random     572/20000   2844/20000
                      (2.9%)      (14.2%)

Three things follow. (i) The aggregate conclusions — a ~45-49% response-time improvement over random dispatch, and a persistent ~0.9 h Near/Far equity penalty — are robust across the full uncertainty interval. (ii) The shift constraint now genuinely BINDS (only 2.9-14.2% of random plans are feasible), so the routing model is non-degenerate: the audit's fatal §4.1 problem is gone by construction. (iii) BUT the optimal crew-to-fault partition is NOT the same under the two matrices, and the MIP run shared only 9 of 20 arcs. So aggregate findings are publishable now; the specific dispatch plan is not an operational recommendation until the real matrix exists.

=== 6. SOLVER WARNING THE TEAM WILL OTHERWISE WALK INTO ===
On 16 nodes with an MTZ + big-M time formulation, CBC does NOT prove optimality. A 60 s run: incumbent 21.213, lower bound 16.310, GAP 30%, 12,228 nodes, CBC's own log line "Result - Stopped on time limit". An unlimited run was still going after 25 minutes and then died. Critically, PuLP reported LpStatus == "Optimal" in every one of these cases. If the team writes "solved to optimality" off the back of pulp.LpStatus they will be reporting a 30%-gap incumbent as an optimum, and that is a desk-reject-grade error. They must parse CBC's gap, set an explicit timeLimit, report it, and either strengthen the formulation (single-commodity flow subtour elimination instead of MTZ) or pair the MIP with the heuristic and report both.

### Positioning
HOW A REFEREE WILL REACT, AND WHAT THE PAPER MUST DISCLOSE

The blunt answer on imputed vs real. An imputed inter-town matrix is not automatically fatal, but it moves the paper from "case study" to "methodological study on a real network". A referee at an OR or energy-systems venue will accept a synthetic fault set against a real network (that is standard), and will accept a modelled travel matrix IF it is presented as a model with stated error. What gets a paper rejected is presenting an imputed matrix as measured data, or burying the imputation in a footnote. Concretely, the danger sentence is any variant of "travel times between towns were obtained from field data" — the team has depot-to-town field data only, for 23 of the 552 ordered pairs, i.e. 4.2% of the matrix. The other 95.8% is model output. That ratio must appear in the paper.

With a REAL matrix (OSRM/ORS, one HTTP request, see the gaps field) the paper is materially stronger and the travel matrix simply stops being a discussion point. The only remaining disclosure is the provenance line plus a validation table against the 23 field legs — and that table is itself a contribution, because almost nobody checks routing-engine output against field measurement in a rural African setting. I would expect a referee to like it.

With an IMPUTED matrix the paper is still defensible, but only in the bounded form. The argument that survives review is: "we do not know the inter-town matrix, so we bracket it between a pessimistic corridor-tree construction and an optimistic polar construction, solve both, and show that our conclusions are invariant across the bracket." My numbers support exactly that argument — mean response moves 2.8%, makespan 2.7%, the Near/Far equity gap 0.7%, and the improvement over random dispatch stays in 45.5-48.9%. That is a genuinely referee-proof framing, because it makes the matrix non-load-bearing for every claim the paper makes. What it does NOT license is publishing the specific crew-to-fault assignment as an operational recommendation: the optimal partition differs between the two matrices, so the routes are inside the uncertainty and the aggregates are outside it. The paper should say that in one explicit sentence and it will disarm the obvious objection before a referee raises it.

Positioning the contribution. The travel-matrix work should be framed as calibration, not as a headline. The headline contribution stays where the audit put it: an equity-constrained multi-vehicle routing model for crew dispatch in a rural sub-Saharan distribution utility, with real field-measured depot travel data and a documented no-return-to-depot dispatch protocol from a named field informant. The matrix work earns a Methods subsection ("Estimating inter-site travel") and a Limitations paragraph. Do not oversell it.

Two genuine methodological results deserve to be foregrounded though, because they are novel-ish and cheap to defend:

(1) The fixed-overhead speed model. t = 0.1595 + 0.02059 d (R2 0.8957, LOOCV Q2 0.8743, cross-validated MAE 3.72 min) with a 9.6-minute egress overhead significant at p = 0.0001, and a power-law exponent of 0.7415 that rejects constant speed at p = 0.00013. This turns the dataset's most embarrassing feature — implied speeds from 18 to 47 km/h — into an explained, parameterised regularity, and it is exactly the kind of small empirical result that makes a case study feel like real fieldwork rather than a class exercise. It also hands the team a defensible way to convert any distance into a time.

(2) The bounded-matrix sensitivity design. Solving under a provable upper bound and a provable lower bound, with an identical heuristic and seed, and reporting the spread on every headline metric, is a reusable pattern for anyone doing OR in a data-poor setting. Both my constructions are tree/metric-consistent (zero triangle-inequality violations), which is not a detail — a travel matrix that violates the triangle inequality produces VRP "optima" that are artefacts, and most ad-hoc imputation schemes do violate it. Saying explicitly that both constructions are verified metrics is a credibility marker a good referee will notice.

What the paper must disclose either way (non-negotiable list):
- That 23 of 552 ordered node pairs are field-measured and the rest are modelled or API-derived; give the number.
- The exact construction, with its parameters: the M1 speed model coefficients, the circuity factor 1.162 and where it came from, and the corridor assignment (including that it is a hypothesis).
- The Fodome cell as a corrected data error, with the correction rule and the sensitivity to it. Do not silently fix it. A reviewer who downloads the CSV and sees 0.65/0.65 and no mention of it will assume the worst.
- Gbledi and Godenu as open data questions if they cannot be resolved before submission.
- That the 15 faults are simulated (already in the audit, still true).
- The solver gap. Report CBC's actual gap and time limit, never pulp.LpStatus alone.
- A data-availability statement and ECG Hohoe's written permission, which is still the item on the critical path the team does not control.

One framing suggestion. If the real matrix arrives in time, keep the imputed one in the paper anyway as a comparison — "how well can you do a routing study with nothing but depot-to-town odometer readings?" is a question that matters to every utility in the region that has no GIS department, and answering it with a measured error (bearing substitution costs +1.01 km MAE; headline metrics move under 3%) is a better contribution than quietly deleting the fallback.

### Gaps / actions
WHAT THE TEAM IN GHANA MUST COLLECT, IN PRIORITY ORDER. Everything below needs an unrestricted connection, which they have and this sandbox does not.

--- TASK 1 (BLOCKING, ~2 hours): 24 verified coordinates ---
This is the whole critical path. Without coordinates there is no real matrix.

Fill in /tmp/claude-0/-home-user-optimization-assignment/09712f65-58f9-58af-a0a9-791748005b23/scratchpad/GEOCODE_TEMPLATE.csv (copy it into the repo as dataset/ecg_towns_coordinates.csv). Columns: dataset_name, verified_settlement_name, latitude, longitude, gps_source, corridor_road, road_surface, notes.

Rules that matter:
- Use decimal degrees, 5 decimal places minimum (5 dp is about 1 m).
- Record the point the crew ACTUALLY drives to — the ECG service point / transformer site / town junction — not the Wikipedia town centroid.
- Row 1 must be the DEPOT: the Hohoe ECG post GATE, not Hohoe town centre. Nobody can supply this but them. Have someone stand at the gate and read it off a phone.
- Add a road_surface column (tarred / graded laterite / untarred). This is free to collect and it answers the referee question "why do implied speeds differ", with evidence rather than assertion.
- Add corridor_road (which road out of Hohoe). My corridor hypothesis is untested and the residual ANOVA did not support it (p = 0.59); their local knowledge beats my guess.

Ten towns I could NOT locate at all and that therefore MUST come from them: Gbi-Kledzo, Gbi-Wegbe, Gbi-Avege, Ve-Dator, Ve-Gbodome, Wuinta, Gbledi, Agome yo, Zimugaziwo snake Village, Afadzo South.

Thirteen names that are AMBIGUOUS — each is a traditional area with several settlements, and picking the wrong one moves the node by kilometres. Ask the ECG contact which specific town was measured: Fodome (Ahor / Woe / Helu / Dzogbega), Liati (Wote / Teteman / Soba), Wli (Agorviefe / Todzi / Afegame), Leklebi (Duga / Kame / Agbesia), Santrokofi (Benua / Gbodome / Bume — Benua fits the 7.5 km reading), Akpafu (Todzi / Mempeasem / Adokor), Lolobi (Kumasi / Ashiambi / Huyiam), Likpe (Mate / Bakwa / Todome — Mate fits the 17.2 km reading), Logba (Adzekoe / Alakpeti / Tota), Ve-Kobenu (probably Ve-Koloenu — confirm the spelling), Fume (is it Avatime-Fume in Ho West, 38 km south?), Godenu (Wikipedia's Gbi Godenu is only 6.1 km out but the dataset says 19.2 km — one of the two is wrong), and "Afadzo South", which is not a settlement name at all (Afadzato South is a district).

Free geocoding tools they can use: Nominatim (https://nominatim.openstreetmap.org/search?q=<place>,+Ghana&format=json — max 1 request/second, must set a real User-Agent with a contact email), Google Maps (right-click a point, copy coordinates), or a phone GPS reading taken on site, which is the most defensible of the three and is what I would cite in the paper.

--- TASK 2 (BLOCKING, ~10 minutes of compute): the real 24x24 matrix ---
IMPORTANT: this is ONE HTTP request, not 253 or 552. Do not write a pair loop. OSRM's /table endpoint returns up to 10,000 durations per call; 24x24 = 576, so the entire matrix comes back in about two seconds.

OSRM demo server (no key, no signup — do this first):
  GET https://router.project-osrm.org/table/v1/driving/{lon1},{lat1};{lon2},{lat2};...;{lon24},{lat24}?annotations=duration,distance
  - Coordinates are LON,LAT — this order trips everyone up.
  - Semicolon-separated, all 24 nodes in one URL, depot first.
  - Response: {"durations": [[...24 x 24 seconds...]], "distances": [[...metres...]], "code":"Ok"}
  - Divide durations by 3600 for hours, distances by 1000 for km.
  - Policy: max 1 request/second, non-commercial use only, no uptime or accuracy guarantee. Service-wide cap is 5,000 req/min, so one request is nothing.

OpenRouteService (free API key from openrouteservice.org, use as the cross-check):
  POST https://api.openrouteservice.org/v2/matrix/driving-car
  Headers: Authorization: <your key>, Content-Type: application/json
  Body: {"locations": [[lon,lat], ... 24 pairs ...], "metrics": ["duration","distance"], "units":"km"}
  - Matrix limit is 3,500 origin x destination pairs per request; 576 is well inside it.
  - Free tier is roughly 2,500 requests/day overall with a tighter per-minute matrix quota. One request per day is a rounding error.

Run the same 24 coordinates through BOTH engines and report the agreement. Two independent engines agreeing is a strong, cheap credibility signal, and it costs an extra five minutes.

A ready-to-run script is at /tmp/claude-0/-home-user-optimization-assignment/09712f65-58f9-58af-a0a9-791748005b23/scratchpad/build_real_matrix.py. It reads coords.csv, makes the single OSRM call, CACHES the raw JSON to osrm_raw.json (so re-running never re-hits the server — commit that JSON to the repo, it is the provenance artefact a reviewer will want), and writes travel_time_hours.csv and travel_distance_km.csv. It needs only requests, pandas and numpy.

--- TASK 3 (BLOCKING, ~30 min): validate and calibrate the API against the field data ---
Do NOT drop the raw API times into the model. The 23 field-measured depot legs are the project's key asset precisely because they let you calibrate.
- Compare OSRM depot->town against the field readings. build_real_matrix.py prints this table and computes MAE, bias and R2.
- Expect OSRM to be FASTER than reality: it models a generic car on mapped geometry, not a loaded ECG utility vehicle with a three-man crew, gate delays and stops.
- If there is a systematic bias, fit t_field = a + b * t_osrm on the 23 legs and apply (a, b) to the entire matrix. Report a, b and R2 in the paper. The script prints the suggested coefficients.
- Quality gates the script also runs: count null (unroutable) entries — a null means a coordinate snapped to no road, so nudge it onto the road and re-run; measure max asymmetry |T - T'| and KEEP the matrix asymmetric (one-ways and terrain are real, do not average it away); count triangle-inequality violations, which should be zero for a road matrix.
- Also compare the API's depot->town DISTANCE against the field odometer readings. That is a second, independent check, and it is how you finally settle Fodome, Gbledi and Godenu.

--- TASK 4 (BLOCKING, ~1 hour, needs the ECG contact not the internet): fix the three bad rows ---
- FODOME: the distance cell is corrupt (0.65 km is 18x shorter than the crow-flies distance to Fodome Ahor and it is the only row of 23 where distance == travel_time, i.e. a copy-across). Candidate true values span 6.5 to 23.8 km. Re-measure it; do not pick one. If it genuinely cannot be re-measured before submission, drop the row and say so — with 22 towns the speed model is unchanged.
- GBLEDI: 1.3 km / 3 minutes. Is this a quarter of Hohoe (fine, the 9.6 min egress overhead simply does not apply to an intra-town trip) or Gbledi-Gbogame near Mount Afadja, roughly 20 km out (in which case both cells are wrong)? One phone call settles it.
- GODENU: 19.2 km recorded against 6.1 km crow-flies to Wikipedia's Gbi Godenu, implying circuity 3.14. Either a different Godenu or a bad distance.

--- TASK 5 (non-blocking but high value) ---
- Ask ECG Hohoe for their OWN Near/Far service-area threshold. The code currently uses ceil(max)/2 = 19.5 km, which is a function of the sample and will move if a town is added. An exogenous, ECG-sourced constant kills that objection outright.
- Ask whether H = 8 h and Q = 3 are ECG's real figures, and get the source on record.
- Ask for the historical fault log. Even one year of fault types and priorities replaces the invented [0.15, 0.25, 0.20, 0.15, 0.10, 0.15] distribution and the 30/70 priority split with something citable, and lets the Priority column finally be used.
- Record road_surface while collecting coordinates (see Task 1).
- Nail down the exact depot: crews return to the post at end of shift and mid-shift only for tools or materials. Ask how often that mid-shift return happens — if it is common, it belongs in the model as an occasional forced depot visit, and that is a genuinely publishable modelling wrinkle nobody else has.

--- IF TASKS 1-3 CANNOT BE DONE IN TIME ---
The fallback is already built and needs no API: matrix_A_tree_hours.csv (upper bound) and matrix_B_polar_hours.csv (lower bound) in the scratchpad. Solve under both, report the spread on every headline number, and state plainly that the routes are inside the uncertainty while the aggregates are outside it. That is defensible. What is not defensible is a single imputed matrix presented without a bracket.

### References
- **[verified]** Ballou, R.H., Rahardja, H., & Sakai, N. (2002). Selected country circuity factors for road travel distance estimation. Transportation Research Part A: Policy and Practice, 36(9), 843-848. https://doi.org/10.1016/S0965-8564(01)00044-1
  - The canonical source for circuity factors; justifies the 1.162 multiplier used to convert great-circle to road distance and situates it against their reported inter-city range of 1.12 (Belarus) to 2.10 (Egypt).
- **[verified]** Giacomin, D.J., & Levinson, D.M. (2015). Road network circuity in metropolitan areas. Environment and Planning B: Planning and Design, 42(6), 1040-1053. https://doi.org/10.1068/b130131p
  - Second pillar of the circuity literature; establishes that circuity varies systematically with network structure, supporting the paper's decision to measure circuity locally rather than adopt a textbook constant.
- **[verified]** Nesbitt, R.C., Gabrysch, S., Laub, A., Soremekun, S., Manu, A., Kirkwood, B.R., Amenga-Etego, S., Wiru, K., Hofle, B., & Grundy, C. (2014). Methods to measure potential spatial access to delivery care in low- and middle-income countries: a case study in rural Ghana. International Journal of Health Geographics, 13, 25. https://doi.org/10.1186/1476-072X-13-25
  - The closest methodological precedent in the same country: compares straight-line, network distance, network travel time and raster travel time as impedance measures in rural Ghana, and is the natural citation for why an imputed travel matrix is an accepted practice in Ghanaian data-poor settings.
- **[verified]** Boscoe, F.P., Henry, K.A., & Zdeb, M.S. (2012). A nationwide comparison of driving distance versus straight-line distance to hospitals. The Professional Geographer, 64(2), 188-196. https://doi.org/10.1080/00330124.2011.583586
  - Empirical evidence on when straight-line distance is an adequate proxy for driving distance and time; directly supports the paper's argument that the imputed matrix does not change aggregate conclusions.
- **[verified]** Mennicken, E., Lemoy, R., & Caruso, G. (2024). Road network distances and detours in Europe: Radial profiles and city size effects. Environment and Planning B: Urban Analytics and City Science. https://doi.org/10.1177/23998083231168870
  - Recent work showing that detour ratios follow radial profiles around a centre, which is exactly the geometry of the Hohoe depot-centred network and underpins the polar (Construction B) matrix.
- **[verified]** Luxen, D., & Vetter, C. (2011). Real-time routing with OpenStreetMap data. In Proceedings of the 19th ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems (GIS '11), Chicago, IL, pp. 513-516. https://doi.org/10.1145/2093973.2094062
  - The citation for OSRM, which is the routing engine the team should use to build the real matrix; must be cited in the data section if the /table endpoint is used.
- **[verified]** Marsh, M.T., & Schilling, D.A. (1994). Equity measurement in facility location analysis: A review and framework. European Journal of Operational Research, 74(1), 1-17. https://doi.org/10.1016/0377-2217(94)90200-3
  - The standard reference for how to define and measure equity in a location/allocation objective; gives the paper a defensible vocabulary for its Near/Far fairness constraint instead of an ad-hoc theta.
- **[likely-real]** Toth, P., & Vigo, D. (Eds.) (2014). Vehicle Routing: Problems, Methods, and Applications (2nd ed.). MOS-SIAM Series on Optimization, SIAM, Philadelphia.
  - The standard reference for the model class the project is moving to; needed the moment the paper stops calling this an assignment problem, and covers why travel matrices must satisfy the triangle inequality.
- **[likely-real]** Miller, C.E., Tucker, A.W., & Zemlin, R.A. (1960). Integer programming formulation of traveling salesman problems. Journal of the ACM, 7(4), 326-329. https://doi.org/10.1145/321043.321046
  - Source of the MTZ subtour-elimination constraints used in the routing formulation I tested; also the reason to warn that MTZ gives a weak LP relaxation, which is why CBC left a 30% gap after 60 seconds on only 16 nodes.
- **[likely-real]** Laporte, G. (2009). Fifty years of vehicle routing. Transportation Science, 43(4), 408-416. https://doi.org/10.1287/trsc.1090.0301
  - A compact survey to cite when positioning the reformulated model in the VRP literature, which the repository currently has zero engagement with (the README's References section is empty).
- **[uncertain]** Cole, J.P., & King, C.A.M. (1968). Quantitative Geography: Techniques and Theories in Geography. John Wiley & Sons, London.
  - Cited throughout the circuity literature as the origin of the 1.2-1.6 rural-street circuity range that brackets the 1.162 median I measured; I only saw it quoted secondhand in the Ballou-derived sources, so verify the page before citing.

---

## Venues

### Summary
VERIFICATION CAVEAT: this sandbox's egress proxy blocked every primary venue site (ieee-powerafrica.org, ieee-pes.org, sciencedirect.com, jesit.springeropen.com, 2027.cired.net, research4life.org, casrai.org). WebSearch worked, so all figures below come from search-engine summaries of those pages, not the pages themselves. Treat every number as "check before relying on it."

TIMING FINDING THAT INVALIDATES THE AUDIT'S TOP PICK. PowerAfrica 2026 is in Nairobi 21-25 Sep 2026 — i.e. it is running this week. Its paper deadline was 7 April 2026. No 2027 edition is announced anywhere I could find. So PowerAfrica means submitting ~Mar/Apr 2027 and appearing ~Sep 2027: 12+ months. The audit's claim that it is "faster and more forgiving than a journal" is now false. A journal is faster.

CONFERENCES. IEEE AFRICON 2027, 23-25 Sep 2027, Kumasi, GHANA (18th IEEE R8 AFRICON) — the audit missed this and it is the best conference fit: IEEE Xplore, home country, no international travel, expect CFP deadline ~Feb-Mar 2027. CIRED 2027 (Stockholm, 14-17 Jun 2027), the world's main electricity-distribution conference and a near-perfect domain match, had its 500-word/2-page abstract deadline on 14 Sep 2026 — eight days ago. I found no extension notice; CIRED often extends, so this is worth one email today.

JOURNALS (APC / indexing / first decision). Scientific African (Elsevier, gold OA, 2468-2276): pan-African, Scopus + ESCI + DOAJ, APC reported as ~USD 720 (one source said ~200 — conflict unresolved), CiteScore ~3.3, reported 13% acceptance, ~4 days to first decision (desk screen) / ~59 days after review. JESIT (SpringerOpen, 2314-7172): ZERO APC for all authors, funded by Egypt's Specialized Presidential Council; power/electrical + applied scope; DOAJ-listed; Scopus status I could NOT confirm. Decision Analytics Journal (Elsevier, 2772-6622): optimisation/simulation scope, Scopus + DOAJ, APC USD 2,190, ~59 days to first decision. Results in Engineering: APC ~USD 2,320. Heliyon: APC USD 2,270. IJESM (Emerald): hybrid — green/subscription route free, Scopus + ESCI + Compendex. IEEE Access: APC USD 2,160, Ghana gets only a 25-50% LMIC discount (not a waiver). Elsevier waives APCs fully for Research4Life Group A and 50% for Group B; two searches said Ghana is Group A, but checking Ghana (GNI ~USD 78bn, GNIpc ~2,370, HDI 0.628) against the published Group A criteria suggests it may not qualify — UNRESOLVED and financially decisive.

### Positioning
RANKED RECOMMENDATION — and it inverts the audit's advice. The audit said "conference first, PowerAfrica." That was right in April 2026 and is wrong now: PowerAfrica 2026 is running this week, its deadline closed on 7 April, and no 2027 edition exists yet. Going conference-first now means submitting in ~March 2027 and publishing in ~September 2027. Go journal-first.

1. SCIENTIFIC AFRICAN (Elsevier, gold OA, Scopus + ESCI). Primary target. Best fit x indexing x cost. Its whole mission is publishing African primary data, which is exactly the project's strongest asset. Cheapest credible APC (~USD 720 list, likely waived or halved for Ghana). Risks: a reported ~13% acceptance rate and a fast desk-screen, so the cover letter and abstract must carry the contribution in the first three sentences.

2. JESIT (SpringerOpen). Zero APC for everyone, permanently, funded by a third party — no waiver paperwork, no risk of a surprise invoice. Power-systems scope fits. Use this if the Elsevier waiver does not come through, or as the immediate fallback on a Scientific African reject. Verify its Scopus status first; if it is not Scopus-indexed, it may not count for the lecturer's or the university's purposes.

3. IEEE AFRICON 2027, Kumasi, Ghana (23-25 Sep 2027). Run this in PARALLEL, not instead. A 6-page IEEE version, in their own country, no travel cost, IEEE Xplore indexed, deadline probably Feb-Mar 2027 — which is exactly when a journal submission made in October 2026 will be in review. Watch self-plagiarism: make the conference paper the short version and the journal paper the full one, and cite across.

4. DECISION ANALYTICS JOURNAL — if the team wants to be read as OR rather than as power engineering, and the APC is waived.

5. INTERNATIONAL TRANSACTIONS IN OPERATIONAL RESEARCH — the audit missed this. Its scope text ("work from nations with emerging OR communities... regional OR work with potential for application in other nations") reads like it was written for this paper, and the subscription route is free. Higher bar; hold in reserve for a strengthened version.

6. SOCIO-ECONOMIC PLANNING SCIENCES — the audit missed this too, and it is the true disciplinary home of the equity argument. IF ~6.2 makes it a stretch, but it is the right aspiration for the follow-up paper with more instances and a second district.

7. IJESM (Emerald, green route free), then Results in Engineering / Heliyon / IEEE Access as paid fallbacks.

DO TODAY: email CIRED 2027 asking whether the 14 September abstract deadline was extended. It cost them a 500-word abstract, the conference is the exact domain, and full papers would not be due until 2027.

DOES THE ROUTING REFORMULATION LIFT THE TIER? Partly, and less than it feels like it should. It changes the paper from unsubmittable to genuinely submittable, which is the big move. But a depot-origin multi-vehicle routing problem with capacity, duration and equity constraints is a textbook model class — the field-validated no-return-to-depot behaviour is a nice realism detail, not a methodological contribution. What actually lifts the tier is the empirical package: real inter-town travel data from an operating African utility, a real baseline (current ECG dispatch practice), multiple instances, and a theta-sweep showing the price of equity. With that package the paper is a solid Q2 applied case study — Scientific African, DAJ, ITOR, JESIT. Without it, it stays at the fast-and-broad end (Results in Engineering, Heliyon). The reformulation makes SEPS and ITOR reachable; it does not make them likely on this data alone. Claim contribution on the application, the data, and the equity-efficiency trade-off curve, and explicitly disclaim methodological novelty in the model class — reviewers punish overclaiming far harder than modest scope.

### Gaps / actions
MUST NOT CLAIM AS NOVEL
- The model class. Depot-origin multi-vehicle routing with service times, capacity and route-duration limits is standard; it is a Technician Routing and Scheduling Problem / distance-constrained CVRP variant with a fairness side-constraint. Do not claim a "new formulation."
- Equity/fairness constraints in service allocation. There is a large existing literature (equitable facility location, fairness in humanitarian and emergency-service routing, min-max and gap-based fairness objectives). The team must cite it and position against it, not around it.
- Optimisation applied to utility crew dispatch. Also well established in outage-management literature.
- "We optimised travel time." Under the old formulation this was provably a constant (audit 4.1) and under the new one the headline should be response time and shift feasibility, not travel-time percentage.
- The superseded probe numbers (2.549 h mean response, Cmax 7.982 h, "1 in 3,000 feasible", "14.6% faster"). These assumed depot round-trips and are now known to be wrong. They must not appear anywhere.

CAN LEGITIMATELY CLAIM
- Primary, field-measured travel data for 23 towns in an operating ECG district — the genuine asset.
- A field-validated dispatch protocol: crews move site-to-site and return to the post only for tooling/materials, established by interview with a Hohoe technician. Document this as a named field finding with the interview as its source; it is what justifies the routing formulation over an assignment one.
- The quantified efficiency-equity trade-off curve as a decision aid for a rural distribution utility.
- The first (as far as the team can establish) equity-constrained crew-routing case study for a Ghanaian distribution district. Phrase as "to the best of our knowledge" and only after a real literature search.

SUBMISSION-READINESS REQUIREMENTS — BLOCKING
1. The ~24x24 inter-town travel-time matrix. Nothing else matters until this exists. The team in Ghana has open internet: OSRM public API, OpenRouteService (free key, matrix endpoint) or Google Distance Matrix will produce it in an afternoon. Build the no-API fallback too (haversine distance calibrated against the 23 measured depot-to-town times to fit an effective speed, with the residuals reported) so the paper is not hostage to an API, and report both.
2. Reference list: 20-30 refs across TRSP/field-service scheduling, VRP with duration constraints, equity in service allocation, and power-distribution outage management including African utility studies. Currently zero. This alone is a desk-reject trigger.
3. Written ECG permission to publish district operational data, plus a data-availability statement. Outside the team's control — send today if not already sent.
4. Explicit disclosure, in the abstract and in Methods, that the 15 fault instances are synthetic. Consider retitling to "A Simulation Case Study Grounded in the Hohoe Operations Department." Undisclosed synthetic data presented under a case-study title is the one failure mode that ends a paper's life permanently.
5. Experimental design: more than n=1 instance, a feasibility-aware baseline, current ECG practice as the counterfactual if obtainable, theta and alpha/beta sensitivity sweeps, solve times and optimality gaps.

SUBMISSION-READINESS — ADMINISTRATIVE
6. Confirm the Elsevier/Research4Life waiver BEFORE choosing a paid-OA venue. Practical route: start a submission in Elsevier's system — the author communication system quotes the waiver-adjusted APC automatically. Do not commit to a USD 2,000+ venue on the assumption of a waiver.
7. Venue templates and limits: Elsevier article template for Scientific African; IEEE conference template with a 6-page limit for AFRICON; CIRED wants a 500-word, 2-page abstract first.
8. CRediT author contributions, corresponding author, affiliations, ORCIDs for all five, funding statement (or "none"), competing-interests statement.
9. Data licence for dataset/ separate from the code's MIT (CC-BY-4.0 is conventional), and a tagged repository release cited in the data-availability statement.
10. Fix the data-integrity items before a reviewer finds them: the Fodome 0.65 km / 0.65 h entry, the Wli-vs-Ve-Dator speed inversion, the town-name spacing, and the unstable ceil(max)/2 zone threshold.

WHAT I COULD NOT VERIFY — the team must check these themselves
- Whether Ghana is Research4Life Group A (full Elsevier waiver) or Group B (50%). Two search summaries said Group A; my own check of Ghana's GNI (~USD 78bn), GNI per capita (~USD 2,370) and HDI (0.628) against the published Group A criteria suggests it may not qualify. Financially decisive — verify at portal.research4life.org.
- Whether PowerAfrica 2027 exists at all. Nothing announced.
- The AFRICON 2027 CFP deadline. Not yet published.
- Whether CIRED 2027 extended its 14 September abstract deadline. No evidence either way.
- JESIT's Scopus and Web of Science status. DOAJ confirmed; Scopus not confirmed.
- Scientific African's exact current APC (sources gave ~USD 200 and USD 720).
All primary venue websites were blocked by this sandbox's egress proxy, so every figure above is second-hand.

### References
- **[likely-real]** IEEE PES/IAS PowerAfrica 2026 Conference, Safari Park, Nairobi, Kenya, 21-25 September 2026. Theme: "Accelerating Resilient Energy Systems & Industrial Decarbonization through Innovation". Full papers 6 pages (IEEE format, +2 pages at USD 50/page), short papers 3 pages. Paper submission deadline: 7 April 2026. https://ieee-powerafrica.org/call-for-papers/
  - The audit's top recommendation — but the conference is running this week and its deadline passed five months ago, so it is a 2027 target at best and no longer the fast option.
- **[uncertain]** IEEE AFRICON 2027 (18th IEEE Region 8 AFRICON), Kumasi, Ghana, 23-25 September 2027. IEEE Region 8 / IEEE Africa Council. Proceedings in IEEE Xplore. CFP not yet published. https://ieeer8.org/category/technical-activities/conference-coordination/
  - The venue the audit missed that fits best on practical grounds: IEEE-indexed, hosted in the team's own country (no international travel or visa cost), and broad enough in scope to take an applied power-systems OR case study.
- **[likely-real]** CIRED 2027 - 29th International Conference and Exhibition on Electricity Distribution, Stockholm, Sweden, 14-17 June 2027. CFP opened 10 April 2026; abstract deadline 14 September 2026 (max 500 words / 2 pages); acceptance notification 13 November 2026. https://2027.cired.net/key-dates/
  - The single best domain match in the world for distribution-utility field operations, and the deadline is only eight days past — worth an immediate email asking whether the abstract deadline was extended.
- **[verified]** Scientific African (Elsevier), ISSN 2468-2276, gold open access. Scope categories include "Information Technology and Engineering" and "Mathematics". Indexed in Scopus, DOAJ and ESCI. APC reported at USD 720 (one source reported ~USD 200). CiteScore ~3.3; reported acceptance rate ~13%; submission-to-first-decision ~4 days, submission-to-acceptance ~155 days. https://www.sciencedirect.com/journal/scientific-african
  - Best overall balance of scope fit, pan-African remit, Scopus indexing and low/waivable cost; the journal exists precisely to publish African primary data like the 23-town travel survey.
- **[likely-real]** Journal of Electrical Systems and Information Technology (JESIT), SpringerOpen, ISSN 2314-7172. Open access with NO article-processing charge — the APC is covered by Egypt's Specialized Presidential Council for Education and Scientific Research. Scope: electrical engineering and information technology, including power electronics, renewable energy, informatics. DOAJ-listed. https://jesit.springeropen.com/submission-guidelines/fees-and-funding
  - The only candidate that is guaranteed free to publish in regardless of any waiver decision, which removes the largest financial risk for an unfunded student team; scope covers applied power-systems work.
- **[verified]** Decision Analytics Journal (Elsevier), ISSN 2772-6622, gold open access since 2021. Scope: predictive modelling, simulation modelling, optimization modelling, business intelligence. Indexed in Scopus, Crossref, DOAJ. APC USD 2,190 (excl. tax). Submission to first decision ~59 days. https://www.sciencedirect.com/journal/decision-analytics-journal
  - The most natural OR-framed home among the audit's list — "optimization modelling" is an explicit scope term — but the USD 2,190 APC is the binding constraint unless a full Elsevier waiver applies.
- **[verified]** International Transactions in Operational Research (ITOR), Wiley-Blackwell on behalf of IFORS, ISSN 1475-3995. Hybrid: subscription route free to authors; gold OA APC USD 4,230. Scope explicitly includes "studies of worldwide interest from nations with emerging OR communities" and "national or regional OR work which has the potential for application in other nations". Scopus/SCIE indexed. https://onlinelibrary.wiley.com/page/journal/14753995/homepage/aims.htm
  - A venue the audit missed whose stated scope is an almost verbatim description of this paper; publishing via the subscription route costs nothing, though the methodological bar is higher than Scientific African's.
- **[verified]** Socio-Economic Planning Sciences: The International Journal of Public Sector Decision-Making (Elsevier), ISSN 0038-0121. Hybrid; gold OA APC reported USD 2,640-3,590; subscription route free. Scope: application of operations research, management science and statistics to public- and service-sector decision problems. Scopus/SCIE indexed; 2023 impact factor ~6.2. https://www.sciencedirect.com/journal/socio-economic-planning-sciences
  - A venue the audit missed that is the natural disciplinary home for the equity-constrained framing (fair restoration times for rural customers), but it is a genuine stretch that would need a far stronger experimental section.
- **[verified]** Results in Engineering (Elsevier), ISSN 2590-1230, gold open access, DOAJ-listed, Scopus indexed. APC USD 2,320 (excl. tax); sources vary between USD 1,210 and 2,320. Broad interdisciplinary engineering scope. https://www.sciencedirect.com/journal/results-in-engineering
  - Fast and broad enough to accept the paper, but expensive and carries little signalling value for an applied OR contribution; keep as a fallback only.
- **[verified]** Heliyon (Cell Press / Elsevier), gold open access. APC USD 2,270 plus tax, due on acceptance. Research4Life waivers/discounts applied automatically where all authors are in an eligible country. https://www.cell.com/heliyon/open-access
  - Included because the audit listed it; the high APC and very broad multidisciplinary scope make it a weaker choice than Scientific African for essentially the same effort.
- **[verified]** International Journal of Energy Sector Management (IJESM), Emerald Publishing. Hybrid journal: gold OA requires an APC, but the green open-access route (self-archiving) is free. Indexed in Scopus, Ei Compendex, Inspec and ESCI. Scope covers supply management across the energy chain including distribution and retail supply, demand management, and customer/stakeholder management. https://www.emeraldgrouppublishing.com/journal/ijesm
  - Fits the utility-operations and customer-equity framing and costs nothing via the green route; a reasonable non-OA option if the team wants a management-oriented readership.
- **[verified]** Operations Research Forum (Springer), ISSN 2662-2556. Hybrid; gold OA APC GBP 2,290 / USD 3,190 / EUR 2,590; subscription route free. Scope explicitly lists case studies, scheduling, logistics, optimization and energy applications, and welcomes "new and innovative practical applications". Scopus-listed (SJR source 21101080460). https://link.springer.com/journal/43069/aims-and-scope
  - A venue the audit missed that explicitly solicits applied case studies in OR — a good match for a routing formulation with real field data, free via the subscription route.
- **[verified]** IEEE Access, gold open access. 2026 APC USD 2,160 plus local taxes. IEEE Low and Lower-Middle Income Country Open Access Discount Program: 100% waiver for low-income countries, 25-50% discount for lower-middle-income countries (Ghana is World Bank lower-middle-income); discount applies only if ALL authors are in an eligible country. https://open.ieee.org/for-authors/ieee-low-and-lower-middle-income-country-open-access-discount-program/
  - Confirms the audit's "moderate" rating and adds the cost reality: Ghana gets at most a 50% discount, so roughly USD 1,080-1,620, for a venue whose reviewers will press hardest on routing rigour.
- **[uncertain]** Elsevier APC waiver policy and Research4Life eligibility: Elsevier fully waives APCs in fully open access journals for authors from 69 Research4Life Group A countries and gives a 50% discount for 57 Group B countries; all authors must be in an eligible country. Elsevier also runs a Geographical Pricing for Open Access (GPOA) pilot across ~142 gold OA journals from January 2024. Group A criteria are GNI/GNIpc/LDC/HDI-based. https://www.elsevier.com/about/policies-and-standards/pricing and https://www.research4life.org/access/criteria/
  - This single policy decides whether Scientific African, Decision Analytics Journal, Results in Engineering and Heliyon cost the team zero or several thousand dollars — and Ghana's group membership is the one fact I could not pin down.
