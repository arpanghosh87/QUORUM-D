# Reproducibility verification

## Historical development run

Python 3.13.5, NumPy 2.3.5, Matplotlib 3.10.8 and pytest 9.0.2. The final targeted suite passed 21 tests. The numerical archive was regenerated in a separate temporary directory (no overwrite of the expected snapshots). All seven comparisons passed.

- table5.csv
- majority_simulation.csv
- calibration_sensitivity.csv
- synthetic_correlation.csv
- reference_heldout.csv (extracted from regenerated reference_demo.json)
- strengthening.json
- FINAL_RESEARCH_OUTCOMES.md

Numeric comparisons use absolute tolerance 1e-12 and relative tolerance 1e-9; text, schema and row ordering must match. The generated Markdown report must match its archived content. No empirical model data were used.

## Commands

```sh
python -m pip install -r requirements-reproduce.txt
python -m pip install -e '.[test]'
python -m pytest -q
python -m scripts.verify_archive
```

The requirements file pins direct dependencies, not every transitive dependency. The pinned environment requires Python 3.11 or newer. GitHub Actions reruns tests and archive verification before generating downloadable figures and experiment outputs. Inspect the actual PR checks for CI status. Publication SVGs are compared byte-for-byte in CI; rendered PDF and PNG exports are generated but are not pixel-hash verified. The archived numeric results are analytical or synthetic; the verifier does not validate primary-source findings, every Algorithm 1 safeguard, or real LLM performance.

## Historical baseline and policy report

See [final verification](FINAL_VERIFICATION.md) for historical main-branch CI run 45886588454 and the distinction between the historical seven-artifact comparison and the added eighth policy-selection Markdown comparison. See [full development and held-out results](POLICY_SELECTION_RESULTS.md). The original local run above refers to the earlier research package.
