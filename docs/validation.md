# Computational validation summary

Analytical and synthetic scope only. All reported costs and judge competence in the policy examples are assumed. No real model calls were made. These results do not establish actual LLM superiority, replicate published datasets, or prove population-level risk control.

## Local execution

The initial PR #1 suite passed 14 pytest tests; PR #2 expanded the suite to 21. All 21 passed in the historical development PR #3 main-branch CI run ([45886588454](https://github.com/arpanghosh87/QUORUM-D---1st-draft/actions/runs/45886588454), commit `9eda029d6081467799b2b8a2abaca989c08d6f69`). Five rows of Table 6 were reproduced to their displayed precision. Figures 4–6 are numerical reproductions, not pixel-identical layouts.

## Common-shock majority experiment

24 conditions, 200,000 independent synthetic items per condition. Maximum absolute deviation from the model-specific analytical majority probability: 0.002695 (0.2695 percentage points).

For nine judges with individual correctness probability 0.75:

| Pairwise correlation | Theoretical majority accuracy | Simulated accuracy | Effective size |
| --- | ---: | ---: | ---: |
| 0.0 | 0.951073 | 0.950825 | 9.000 |
| 0.4 | 0.870644 | 0.870855 | 2.143 |
| 0.8 | 0.790215 | 0.788780 | 1.216 |

The common-shock model is one feasible joint Bernoulli distribution. Correlation alone does not uniquely determine majority correctness.

## Calibration sensitivity

Fixed synthetic five-judge model, 50 fits per calibration size, fixed shrinkage, independent test tape of 100,000 items. The mean and SD are calculated among successful closed-form fits; failures remain reported and are not discarded silently.

| Calibration items | Successful | Failed | Mean test ESS | SD |
| ---: | ---: | ---: | ---: | ---: |
| 25 | 25 | 25 | 1.829815 | 0.040717 |
| 100 | 40 | 10 | 1.854071 | 0.014047 |
| 500 | 50 | 0 | 1.869678 | 0.003743 |
| 2000 | 50 | 0 | 1.872989 | 0.001169 |

These results illustrate sensitivity under the chosen generator and fitting procedure; they are not a universal sample-size recommendation.

## Frozen synthetic reference pipeline

1,000 calibration, 4,000 development, 4,000 held-out items; two binary dimensions. 37 fixed candidates evaluated, four feasible on development: `single+verifier`, `single+selective`, `selective+selective`, and `shared+shared`. See [the complete policy-selection report](POLICY_SELECTION_RESULTS.md) for all 37 candidates, Wilson upper endpoints, objectives and constraint violations. Budget $0.046/item, maximum p95 latency 2s, minimum coverage 95%, accepted-case error limits 17% and 19% (using Wilson upper endpoints), loss prices $0.15 per unit per dimension. Assumed amortized calibration cost $0.001/item.

Selected shared+shared (one shared call), frozen before held-out scoring. Held-out comparison:

| Policy | Cost/item | Dimension 1 error | Dimension 2 error | Feasible |
| --- | ---: | ---: | ---: | --- |
| single+single | 0.041 | 0.09675 | 0.17375 | yes |
| panel+panel | 0.031 | 0.19750 | 0.23350 | no |
| weighted+weighted | 0.031 | 0.19750 | 0.23350 | no |
| verifier+verifier | 0.051 | 0.05775 | 0.08750 | no |
| selective+selective | 0.04447 | 0.11600 | 0.15050 | yes |
| shared+shared | 0.026 | 0.11900 | 0.13525 | yes |

The verifier was more accurate but exceeded the assumed budget ($0.051 > $0.046). The uniform and competence-weighted panels violated both dimension-specific Wilson upper risk limits (0.21013 and 0.24686 versus 0.17 and 0.19). Three configurations are feasible on held-out data; the four development-feasible configurations are a distinct set.  The selected policy has a simulated deployment-candidate decision, not approval to deploy a real system. Candidate costs are synthetic, and parallel latency is modeled as the maximum of dimension latencies. Wilson intervals and paired IID standard errors are descriptive; they do not establish simultaneous or distribution-free guarantees. See generated JSON and CSV files for full outputs. The same seed deterministically reproduces these results within a compatible numerical environment.
