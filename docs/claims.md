# Claim traceability

| ID | Manuscript location | Implementation | Verification / scope |
| --- | --- | --- | --- |
| C01 | Eq. 1 | weighted_vote | Binary weighted rule; positive tie; test_vote_and_objective |
| C02 | Eq. 2 | majority_accuracy | Independent equally competent odd panel; test_majority |
| C03 | Eq. 3 / Fig. 4 | effective_size | Analytical ESS; PSD range and zero-variance endpoint; test_effective_size |
| C04 | Eq. 4 / Fig. 5 | weighted_effective_size | Equal positive marginal variance; test_weighted |
| C05 | §5.1 / Fig. 6 / Table 6 | minimum_variance_weights, table_rows | Five rows verified to printed precision; test_table5 |
| C06 | §5.1 | correlated_errors, error_statistics | Synthetic Bernoulli copy construction; test_binary_construction |
| C07 | §4.5 | pivotal | Exhaustive binary ballot enumeration through N=9; test_pivotal_exhaustive |
| C08 | Eq. 5 | policy_objective | Evaluation of same-horizon cost plus loss; test_vote_and_objective |
| C09 | Algorithm 1 | policy.py, reference.py | Synthetic finite-menu reference pipeline; split checks, feasibility, shared-call accounting, frozen rule and held-out comparison; not a general implementation or empirical validation |
| C10 | ESS limitation (Eq. 3–4 discussion) | exchangeable_moments | Exact matched-moment counterexample; test_counterexample; strengthening.json |
| C11 | Unequal variance and weighting (Eq. 4 discussion) | covariance_variance, constrained_weights | Explicit reference variance; small positive definite matrices; test_covariance, test_boundary |
| C12 | Conditional dependence (Algorithm 1) | conditional_errors | Synthetic jointly observed routed subset; test_routing |
| C13 | Uncertainty (Algorithm 1) | paired_bootstrap | Paired IID descriptive percentile intervals; cluster helper tested separately; test_bootstrap |
| C14 | Deployment safeguard | held_out | Success, rejection, inconclusive and frozen-name checks; test_heldout_rejection_and_uncertainty |
| C15 | Reproducibility | scripts/verify_archive.py | Seven original archived artifacts plus the policy-selection Markdown report; test_archive_comparison |

## Numerical checks

* Eq. 2: p=0.4, N=9 yields 0.26656768.
* Eq. 3: N=9, rho=0.391 yields approximately 2.18, consistent with the cited rounded values.
* Eq. 3: N=10, rho=0.206 yields 3.50385, close to the reported 3.51. The input correlation is rounded; the original estimate cannot be recovered exactly without the unrounded data. This is not replication of Hossain et al.
* Table 6: all five rows agree at printed precision. No judge-call expenditure is reduced by reweighting.
* The Bernoulli construction uses independent copy decisions; pairwise correlations are products of copy probabilities. PSD alone is not sufficient for general joint Bernoulli feasibility.

## Historical development execution

Twenty-one pytest test functions passed in Python with NumPy 2.3.5, Matplotlib 3.10.8 and pytest 9.0.2. Figures and CSV outputs were generated locally. CI has its own execution environment and must be checked separately. No benchmark data or paid LLM calls were used.

Limitations: complete-case binary errors only; no arbitrary missing-ballot handling or general large-panel optimization. The targeted helpers cover explicit reference-normalized covariance, small positive definite constrained weighting, and cluster resampling, but only the IID bootstrap example is exercised in the reported synthetic experiment. The reference pipeline implements explicit deferral, but not actual downstream human outcomes, full per-candidate judge dependence re-estimation, dynamic resource reallocation, persistent held-out locks, or production monitoring. Eq. 5 requires correctly deduplicated costs supplied by callers. These are outside the current restricted research companion. See [FINAL_RESEARCH_OUTCOMES.md](FINAL_RESEARCH_OUTCOMES.md) for the new results and limitations.

For the historical development CI evidence and full policy-selection report, see [FINAL_VERIFICATION.md](FINAL_VERIFICATION.md) and [POLICY_SELECTION_RESULTS.md](POLICY_SELECTION_RESULTS.md).

## Revised Algorithm 1 and feasibility reporting

The general proposed algorithm reserves candidate-search budget for predeclared mandatory baselines and returns an insufficient-comparison-budget outcome if the required comparisons cannot be completed. This safeguard is not enforced by the restricted reference implementation for arbitrary truncated searches; the reported run evaluated all 37 candidates, including the baselines. The implemented selection key is (objective, complexity, policy name), with no nonzero tie tolerance. The held-out comparison uses identical items and labels without selecting a new winner. Feasibility uses upper endpoints of nominal two-sided 95% Wilson intervals (z = 1.96), not simultaneous guarantees. The development objectives and held-out diagnostics are archived in [POLICY_SELECTION_RESULTS.md](POLICY_SELECTION_RESULTS.md).
