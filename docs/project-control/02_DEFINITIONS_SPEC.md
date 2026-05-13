# Definitions Specification

Status: draft v0.1. This document is the sole authority for code and paper definitions. Do not implement final stability logic until Codex freezes this document.

## Objects To Define

- Sample representation: ordered tuple, multiset, or set.
- Finite metric space.
- Graph shortest-path metric.
- Deterministic tie-breaking.
- k-NN prediction rule.
- Binary labels and 0-1 loss.
- Delete-one stability.
- Add-one stability.
- Replace-one stability.
- CVloo / LOO stability.
- Pointwise stability.
- Expected stability.
- Uniform stability.
- Consistency notion.

## Decisions Required Before Freeze

1. Whether training samples are ordered tuples, multisets, or sets.
2. Whether repeated points are allowed.
3. Whether the same point may appear with conflicting labels.
4. Whether the query point may be a training point.
5. Whether LOO evaluates at the deleted point.
6. Whether replace-one replacements are arbitrary labeled points or distributional draws.
7. Whether tie-breaking uses vertex order, sample index order, label order, or a combined rule.
8. Whether labels are binary only in v0.1.
9. Whether consistency is classical distributional consistency or finite-sequence consistency.
10. The supremum domain in uniform stability.

## Default Draft Choices For Early Infrastructure

- Labels are binary for initial code tasks.
- Loss is 0-1 classification loss.
- Tie-breaking must be deterministic and explicitly documented.
- Computational evidence must remain separate from theorem statements.

