# Definitions Specification

Status: frozen v0.2 on 2026-05-16. This document is the canonical authority for
the paper, code, and tests unless superseded by a later decision record.

## Core Domain

### Sample

A training sample is an ordered tuple

\[
S = \big((x_1, y_1), \ldots, (x_n, y_n)\big)
\]

where each \(x_i\) lies in a finite metric space \((X, d)\) and each label
\(y_i\) lies in \(\{0, 1\}\).

The order is semantically relevant for deterministic tie-breaking. Two
identical labeled points at different indices are distinct sample occurrences.

### Duplicate points and conflicting labels

- Duplicate points are allowed.
- Conflicting labels at the same point are allowed.
- Any theorem or experiment that excludes duplicates or conflicts must state so
  explicitly.

### Finite metric space

A finite metric space is a finite set \(X\) together with a function

\[
d : X \times X \to \mathbb{R}_{\ge 0}
\]

satisfying:

- \(d(x, x) = 0\)
- \(d(x, x') > 0\) for \(x \ne x'\)
- \(d(x, x') = d(x', x)\)
- \(d(x, z) \le d(x, y) + d(y, z)\)

The code interface may represent \(X\) by indexed points and \(d\) by a
validated distance matrix.

### Graph shortest-path metric

For a finite, simple, connected, unweighted, undirected graph \(G = (V, E)\),
the graph metric is

\[
d_G(u, v) = \text{length of a shortest path from } u \text{ to } v.
\]

## Prediction Rule

### Query points

The query point \(x\) may be any element of \(X\), including one that already
appears in the training sample.

### Deterministic tie-breaking

Neighbor ordering is determined lexicographically by:

1. smaller distance to the query point
2. smaller sample index in the ordered tuple

If class votes tie after the first \(k\) ordered neighbors are selected, the
predicted label is resolved by fixed label order \(0 \prec 1\). Ties therefore
break in favor of label \(0\).

### k-NN prediction

Given \(k \in \mathbb{N}\) with \(1 \le k \le n\), the deterministic k-NN
predictor \(h_S^{(k)}(x)\) is obtained by:

1. ordering the sample occurrences by the deterministic neighbor rule above
2. selecting the first \(k\) occurrences
3. taking the majority vote of their labels
4. resolving label-vote ties by \(0 \prec 1\)

## Loss

The active loss is binary classification 0-1 loss:

\[
\ell(h, (x, y)) = \mathbf{1}\{h(x) \ne y\}.
\]

## Sample Perturbations

Let

\[
S = \big((x_1, y_1), \ldots, (x_n, y_n)\big).
\]

### Delete-one

For index \(i\), define

\[
S^{-i}
\]

as the ordered tuple obtained by removing the \(i\)-th occurrence.

### Insert-one

For any labeled point \(z = (x, y) \in X \times \{0, 1\}\) and any insertion
position \(j \in \{1, \ldots, n+1\}\), define

\[
S \oplus_j z
\]

as the ordered tuple obtained by inserting \(z\) at position \(j\).

Code uses 0-based insertion positions:

- paper position \(j \in \{1, \ldots, n+1\}\)
- code position `insert_position in {0, ..., n}`

### Replace-one

For index \(i\) and labeled point \(z = (x', y') \in X \times \{0, 1\}\),
define

\[
S^{i \leftarrow z}
\]

as the ordered tuple obtained by replacing the \(i\)-th occurrence with \(z\).

Replace-one factors through delete-plus-insert at the same index:

\[
S^{i \leftarrow z} = (S^{-i}) \oplus_i z
\]

in 1-based paper indexing, or equivalently insert at `delete_index` in 0-based
code indexing.

### Append-only compatibility helper

The legacy append-only operation

\[
S \oplus z
\]

is not a paper-level perturbation notion anymore. In code it may remain only as
an explicit compatibility helper meaning “insert at the end”.

## Stability Notions

### Pointwise delete-one stability indicator

For index \(i\) and query-label pair \((x, y)\), define

\[
\Delta_{\mathrm{del}}(S, i, x, y)
=
\left| \ell(h_S^{(k)}, (x, y)) - \ell(h_{S^{-i}}^{(k')}, (x, y)) \right|,
\]

where \(k' = \min(k, n-1)\) when deletion reduces sample size below \(k\).

### Pointwise insert-one stability indicator

For insertion position \(j\), inserted labeled point \(z\), and query-label
pair \((x, y)\), define

\[
\Delta_{\mathrm{ins}}(S, j, z, x, y)
=
\left| \ell(h_S^{(k)}, (x, y)) - \ell(h_{S \oplus_j z}^{(k)}, (x, y)) \right|.
\]

### Pointwise replace-one stability indicator

For index \(i\), replacement \(z\), and query-label pair \((x, y)\), define

\[
\Delta_{\mathrm{rep}}(S, i, z, x, y)
=
\left| \ell(h_S^{(k)}, (x, y)) - \ell(h_{S^{i \leftarrow z}}^{(k)}, (x, y)) \right|.
\]

### LOO / CVloo stability

For each deleted occurrence \(i\),

\[
\Delta_{\mathrm{loo}}(S, i)
=
\left| \ell(h_{S^{-i}}^{(k')}, (x_i, y_i)) - \ell(h_S^{(k)}, (x_i, y_i)) \right|.
\]

LOO is delete-one with the evaluation point fixed to the deleted occurrence.

### Fixed-sample maxima vs paper-level uniform stability

Pointwise statements fix a sample, perturbation, and evaluation pair.

Expected stability refers to expectations under an explicitly stated
distributional setup.

Paper-level uniform stability is the supremum over all valid samples,
perturbations, and evaluation pairs of the relevant size.

The current Python helpers named `uniform_*` are fixed-sample brute-force
maxima, not full paper-level uniform stability functionals. Code and prose must
say that explicitly.

## Implementation Notes

- Code treats samples as ordered tuples of labeled occurrences.
- Code insertion positions are 0-based and must satisfy
  `0 <= insert_position <= sample.n`.
- Paper positions are 1-based and must satisfy \(1 \le j \le n+1\).
- The deprecated append-only helper must not be used as evidence for
  paper-level insert-one statements.
