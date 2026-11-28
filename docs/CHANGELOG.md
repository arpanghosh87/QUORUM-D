# Research changelog

The following entries describe the earlier development repository, not pull requests in this publication repository.

## Targeted strengthening (PR #2)

- Added exact exchangeable Bernoulli counterexamples, including competent judges with identical pairwise correlations and ESS but different majority probabilities.
- Added reference-normalized full-covariance variance and small-panel constrained minimum-variance weighting.
- Added jointly evaluated routed-subset dependence and paired descriptive bootstrap intervals on the existing synthetic tape.
- Added seven targeted tests, including failure and inconclusive held-out decisions and archive mismatch detection.
- Added a generated final outcomes Markdown report and numerical JSON snapshot.
- Added isolated archive verification to CI and documented reproduction dependencies.
- Preserved all earlier analytical and synthetic outputs and the restricted scope of the reference policy search.

No new literature, real-model evaluations, software SDK or production claims.

## Publication handoff (PR #4)

- Clarified the historical 14-test count and current 21-test suite.
- Archived all 37 development candidate summaries and the six held-out summaries with Wilson upper limits and constraint violations, sourced from merged-main CI output.
- Added deterministic report generation and archive comparison; no scientific algorithm or existing numerical snapshot changed.

## Publication snapshot

Reader-facing documentation and manuscript cross-references updated. Scientific implementation, parameters, numerical archives, tests, and figure data preserved. Report prose and its generator were updated together. See [provenance](FINAL_VERIFICATION.md).
