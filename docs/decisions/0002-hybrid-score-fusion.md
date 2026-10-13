# ADR 0002: Reciprocal Rank Fusion as initial hybrid baseline

- Status: Proposed
- Context: BM25 and dense retrievers produce scores on different scales.
- Decision: Use RRF as the initial fusion baseline and compare it against calibrated weighted fusion offline.
- Consequences: Robust to raw score-scale differences; discards some score magnitude information.
- Revisit when: a sufficiently large judged dataset supports calibration or learning-to-rank.
