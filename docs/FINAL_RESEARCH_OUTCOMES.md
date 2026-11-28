# Final research outcomes — QUORUM-D

Companion to the QUORUM-D narrative critical review. Analytical and synthetic evidence only; no real LLM calls, paid API expenditure or independent replication of cited studies. Earlier results are in [validation.md](validation.md); claim mapping is in [claims.md](claims.md). The reference pipeline remains a restricted demonstration, not empirical validation.

## 1. Existing reproducibility results

The initial package implements Equations 1–5 and reproduces the numerical illustrations of Figures 4–6 and all five Table 6 rows. The original synthetic common-shock, calibration sensitivity and finite-menu demonstrations remain unchanged. Run the verification command below to compare regenerated outputs with archived numerical values.

## 2. Identical ESS, different majority accuracy (exact construction)

| Distribution | Marginal correctness | Pairwise correlation | ESS | Majority accuracy |
|---|---:|---:|---:|---:|
| Independent fair votes | 0.500 | 0.000 | 3.000 | 0.50000 |
| Even parity | 0.500 | 0.000 | 3.000 | 0.75000 |
| Odd parity | 0.500 | 0.000 | 3.000 | 0.25000 |
| Independent competent votes | 0.750 | 0.000 | 3.000 | 0.84375 |
| Dependent competent A | 0.750 | 0.000 | 3.000 | 0.81250 |
| Dependent competent B | 0.750 | 0.000 | 3.000 | 0.93750 |

Let K count correct votes among three judges. Given K, choose a uniformly random subset of K judges. Thus p=E[K]/3, joint pairwise correctness=E[K(K−1)]/6, correlation=(joint−p²)/(p(1−p)), and majority accuracy=P(K≥2). The fair distributions over K=0,1,2,3 are (1,3,3,1)/8, (1,0,3,0)/4 and (0,3,0,1)/4. The competent distributions are (1,9,27,27)/64, (0,12,24,28)/64 and (4,0,36,24)/64. Each group shares first and second moments but not its majority tail. Zero pairwise correlation is not mutual independence. This is an exact counterexample, not a simulation or a claim about real judges. The three competent distributions appear in Section 4.2 and Table 5 of the manuscript.

## 3. Full covariance and nonnegative weighting (analytical)

Independent Bernoulli error probabilities 0.1, 0.3, 0.5 imply variances 0.09, 0.21, 0.25. The reference variance is explicitly 0.09; the resulting reference-normalized size depends on that choice and is not the equal-variance ESS.

Optimal weights: [0.55910543, 0.23961661, 0.20127796]; variance 0.05031949; uniform variance 0.06111111; reference ESS 1.788571.
Positive definite correlation example with entries R12=R13=0.75, R23=0.3: unconstrained weights [-0.66666667, 0.83333333, 0.83333333]; constrained weights [0.0, 0.5, 0.5], variance 0.650000 versus uniform variance 0.733333. This is a covariance-matrix example, not an asserted jointly feasible Bernoulli model. Small-panel active-face enumeration covers every nonempty face for positive definite matrices of at most 12 judges. It is not a scalable solver. Lower variance does not imply lower decision error.

## 4. Selective routing (synthetic)

| Subset | Jointly evaluated items | Mean off-diagonal error correlation | Error rates |
|---|---:|---:|---|
| full | 4000 | 0.485237 | 0.222500, 0.228500, 0.217500 |
| routed | 1070 | -0.345244 | 0.451402, 0.473832, 0.432710 |

Routing uses only observable one-vote margins of the three lightweight binary judgments, not reference labels. Seed 53, dimension 1 of the existing 4,000-item reference tape. Full and routed pairwise matrices are archived in JSON. Conditional correlations describe the jointly observed routed subset, not the full workload. The negative routed correlations are not evidence that the original judges are independent or that the routing rule improves accuracy. Supports the paper’s conditional-dependence reporting safeguard.

## 5. Paired uncertainty (synthetic)

| Dimension | Shared minus separate single-judge error | 95% percentile interval |
|---|---:|---:|
| 1 | 0.022250 | [0.008000, 0.035750] |
| 2 | -0.038500 | [-0.053500, -0.022750] |

Paired IID bootstrap of 4,000 synthetic items, 2,000 draws, seeds 2026 and 2027; same pre-existing synthetic comparison, no new policy selection. Positive differences mean shared is worse. These are descriptive pointwise percentile intervals, no multiple-comparison adjustment or population-level risk guarantee. Cluster resampling helper tested separately; the example is IID.

## 6. Reproduction and interpretation

Run `python -m scripts.strengthen` and `python -m pytest -q`. Run `python -m scripts.verify_archive` to independently regenerate and verify the archived numerical files. Numerical outputs: `results/strengthening.json`. The results establish neither empirical superiority, actual cost savings, nor complete implementation of Algorithm 1.
