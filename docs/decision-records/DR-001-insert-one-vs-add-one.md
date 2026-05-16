# DR-001: Insert-One Replaces Add-One as the Canonical Perturbation

Date: 2026-05-16

## Decision

The repository standardizes on `insert-one` as the canonical perturbation notion
used by the paper, code, and tests.

Append-only `add-one` remains only as a deprecated compatibility helper meaning
"insert at the end".

## Why

Deterministic k-NN uses sample order for tie-breaking. Because of that, a
general insertion position is semantically meaningful. The paper-level
replace-one decomposition depends on same-position reinsertion:

\[
S^{i \leftarrow z} = (S^{-i}) \oplus_i z
\]

Append-only insertion cannot express this identity in general, so an
append-only helper is not sufficient for the paper's calculus or experiments.

## Consequences

- `insert_one_sample` is the primary code primitive.
- `pointwise_insert_one_stability` is the primary insertion stability API.
- Fixed-sample insertion maxima must enumerate insertion position.
- `add_one_sample` and `pointwise_add_one_stability` may remain only as
  deprecated wrappers for legacy callers and must not be cited as paper-level
  evidence.

## Indexing Convention

- Paper: insertion position is 1-based.
- Code: insertion position is 0-based.

Any proof or doc that crosses between paper and code must say which convention
it is using.
