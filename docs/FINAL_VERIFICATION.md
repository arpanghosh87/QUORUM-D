# Research provenance and verification

## Research disclosures and verification baseline

On 26 November 2026, development CI at the development commit passed 21 tests, reproduced eight archived artifacts, matched five publication SVGs and completed PDF/PNG exports. Historical verification does not substitute for CI on this snapshot.

## Publication snapshot verification

The new repository has its own CI workflow. Run `python -m pytest -q` and `python -m scripts.verify_archive` from the root, or consult the Actions tab for the exact publication commit. Historical success is not evidence of a fresh run on the publication commit. The report generator and archived report have synchronized editorial changes; numerical archives and scientific logic are unchanged.

## Verified selection in the historical run

All 37 development candidates were evaluated; four satisfied the prespecified constraints. The selected shared+shared configuration had development objective 0.065 and held-out objective 0.0641375. See [complete results](POLICY_SELECTION_RESULTS.md). All evidence is analytical or synthetic. No real LLM evaluation, measured production cost, independent replication of cited studies, or complete general Algorithm 1 implementation is claimed.
