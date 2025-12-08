# Contradiction Taxonomy

The package uses five pragmatic contradiction classes that map onto common
symbolic and neuro-symbolic tasks:

- **direct_negation** – explicit affirmation vs. denial of the same claim.
- **property_mismatch** – numeric or unit properties disagree (e.g., boiling points).
- **definitional_violation** – a query contradicts a definitional fact.
- **universal_counterexample** – counterexample presented for a universal quantifier.
- **temporal_conflict** – statements use incompatible time references against an "always" claim.

These categories align with the detectors implemented in
`contradiction.engine.ContradictionEngine` and are used across training,
benchmarking, and export utilities.
