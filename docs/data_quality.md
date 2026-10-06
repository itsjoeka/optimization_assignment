# Data Quality Register

Every known issue in the datasets, with the decision taken and its effect.
Nothing here is silently patched: a reviewer who downloads the CSVs and finds
an anomaly with no corresponding entry will assume the worst.

## 1. Fodome — near-certain transcription error

| field | value |
|---|---|
| distance | 0.65 km |
| travel time | 0.65 h |
| implied speed | **1.0 km/h** |

0.65 km taking 39 minutes implies walking pace. The most likely true value is
6.5 km (a dropped digit) or 16.5 km.

**Decision taken:** the value is **retained unchanged** in the dataset, flagged in
`src.config.SUSPECT_TOWNS`, and **excluded from the speed-model calibration**.
It is not corrected because the correct value is unknown — that requires the
original measurement source. **No fault in the published 15-fault instance occurs
at Fodome**, so no result in the paper depends on it.

**Action required:** confirm against the source, and ask what the measurement
*procedure* was (odometer from the post, or from somewhere else) — that may
explain Fodome and Gbledi at once.

## 2. Implied road speeds span 1.0–47.2 km/h

This looked like noisy data in the first audit. It is mostly not.

Regressing travel time on distance over the 22 clean towns gives a fixed
overhead plus a constant cruise speed — about ten minutes to clear Hohoe town,
then roughly 49 km/h. Dividing a *fixed overhead* by a *short distance* produces
an apparently slow town; the same vehicle on the same road model produces Wli at
47 km/h and Gbi-Kledzo at 18 km/h.

**Decision taken:** report the fitted speed model in the Data section as a
finding, not an assumption. See `notebooks/01_data.ipynb`.

### Implied speeds, all 23 towns

| town | distance (km) | travel (h) | implied km/h |
|---|---|---|---|
| Fodome ⚠️ | 0.65 | 0.65 | 1.0 |
| Gbi - Kledzo | 4.9 | 0.267 | 18.4 |
| Gbi - Wegbe | 6.2 | 0.333 | 18.6 |
| Gbi - Avege | 10.2 | 0.467 | 21.8 |
| Santrokofi | 7.5 | 0.333 | 22.5 |
| Ve- Kobenu | 13.7 | 0.583 | 23.5 |
| Ve-Dator | 14.3 | 0.6 | 23.8 |
| Gbledi | 1.3 | 0.05 | 26.0 |
| Akpafu | 11.9 | 0.417 | 28.5 |
| Lolobi | 10.1 | 0.35 | 28.9 |
| Agome yo | 15.9 | 0.517 | 30.8 |
| Zimugaziwo snake Village | 16.5 | 0.467 | 35.3 |
| Liati | 20.0 | 0.55 | 36.4 |
| Likpe | 17.2 | 0.467 | 36.8 |
| Leklebi | 23.5 | 0.633 | 37.1 |
| Afadzo South | 38.4 | 1.017 | 37.8 |
| Ve -Gbodome | 25.4 | 0.667 | 38.1 |
| Logba | 38.3 | 1.0 | 38.3 |
| Godenu | 19.2 | 0.5 | 38.4 |
| Wuinta | 30.7 | 0.783 | 39.2 |
| Fume | 38.3 | 0.917 | 41.8 |
| Golokwati | 21.3 | 0.5 | 42.6 |
| Wli | 22.8 | 0.483 | 47.2 |

## 3. Zone threshold — resolved

The original code used `ceil(max(distance))/2` = 19.5 km, a function of the
farthest town in the dataset: adding one distant town silently reclassifies
others. The README stated 20 km. The two disagree on **Liati, at exactly 20.0 km**.

**Decision taken:** fixed exogenously at **20.0 km** in
`src.config.ZONE_THRESHOLD_KM`, with sensitivity reported over (19.5, 20.0, 25.0).

| threshold | n_Near | n_Far | mean travel Near | mean travel Far |
|---|---|---|---|---|
| 19.5 km | 8 | 7 | 0.468875 | 0.747714 |
| 20.0 km | 9 | 6 | 0.477889 | 0.780667 |
| 25.0 km | 11 | 4 | 0.480364 | 0.925250 |

**This choice moves every equity constant in the paper.** It was made before any
result was generated, which is why it appears here rather than in the results.

## 4. Town-name inconsistencies

`Ve -Gbodome`, `Ve- Kobenu`, `Ve-Dator` use inconsistent internal spacing;
`Zimugaziwo snake Village` has inconsistent capitalisation. These are cosmetic
and do not affect joins (names match exactly between the two CSVs), but they
should be normalised before the dataset is published.

## 5. The faults are simulated

The 23 towns and their travel times are **real field data**. The 15 faults are
**synthetic** — `random.choices(seed=60)` over an assumed fault-type distribution
(0.15/0.25/0.20/0.15/0.10/0.15) and an assumed 30/70 priority split. Neither
distribution has a stated source.

**This must be disclosed in the abstract**, not only in Methods, and the title
should say *simulation case study*. Simulated demand against a real network is a
standard and acceptable design; undisclosed, it is a research-integrity problem.
