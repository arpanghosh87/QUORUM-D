# Full synthetic policy-selection results

Analytical/synthetic companion only. All prices, latency and judge performance are assumed. Calibration/development/test seeds 51/52/53; item counts 1,000/4,000/4,000. The fixed menu has 37 candidates. Budget 0.046 USD/item, p95 latency <=2 s, per-dimension coverage >=0.95, accepted-case Wilson upper risk <=0.17/0.19 (z=1.96); loss prices 0.15 per dimension, deferral loss 0.5, amortized calibration 0.001 USD/item. The objective uses all-item loss including deferral, not accepted-case risk alone. Risk and coverage are proportions. Values are rounded for presentation; feasibility and violated criteria use unrounded values. These are descriptive selection diagnostics, not simultaneous guarantees.

## Development — all 37 configurations

| Policy | Cost/item | p95 s | Coverage D1 | Coverage D2 | Error D1 | Error D2 | Wilson upper D1 | Wilson upper D2 | Objective | Feasible | Violated criteria |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| single+single | 0.04100000 | 1.0 | 1.00000 | 1.00000 | 0.09375 | 0.18475 | 0.10318 | 0.19708 | 0.08277500 | False | risk D2 |
| single+panel | 0.03600000 | 1.2 | 1.00000 | 1.00000 | 0.09375 | 0.22700 | 0.10318 | 0.24024 | 0.08411250 | False | risk D2 |
| single+weighted | 0.03600000 | 1.2 | 1.00000 | 1.00000 | 0.09375 | 0.22700 | 0.10318 | 0.24024 | 0.08411250 | False | risk D2 |
| single+verifier | 0.04600000 | 1.5 | 1.00000 | 1.00000 | 0.09375 | 0.09075 | 0.10318 | 0.10005 | 0.07367500 | True | none |
| single+selective | 0.04347500 | 2.0 | 1.00000 | 1.00000 | 0.09375 | 0.14900 | 0.10318 | 0.16037 | 0.07988750 | True | none |
| single+defer | 0.04796000 | 1.2 | 1.00000 | 0.70100 | 0.09375 | 0.16583 | 0.10318 | 0.18006 | 0.10188500 | False | budget; coverage D2 |
| panel+single | 0.03600000 | 1.2 | 1.00000 | 1.00000 | 0.20375 | 0.18475 | 0.21651 | 0.19708 | 0.09427500 | False | risk D1; risk D2 |
| panel+panel | 0.03100000 | 1.2 | 1.00000 | 1.00000 | 0.20375 | 0.22700 | 0.21651 | 0.24024 | 0.09561250 | False | risk D1; risk D2 |
| panel+weighted | 0.03100000 | 1.2 | 1.00000 | 1.00000 | 0.20375 | 0.22700 | 0.21651 | 0.24024 | 0.09561250 | False | risk D1; risk D2 |
| panel+verifier | 0.04100000 | 1.5 | 1.00000 | 1.00000 | 0.20375 | 0.09075 | 0.21651 | 0.10005 | 0.08517500 | False | risk D1 |
| panel+selective | 0.03847500 | 2.0 | 1.00000 | 1.00000 | 0.20375 | 0.14900 | 0.21651 | 0.16037 | 0.09138750 | False | risk D1 |
| panel+defer | 0.04296000 | 1.2 | 1.00000 | 0.70100 | 0.20375 | 0.16583 | 0.21651 | 0.18006 | 0.11338500 | False | coverage D2; risk D1 |
| weighted+single | 0.03600000 | 1.2 | 1.00000 | 1.00000 | 0.20375 | 0.18475 | 0.21651 | 0.19708 | 0.09427500 | False | risk D1; risk D2 |
| weighted+panel | 0.03100000 | 1.2 | 1.00000 | 1.00000 | 0.20375 | 0.22700 | 0.21651 | 0.24024 | 0.09561250 | False | risk D1; risk D2 |
| weighted+weighted | 0.03100000 | 1.2 | 1.00000 | 1.00000 | 0.20375 | 0.22700 | 0.21651 | 0.24024 | 0.09561250 | False | risk D1; risk D2 |
| weighted+verifier | 0.04100000 | 1.5 | 1.00000 | 1.00000 | 0.20375 | 0.09075 | 0.21651 | 0.10005 | 0.08517500 | False | risk D1 |
| weighted+selective | 0.03847500 | 2.0 | 1.00000 | 1.00000 | 0.20375 | 0.14900 | 0.21651 | 0.16037 | 0.09138750 | False | risk D1 |
| weighted+defer | 0.04296000 | 1.2 | 1.00000 | 0.70100 | 0.20375 | 0.16583 | 0.21651 | 0.18006 | 0.11338500 | False | coverage D2; risk D1 |
| verifier+single | 0.04600000 | 1.5 | 1.00000 | 1.00000 | 0.05650 | 0.18475 | 0.06409 | 0.19708 | 0.08218750 | False | risk D2 |
| verifier+panel | 0.04100000 | 1.5 | 1.00000 | 1.00000 | 0.05650 | 0.22700 | 0.06409 | 0.24024 | 0.08352500 | False | risk D2 |
| verifier+weighted | 0.04100000 | 1.5 | 1.00000 | 1.00000 | 0.05650 | 0.22700 | 0.06409 | 0.24024 | 0.08352500 | False | risk D2 |
| verifier+verifier | 0.05100000 | 1.5 | 1.00000 | 1.00000 | 0.05650 | 0.09075 | 0.06409 | 0.10005 | 0.07308750 | False | budget |
| verifier+selective | 0.04847500 | 2.0 | 1.00000 | 1.00000 | 0.05650 | 0.14900 | 0.06409 | 0.16037 | 0.07930000 | False | budget |
| verifier+defer | 0.05296000 | 1.5 | 1.00000 | 0.70100 | 0.05650 | 0.16583 | 0.06409 | 0.18006 | 0.10129750 | False | budget; coverage D2 |
| selective+single | 0.04258125 | 2.0 | 1.00000 | 1.00000 | 0.11700 | 0.18475 | 0.12733 | 0.19708 | 0.08784375 | False | risk D2 |
| selective+panel | 0.03758125 | 2.0 | 1.00000 | 1.00000 | 0.11700 | 0.22700 | 0.12733 | 0.24024 | 0.08918125 | False | risk D2 |
| selective+weighted | 0.03758125 | 2.0 | 1.00000 | 1.00000 | 0.11700 | 0.22700 | 0.12733 | 0.24024 | 0.08918125 | False | risk D2 |
| selective+verifier | 0.04758125 | 2.0 | 1.00000 | 1.00000 | 0.11700 | 0.09075 | 0.12733 | 0.10005 | 0.07874375 | False | budget |
| selective+selective | 0.04505625 | 2.0 | 1.00000 | 1.00000 | 0.11700 | 0.14900 | 0.12733 | 0.16037 | 0.08495625 | True | none |
| selective+defer | 0.04954125 | 2.0 | 1.00000 | 0.70100 | 0.11700 | 0.16583 | 0.12733 | 0.18006 | 0.10695375 | False | budget; coverage D2 |
| defer+single | 0.04653000 | 1.2 | 0.73675 | 1.00000 | 0.13845 | 0.18475 | 0.15139 | 0.19708 | 0.10928625 | False | budget; coverage D1; risk D2 |
| defer+panel | 0.04153000 | 1.2 | 0.73675 | 1.00000 | 0.13845 | 0.22700 | 0.15139 | 0.24024 | 0.11062375 | False | coverage D1; risk D2 |
| defer+weighted | 0.04153000 | 1.2 | 0.73675 | 1.00000 | 0.13845 | 0.22700 | 0.15139 | 0.24024 | 0.11062375 | False | coverage D1; risk D2 |
| defer+verifier | 0.05153000 | 1.5 | 0.73675 | 1.00000 | 0.13845 | 0.09075 | 0.15139 | 0.10005 | 0.10018625 | False | budget; coverage D1 |
| defer+selective | 0.04900500 | 2.0 | 0.73675 | 1.00000 | 0.13845 | 0.14900 | 0.15139 | 0.16037 | 0.10639875 | False | budget; coverage D1 |
| defer+defer | 0.05349000 | 1.2 | 0.73675 | 0.70100 | 0.13845 | 0.16583 | 0.15139 | 0.18006 | 0.12839625 | False | budget; coverage D1; coverage D2 |
| shared+shared | 0.02600000 | 1.1 | 1.00000 | 1.00000 | 0.12800 | 0.13200 | 0.13871 | 0.14284 | 0.06500000 | True | none |

Development feasible (4): single+verifier, single+selective, selective+selective, shared+shared. Selected: shared+shared. Selection minimizes the declared objective among feasible candidates, with complexity and name as tie breakers.

## Held-out — frozen selected configuration and declared baselines

| Policy | Cost/item | p95 s | Coverage D1 | Coverage D2 | Error D1 | Error D2 | Wilson upper D1 | Wilson upper D2 | Objective | Feasible | Violated criteria |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| single+single | 0.04100000 | 1.0 | 1.00000 | 1.00000 | 0.09675 | 0.17375 | 0.10630 | 0.18580 | 0.08157500 | True | none |
| panel+panel | 0.03100000 | 1.2 | 1.00000 | 1.00000 | 0.19750 | 0.23350 | 0.21013 | 0.24686 | 0.09565000 | False | risk D1; risk D2 |
| weighted+weighted | 0.03100000 | 1.2 | 1.00000 | 1.00000 | 0.19750 | 0.23350 | 0.21013 | 0.24686 | 0.09565000 | False | risk D1; risk D2 |
| verifier+verifier | 0.05100000 | 1.5 | 1.00000 | 1.00000 | 0.05775 | 0.08750 | 0.06541 | 0.09666 | 0.07278750 | False | budget |
| selective+selective | 0.04446875 | 2.0 | 1.00000 | 1.00000 | 0.11600 | 0.15050 | 0.12629 | 0.16192 | 0.08444375 | True | none |
| shared+shared | 0.02600000 | 1.1 | 1.00000 | 1.00000 | 0.11900 | 0.13525 | 0.12940 | 0.14620 | 0.06413750 | True | none |

Decision: deploy_candidate (synthetic only). Three held-out configurations are feasible; this is distinct from the four development-feasible policies. Development-feasible alternatives not designated as held-out baselines were not retested. No selection from held-out results. The verifier-only configuration violates budget; uniform and competence-weighted panels violate both critical risk limits. A failed feasibility check is not always a statistically established violation: uncertainty can make a policy inconclusive.
