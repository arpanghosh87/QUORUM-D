# Manuscript cross-reference

This repository accompanies a narrative critical review and its proposed conceptual framework. The following mapping uses the final manuscript numbering.

| Manuscript element | Artifact |
|---|---|
| Equations 1–5 | `quorum_d/statistics.py`, `tests/test_statistics.py` |
| Figure 3 and Table 5 (exact counterexample) | `scripts/strengthen.py`, `results/strengthening.json` |
| Figures 4–6 and Table 6 (analytical illustrations) | `scripts/reproduce.py`, `results/table5.csv` |
| Section 5.1 Bernoulli construction | `results/synthetic_correlation.csv` |
| Section 4.5 pivotal-margin property | `tests/test_statistics.py` |
| Section 4.3.1 calibration and routing | `scripts/claim_experiments.py`, `scripts/strengthen.py` |
| Algorithm 1 and Section 6.5 | `quorum_d/reference.py`, `quorum_d/policy.py` (restricted finite-menu demonstration) |
| Figure 8 and Table 9 | `results/reference_heldout.csv`, `results/strengthening.json`, `docs/POLICY_SELECTION_RESULTS.md` |

The filename `table5.csv` retains its historical identifier for compatibility; it corresponds to Table 6 in the final manuscript. No new empirical results, literature or production claims are introduced by this package. See [claim traceability](claims.md), [figure guide](FIGURE_GUIDE.md) and [provenance](FINAL_VERIFICATION.md).

## Revised policy-selection reporting

The manuscript distinguishes development selection from held-out feasibility. Supplement S1, §S1.8 adds the four feasible development objectives and six held-out feasibility diagnostics from the existing [policy-selection archive](POLICY_SELECTION_RESULTS.md). The proposed algorithm's mandatory-baseline budget safeguard is not implemented for arbitrary truncated searches; all 37 candidates were evaluated in the reported demonstration. Selection uses the exact objective, complexity and policy name in that order. No results or scientific code were changed.
