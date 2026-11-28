# Publication figure guide

All figures are derived from the archived analytical or synthetic data, not observations of real LLMs. The lettered filenames are stable identifiers independent of manuscript numbering.

| File | Placement | Evidence |
|---|---|---|
| [A_ess_counterexample.svg](../results/figures/A_ess_counterexample.svg) | Main paper, Figure 3 | Exact matched-moment counterexample |
| [B_policy_tradeoffs.svg](../results/figures/B_policy_tradeoffs.svg) | Main paper, Figure 8 | Synthetic held-out comparison and paired intervals |
| [C_conditional_dependence.svg](../results/figures/C_conditional_dependence.svg) | Supplementary Figure S1 | Synthetic routed-subset dependence |
| [D_calibration_sensitivity.svg](../results/figures/D_calibration_sensitivity.svg) | Repository or supplement | Synthetic finite calibration |
| [E_covariance_weighting.svg](../results/figures/E_covariance_weighting.svg) | Repository or supplement | Analytical unequal-variance example |

## Captions

**A.** Identical effective sample size does not identify majority correctness. Three exchangeable binary judges have marginal correctness 0.75, zero pairwise correlation and ESS 3. (a) Exact majority correctness under three joint distributions. (b) Probability mass functions of the count of correct judges, with the majority-correct region shaded. Zero pairwise correlation does not establish mutual independence.

**B.** Synthetic held-out policy comparison (4,000 items). (a) Assumed expenditure versus arithmetic mean of dimension-specific accepted error rates. Feasibility is determined separately by the declared budget, latency, coverage and dimension-risk criteria, including Wilson upper endpoints. Uniform and competence-weighted panels coincide in the plotted measures. The shared policy was selected on development data, not from this test plot. (b) Shared-minus-separate error differences with descriptive pointwise 95% paired percentile bootstrap intervals (2,000 repetitions per dimension). Negative differences favor the shared configuration. All costs and judge performance are synthetic assumptions; no real-world savings or superiority is established.

**C.** Reference-defined pairwise error correlations for the full synthetic workload (4,000 items) and the one-vote-margin routed subset (1,070 items). A common diverging scale is used. Conditional dependence is not workload-level dependence; routing uses observable ballots, not reference labels.

**D.** Synthetic calibration sensitivity. (a) Mean held-out ESS and one standard deviation across successful fits only. (b) Successful and failed fits out of 50 attempts for each calibration size. No universal minimum calibration size is inferred.

**E.** Analytical unequal-variance example. (a) Uniform versus minimum-variance weighted-mean error variance. (b) Optimized nonnegative weights for independent Bernoulli error probabilities 0.10, 0.30 and 0.50. Reduced variance does not establish reduced classification error or actual expenditure.

## Reproduction

```sh
node scripts/publication_figures.cjs
node scripts/publication_figures.cjs /tmp/quorum-figures
diff -r results/figures /tmp/quorum-figures
```

Node.js 18+; no external packages required. SVGs are standalone vector artwork with white backgrounds, explicit labels, and colorblind-friendly palette. For PDF and 600 dpi PNG export, use the companion Python conversion script (requires CairoSVG and its system Cairo library). Figure data are the committed strengthening JSON and held-out/calibration CSV files. The figures do not add experiments or alter numerical snapshots.
