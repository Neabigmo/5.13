# Definitions Specification

Status: frozen v0.1 on 2026-05-13. This document is the sole authority for code and paper definitions until superseded by a later decision record.

## Core Domain

### Sample

A training sample is an ordered tuple

\[
S = \big((x_1, y_1), \ldots, (x_n, y_n)\big)
\]

where each \(x_i\) lies in a finite metric space \((X, d)\) and each label \(y_i\) lies in \(\{0, 1\}\).

The order is semantically relevant only for deterministic tie-breaking. Two identical labeled points appearing at different indices are treated as distinct sample occurrences.

### Duplicate points and conflicting labels

- Duplicate points are allowed.
- Conflicting labels at the same point are allowed.
- Any theorem or experiment that excludes duplicates or conflicts must say so explicitly.

### Finite metric space

A finite metric space is a finite set \(X\) together with a function

\[
d : X \times X \to \mathbb{R}_{\ge 0}
\]

satisfying:

- \(d(x, x) = 0\);
- \(d(x, x') > 0\) for \(x \ne x'\);
- \(d(x, x') = d(x', x)\);
- \(d(x, z) \le d(x, y) + d(y, z)\).

The code v0.1 interface may represent \(X\) by indexed points and \(d\) by a validated distance matrix.

### Graph shortest-path metric

For a finite, simple, connected, unweighted, undirected graph \(G = (V, E)\), the graph metric is

\[
d_G(u, v) = \text{length of a shortest path from } u \text{ to } v.
\]

Disconnected graphs are rejected in code paths that require a metric.

## Prediction Rule

### Query points

The query point \(x\) may be any element of \(X\), including a point that appears in the training sample.

### Deterministic tie-breaking

Neighbor ordering is determined lexicographically by:

1. smaller distance to the query point;
2. smaller sample index in the ordered tuple.

If class votes tie after the first \(k\) ordered neighbors are selected, the predicted label is resolved by fixed label order \(0 \prec 1\). Therefore ties are always broken in favor of label \(0\).

### k-NN prediction

Given \(k \in \mathbb{N}\) with \(1 \le k \le n\), the deterministic k-NN predictor \(h_S^{(k)}(x)\) is obtained by:

1. ordering the sample occurrences by the deterministic neighbor rule above;
2. selecting the first \(k\) occurrences;
3. taking the majority vote of their labels;
4. resolving label-vote ties by \(0 \prec 1\).

## Loss

The v0.1 loss is binary classification 0-1 loss:

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
S^{-i} = \big((x_1, y_1), \ldots, (x_{i-1}, y_{i-1}), (x_{i+1}, y_{i+1}), \ldots, (x_n, y_n)\big).
\]

### Add-one

For any labeled point \(z = (x, y) \in X \times \{0,1\}\), define

\[
S \oplus z
\]

as the ordered tuple obtained by appending \(z\) at the end.

### Replace-one

For index \(i\) and labeled point \(z = (x', y') \in X \times \{0,1\}\), define

\[
S^{i \leftarrow z}
\]

as the ordered tuple obtained by replacing the \(i\)-th occurrence of \(S\) with \(z\).

In v0.1 worst-case stability definitions, the replacement point ranges over all labeled points in \(X \times \{0,1\}\), not over a data-generating distribution.

## Stability Notions

Unless otherwise stated, all pointwise notions are evaluated with fixed \(k\), fixed metric space, fixed tie-breaking rule, and fixed loss above.

### Pointwise delete-one stability indicator

For index \(i\) and query-label pair \((x, y)\), define

\[
\Delta_{\mathrm{del}}(S, i, x, y)
=
\left| \ell(h_S^{(k)}, (x, y)) - \ell(h_{S^{-i}}^{(k')}, (x, y)) \right|,
\]

where \(k' = \min(k, n-1)\) when deletion reduces sample size below \(k\).

### Pointwise replace-one stability indicator

For index \(i\), replacement \(z\), and query-label pair \((x, y)\), define

\[
\Delta_{\mathrm{rep}}(S, i, z, x, y)
=
\left| \ell(h_S^{(k)}, (x, y)) - \ell(h_{S^{i \leftarrow z}}^{(k)}, (x, y)) \right|.
\]

### Pointwise add-one stability indicator

For added labeled point \(z\) and query-label pair \((x, y)\), define

\[
\Delta_{\mathrm{add}}(S, z, x, y)
=
\left| \ell(h_S^{(k)}, (x, y)) - \ell(h_{S \oplus z}^{(k)}, (x, y)) \right|.
\]

### LOO / CVloo stability

LOO evaluates at the deleted sample occurrence itself. For each \(i\),

\[
\Delta_{\mathrm{loo}}(S, i)
=
\left| \ell(h_{S^{-i}}^{(k')}, (x_i, y_i)) - \ell(h_S^{(k)}, (x_i, y_i)) \right|.
\]

This definition is occurrence-based: if the same point appears twice, deleting one copy and evaluating at that occurrence is distinct from deleting the other.

### Pointwise stability

A pointwise stability statement concerns a fixed training sample, a fixed perturbation, and a fixed evaluation pair \((x, y)\).

### Expected stability

Expected stability refers to the expectation of the corresponding indicator under an explicitly specified data-generating distribution and sampling procedure. No expected-stability code path is authoritative unless the distributional setup is stated.

### Uniform stability

Uniform stability for a perturbation type is the supremum of the corresponding indicator over:

- all valid ordered training tuples \(S\) of the relevant size;
- all allowed perturbation choices for that notion;
- all evaluation pairs \((x, y) \in X \times \{0,1\}\).

For LOO, the evaluation pair is fixed to the deleted occurrence, so the supremum is over ordered tuples \(S\) and indices \(i\).

## Consistency

The consistency notion used in paper-level discussion is classical distributional consistency for k-NN classification. It is not a finite-sequence surrogate notion. Any finite-metric experiment is evidence about worst-case stability behavior, not by itself a consistency statement.

## Implementation Notes Bound To This Spec

- v0.1 code should treat samples as ordered tuples of labeled occurrences.
- Deterministic tie-breaking must be index-stable and auditable.
- Stability code must not silently replace the frozen label order or query convention.
- Any later change to sample semantics, label space, or tie-breaking requires a decision record before implementation changes.
