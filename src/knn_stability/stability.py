"""Stability indicators.

Implements the frozen stability notions from:
docs/project-control/02_DEFINITIONS_SPEC.md

This module provides pointwise and fixed-sample worst-case stability
indicators for the deterministic k-NN classifier under sample perturbations:
- Delete-one (Δ_del)
- Insert-one (Δ_ins)
- Replace-one (Δ_rep)
- Leave-one-out / CVloo (Δ_loo)

Computational limitations:
- Uniform stability requires exhaustive enumeration over all perturbations
  and evaluation points, which is intractable for large metric spaces.
- Replace-one stability with z ranging over X × {0,1} has complexity O(n·|X|).

Implementation note:
- The `uniform_*` helpers in this module compute fixed-sample brute-force
  maxima over allowed perturbations and evaluation pairs. They do not
  implement the paper-level supremum over all ordered training tuples.
- In other words, they are fixed-sample brute-force maxima rather than
  full paper-level uniform stability functionals.
"""

from __future__ import annotations

import warnings

import numpy as np

from knn_stability.knn import LabeledSample, predict_knn


def binary_loss(prediction: int, label: int) -> int:
    """Compute binary 0-1 loss.

    Parameters
    ----------
    prediction : int
        The predicted label (0 or 1).
    label : int
        The true label (0 or 1).

    Returns
    -------
    int
        0 if prediction == label, 1 otherwise.
    """
    return 0 if prediction == label else 1


def delete_one_sample(sample: LabeledSample, delete_index: int) -> LabeledSample:
    """Create sample S^{-i} by deleting the i-th occurrence.

    Parameters
    ----------
    sample : LabeledSample
        The original ordered sample S.
    delete_index : int
        Index i of the occurrence to delete. Must satisfy 0 <= i < sample.n.

    Returns
    -------
    LabeledSample
        The sample with the i-th occurrence removed.

    Raises
    ------
    ValueError
        If delete_index is out of bounds.

    Notes
    -----
    This implements the delete-one perturbation from the frozen spec:
    S^{-i} = ((x_1, y_1), ..., (x_{i-1}, y_{i-1}), (x_{i+1}, y_{i+1}), ..., (x_n, y_n))
    """
    if delete_index < 0 or delete_index >= sample.n:
        raise ValueError(
            f"delete_index {delete_index} out of bounds for sample of size {sample.n}"
        )

    new_points = (
        sample.point_indices[:delete_index] + sample.point_indices[delete_index + 1 :]
    )
    new_labels = sample.labels[:delete_index] + sample.labels[delete_index + 1 :]

    return LabeledSample(
        metric=sample.metric,
        point_indices=new_points,
        labels=new_labels,
    )


def replace_one_sample(
    sample: LabeledSample,
    replace_index: int,
    new_point_idx: int,
    new_label: int,
) -> LabeledSample:
    """Create sample S^{i←z} by replacing the i-th occurrence with z=(x', y').

    Parameters
    ----------
    sample : LabeledSample
        The original ordered sample S.
    replace_index : int
        Index i of the occurrence to replace. Must satisfy 0 <= i < sample.n.
    new_point_idx : int
        Index of the new point x' in the metric space.
    new_label : int
        The new label y' (must be 0 or 1).

    Returns
    -------
    LabeledSample
        The sample with the i-th occurrence replaced by (new_point_idx, new_label).

    Raises
    ------
    ValueError
        If replace_index is out of bounds or new point/label are invalid.
    """
    if replace_index < 0 or replace_index >= sample.n:
        raise ValueError(
            f"replace_index {replace_index} out of bounds for sample of size {sample.n}"
        )

    if new_point_idx < 0 or new_point_idx >= sample.metric.n:
        raise ValueError(
            f"new_point_idx {new_point_idx} out of bounds for metric space "
            f"of size {sample.metric.n}"
        )

    if new_label not in (0, 1):
        raise ValueError(
            f"new_label must be 0 or 1, got {new_label}"
        )

    new_points = (
        sample.point_indices[:replace_index]
        + (new_point_idx,)
        + sample.point_indices[replace_index + 1 :]
    )
    new_labels = (
        sample.labels[:replace_index] + (new_label,) + sample.labels[replace_index + 1 :]
    )

    return LabeledSample(
        metric=sample.metric,
        point_indices=new_points,
        labels=new_labels,
    )


def insert_one_sample(
    sample: LabeledSample,
    insert_position: int,
    new_point_idx: int,
    new_label: int,
) -> LabeledSample:
    """Create sample S⊕_j z by inserting z=(x', y') at a given position.

    Parameters
    ----------
    sample : LabeledSample
        The original ordered sample S.
    insert_position : int
        Zero-based insertion position. Must satisfy 0 <= insert_position <= sample.n.
    new_point_idx : int
        Index of the new point x' in the metric space.
    new_label : int
        The new label y' (must be 0 or 1).

    Returns
    -------
    LabeledSample
        The sample with z inserted at the requested position.
    """
    if insert_position < 0 or insert_position > sample.n:
        raise ValueError(
            f"insert_position {insert_position} out of bounds for sample of size {sample.n}"
        )

    if new_point_idx < 0 or new_point_idx >= sample.metric.n:
        raise ValueError(
            f"new_point_idx {new_point_idx} out of bounds for metric space "
            f"of size {sample.metric.n}"
        )

    if new_label not in (0, 1):
        raise ValueError(f"new_label must be 0 or 1, got {new_label}")

    new_points = (
        sample.point_indices[:insert_position]
        + (new_point_idx,)
        + sample.point_indices[insert_position:]
    )
    new_labels = (
        sample.labels[:insert_position]
        + (new_label,)
        + sample.labels[insert_position:]
    )

    return LabeledSample(
        metric=sample.metric,
        point_indices=new_points,
        labels=new_labels,
    )


def add_one_sample(
    sample: LabeledSample,
    new_point_idx: int,
    new_label: int,
) -> LabeledSample:
    """Compatibility wrapper for append-only insertion at the end.

    Parameters
    ----------
    sample : LabeledSample
        The original ordered sample S.
    new_point_idx : int
        Index of the new point x' in the metric space.
    new_label : int
        The new label y' (must be 0 or 1).

    Returns
    -------
    LabeledSample
        The sample with z appended at the end.
    """
    warnings.warn(
        "add_one_sample is an append-only compatibility helper. "
        "Use insert_one_sample for paper-level insert-one semantics.",
        DeprecationWarning,
        stacklevel=2,
    )
    return insert_one_sample(sample, sample.n, new_point_idx, new_label)


def pointwise_delete_one_stability(
    sample: LabeledSample,
    delete_index: int,
    query_point_idx: int,
    query_label: int,
    k: int,
) -> int:
    """Pointwise delete-one stability indicator Δ_del(S, i, x, y).

    Computes |ℓ(h_S^{(k)}, (x, y)) - ℓ(h_{S^{-i}}^{(k')}, (x, y))|
    where k' = min(k, n-1) when deletion reduces sample size below k.

    Parameters
    ----------
    sample : LabeledSample
        The original ordered sample S.
    delete_index : int
        Index i of the occurrence to delete.
    query_point_idx : int
        Index of the query point x in the metric space.
    query_label : int
        The query label y (must be 0 or 1).
    k : int
        Number of nearest neighbors. Must satisfy 1 <= k <= sample.n.

    Returns
    -------
    int
        The stability indicator value (0 or 1).

    Raises
    ------
    ValueError
        If inputs are invalid.

    Notes
    -----
    Per the frozen spec, k' = min(k, n-1) handles the case where deleting
    the i-th occurrence would make k larger than the new sample size.
    """
    if k < 1:
        raise ValueError(f"k must be at least 1, got {k}")
    if k > sample.n:
        raise ValueError(f"k={k} exceeds sample size {sample.n}")

    if query_point_idx < 0 or query_point_idx >= sample.metric.n:
        raise ValueError(
            f"query_point_idx {query_point_idx} out of bounds for metric "
            f"space of size {sample.metric.n}"
        )
    if query_label not in (0, 1):
        raise ValueError(f"query_label must be 0 or 1, got {query_label}")

    # Original prediction and loss
    pred_original = predict_knn(sample, query_point_idx, k)
    loss_original = binary_loss(pred_original, query_label)

    # Deleted sample
    sample_deleted = delete_one_sample(sample, delete_index)

    # k' = min(k, n-1) for the deleted sample
    k_prime = min(k, sample_deleted.n)
    if k_prime < 1:
        raise ValueError(
            f"After deletion, k'={k_prime} is invalid. Original k={k}, "
            f"sample size after deletion={sample_deleted.n}"
        )

    # Prediction and loss on deleted sample
    pred_deleted = predict_knn(sample_deleted, query_point_idx, k_prime)
    loss_deleted = binary_loss(pred_deleted, query_label)

    return abs(loss_original - loss_deleted)


def pointwise_replace_one_stability(
    sample: LabeledSample,
    replace_index: int,
    new_point_idx: int,
    new_label: int,
    query_point_idx: int,
    query_label: int,
    k: int,
) -> int:
    """Pointwise replace-one stability indicator Δ_rep(S, i, z, x, y).

    Computes |ℓ(h_S^{(k)}, (x, y)) - ℓ(h_{S^{i←z}}^{(k)}, (x, y))|

    Parameters
    ----------
    sample : LabeledSample
        The original ordered sample S.
    replace_index : int
        Index i of the occurrence to replace.
    new_point_idx : int
        Index of the replacement point x' in the metric space.
    new_label : int
        The replacement label y' (must be 0 or 1).
    query_point_idx : int
        Index of the query point x in the metric space.
    query_label : int
        The query label y (must be 0 or 1).
    k : int
        Number of nearest neighbors. Must satisfy 1 <= k <= sample.n.

    Returns
    -------
    int
        The stability indicator value (0 or 1).

    Notes
    -----
    Per the frozen spec, z ranges over all labeled points in X × {0,1}.
    This means for each replacement position, there are 2*|X| possible
    replacements to consider for uniform stability.
    """
    if k < 1:
        raise ValueError(f"k must be at least 1, got {k}")
    if k > sample.n:
        raise ValueError(f"k={k} exceeds sample size {sample.n}")

    if query_point_idx < 0 or query_point_idx >= sample.metric.n:
        raise ValueError(
            f"query_point_idx {query_point_idx} out of bounds for metric "
            f"space of size {sample.metric.n}"
        )
    if query_label not in (0, 1):
        raise ValueError(f"query_label must be 0 or 1, got {query_label}")

    # Original prediction and loss
    pred_original = predict_knn(sample, query_point_idx, k)
    loss_original = binary_loss(pred_original, query_label)

    # Replaced sample
    sample_replaced = replace_one_sample(
        sample, replace_index, new_point_idx, new_label
    )

    # Prediction and loss on replaced sample
    pred_replaced = predict_knn(sample_replaced, query_point_idx, k)
    loss_replaced = binary_loss(pred_replaced, query_label)

    return abs(loss_original - loss_replaced)


def pointwise_insert_one_stability(
    sample: LabeledSample,
    insert_position: int,
    new_point_idx: int,
    new_label: int,
    query_point_idx: int,
    query_label: int,
    k: int,
) -> int:
    """Pointwise insert-one stability indicator Δ_ins(S, j, z, x, y).

    Computes |ℓ(h_S^{(k)}, (x, y)) - ℓ(h_{S⊕_j z}^{(k)}, (x, y))|

    Parameters
    ----------
    sample : LabeledSample
        The original ordered sample S.
    insert_position : int
        Zero-based insertion position.
    new_point_idx : int
        Index of the point x' to add in the metric space.
    new_label : int
        The label y' to add (must be 0 or 1).
    query_point_idx : int
        Index of the query point x in the metric space.
    query_label : int
        The query label y (must be 0 or 1).
    k : int
        Number of nearest neighbors. Must satisfy 1 <= k <= sample.n.

    Returns
    -------
    int
        The stability indicator value (0 or 1).
    """
    if k < 1:
        raise ValueError(f"k must be at least 1, got {k}")
    if k > sample.n:
        raise ValueError(f"k={k} exceeds sample size {sample.n}")

    if query_point_idx < 0 or query_point_idx >= sample.metric.n:
        raise ValueError(
            f"query_point_idx {query_point_idx} out of bounds for metric "
            f"space of size {sample.metric.n}"
        )
    if query_label not in (0, 1):
        raise ValueError(f"query_label must be 0 or 1, got {query_label}")

    # Original prediction and loss
    pred_original = predict_knn(sample, query_point_idx, k)
    loss_original = binary_loss(pred_original, query_label)

    sample_inserted = insert_one_sample(
        sample, insert_position, new_point_idx, new_label
    )

    pred_inserted = predict_knn(sample_inserted, query_point_idx, k)
    loss_inserted = binary_loss(pred_inserted, query_label)

    return abs(loss_original - loss_inserted)


def pointwise_add_one_stability(
    sample: LabeledSample,
    new_point_idx: int,
    new_label: int,
    query_point_idx: int,
    query_label: int,
    k: int,
) -> int:
    """Compatibility wrapper for append-only add-one stability.

    This keeps the legacy append-only helper available, but paper-facing
    semantics must use pointwise_insert_one_stability.
    """
    warnings.warn(
        "pointwise_add_one_stability is append-only compatibility behavior. "
        "Use pointwise_insert_one_stability for paper-level insert-one semantics.",
        DeprecationWarning,
        stacklevel=2,
    )
    return pointwise_insert_one_stability(
        sample,
        sample.n,
        new_point_idx,
        new_label,
        query_point_idx,
        query_label,
        k,
    )


def pointwise_loo_stability(
    sample: LabeledSample,
    delete_index: int,
    k: int,
) -> int:
    """Pointwise LOO / CVloo stability indicator Δ_loo(S, i).

    Computes |ℓ(h_{S^{-i}}^{(k')}, (x_i, y_i)) - ℓ(h_S^{(k)}, (x_i, y_i))|
    where k' = min(k, n-1) and (x_i, y_i) is the deleted occurrence.

    Parameters
    ----------
    sample : LabeledSample
        The original ordered sample S.
    delete_index : int
        Index i of the occurrence to delete and evaluate at.
    k : int
        Number of nearest neighbors. Must satisfy 1 <= k <= sample.n.

    Returns
    -------
    int
        The stability indicator value (0 or 1).

    Notes
    -----
    LOO evaluates at the deleted occurrence itself. This is distinct from
    delete-one stability because the evaluation point (x_i, y_i) is
    specifically the deleted occurrence's location and label.
    """
    if k < 1:
        raise ValueError(f"k must be at least 1, got {k}")
    if k > sample.n:
        raise ValueError(f"k={k} exceeds sample size {sample.n}")

    # Get the point and label of the deleted occurrence
    query_point_idx = sample.point_indices[delete_index]
    query_label = sample.labels[delete_index]

    # Original prediction and loss at (x_i, y_i)
    pred_original = predict_knn(sample, query_point_idx, k)
    loss_original = binary_loss(pred_original, query_label)

    # Deleted sample
    sample_deleted = delete_one_sample(sample, delete_index)

    # k' = min(k, n-1) for the deleted sample
    k_prime = min(k, sample_deleted.n)
    if k_prime < 1:
        raise ValueError(
            f"After deletion, k'={k_prime} is invalid. Original k={k}, "
            f"sample size after deletion={sample_deleted.n}"
        )

    # Prediction and loss on deleted sample, evaluated at the deleted occurrence
    # Note: query_point_idx is still valid for sample_deleted.metric (same metric)
    pred_deleted = predict_knn(sample_deleted, query_point_idx, k_prime)
    loss_deleted = binary_loss(pred_deleted, query_label)

    return abs(loss_original - loss_deleted)


# Uniform stability helpers


def uniform_delete_one_stability(
    sample: LabeledSample,
    k: int,
) -> tuple[int, int, tuple[int, int]]:
    """Fixed-sample brute-force delete-one maximum over indices and queries.

    For a fixed ordered sample ``S``, compute the maximum of
    ``Δ_del(S, i, x, y)`` over all valid delete indices ``i`` and evaluation
    pairs ``(x, y)``.

    Parameters
    ----------
    sample : LabeledSample
        The ordered sample S.
    k : int
        Number of nearest neighbors.

    Returns
    -------
    tuple[int, int, tuple[int, int]]
        A tuple containing:
        - The maximum indicator value for this fixed sample
        - The delete_index achieving the maximum
        - A tuple (query_point_idx, query_label) achieving the maximum

    Warning
    -------
    This helper is not the full paper-level uniform stability definition,
    because the sample is held fixed rather than ranging over all ordered
    tuples of the relevant size.
    """
    max_indicator = 0
    best_delete_index = 0
    best_query = (0, 0)

    for delete_index in range(sample.n):
        for query_point_idx in range(sample.metric.n):
            for query_label in (0, 1):
                indicator = pointwise_delete_one_stability(
                    sample, delete_index, query_point_idx, query_label, k
                )
                if indicator > max_indicator:
                    max_indicator = indicator
                    best_delete_index = delete_index
                    best_query = (query_point_idx, query_label)

    return (max_indicator, best_delete_index, best_query)


def uniform_replace_one_stability(
    sample: LabeledSample,
    replace_index: int,
    k: int,
) -> tuple[int, int, int, tuple[int, int]]:
    """Fixed-sample brute-force replace-one maximum for one index.

    For a fixed ordered sample ``S`` and replacement index ``i``, compute the
    maximum of ``Δ_rep(S, i, z, x, y)`` over all replacements
    ``z in X x {0,1}`` and evaluation pairs ``(x, y)``.

    Parameters
    ----------
    sample : LabeledSample
        The ordered sample S.
    replace_index : int
        The index i of the occurrence to replace.
    k : int
        Number of nearest neighbors.

    Returns
    -------
    tuple[int, int, int, tuple[int, int]]
        A tuple containing:
        - The maximum indicator value for this fixed sample and index
        - The new_point_idx achieving the maximum
        - The new_label achieving the maximum
        - A tuple (query_point_idx, query_label) achieving the maximum

    Warning
    -------
    This helper is not the full paper-level uniform stability definition,
    because the sample is fixed and only one replacement index is varied.
    """
    max_indicator = 0
    best_new_point = 0
    best_new_label = 0
    best_query = (0, 0)

    for new_point_idx in range(sample.metric.n):
        for new_label in (0, 1):
            for query_point_idx in range(sample.metric.n):
                for query_label in (0, 1):
                    indicator = pointwise_replace_one_stability(
                        sample, replace_index, new_point_idx, new_label,
                        query_point_idx, query_label, k
                    )
                    if indicator > max_indicator:
                        max_indicator = indicator
                        best_new_point = new_point_idx
                        best_new_label = new_label
                        best_query = (query_point_idx, query_label)

    return (max_indicator, best_new_point, best_new_label, best_query)


def fixed_sample_max_insert_one_stability(
    sample: LabeledSample,
    k: int,
) -> tuple[int, int, int, int, tuple[int, int]]:
    """Fixed-sample brute-force insert-one maximum over all positions and queries.

    For a fixed ordered sample ``S``, compute the maximum of
    ``Δ_ins(S, j, z, x, y)`` over all insertion positions ``j``, all
    labeled insertions ``z in X x {0,1}``, and all evaluation pairs ``(x, y)``.

    Parameters
    ----------
    sample : LabeledSample
        The ordered sample S.
    k : int
        Number of nearest neighbors.

    Returns
    -------
    tuple[int, int, int, int, tuple[int, int]]
        A tuple containing:
        - The maximum indicator value for this fixed sample
        - The insertion position achieving the maximum
        - The new point index achieving the maximum
        - The new label achieving the maximum
        - A tuple (query_point_idx, query_label) achieving the maximum
    """
    max_indicator = 0
    best_insert_position = 0
    best_new_point = 0
    best_new_label = 0
    best_query = (0, 0)

    for insert_position in range(sample.n + 1):
        for new_point_idx in range(sample.metric.n):
            for new_label in (0, 1):
                for query_point_idx in range(sample.metric.n):
                    for query_label in (0, 1):
                        indicator = pointwise_insert_one_stability(
                            sample,
                            insert_position,
                            new_point_idx,
                            new_label,
                            query_point_idx,
                            query_label,
                            k,
                        )
                        if indicator > max_indicator:
                            max_indicator = indicator
                            best_insert_position = insert_position
                            best_new_point = new_point_idx
                            best_new_label = new_label
                            best_query = (query_point_idx, query_label)

    return (
        max_indicator,
        best_insert_position,
        best_new_point,
        best_new_label,
        best_query,
    )


def uniform_add_one_stability(
    sample: LabeledSample,
    new_point_idx: int,
    new_label: int,
    k: int,
) -> tuple[int, tuple[int, int]]:
    """Compatibility wrapper for append-only add-one fixed-sample maxima."""
    warnings.warn(
        "uniform_add_one_stability is append-only compatibility behavior. "
        "Use fixed_sample_max_insert_one_stability for paper-level insert-one semantics.",
        DeprecationWarning,
        stacklevel=2,
    )
    max_indicator = 0
    best_query = (0, 0)

    for query_point_idx in range(sample.metric.n):
        for query_label in (0, 1):
            indicator = pointwise_insert_one_stability(
                sample,
                sample.n,
                new_point_idx,
                new_label,
                query_point_idx,
                query_label,
                k,
            )
            if indicator > max_indicator:
                max_indicator = indicator
                best_query = (query_point_idx, query_label)

    return (max_indicator, best_query)


def uniform_loo_stability(sample: LabeledSample, k: int) -> tuple[int, int]:
    """Fixed-sample brute-force LOO maximum over deleted indices.

    For a fixed ordered sample ``S``, compute the maximum of ``Δ_loo(S, i)``
    over all valid delete indices ``i``.

    Parameters
    ----------
    sample : LabeledSample
        The ordered sample S.
    k : int
        Number of nearest neighbors.

    Returns
    -------
    tuple[int, int]
        A tuple containing:
        - The maximum indicator value for this fixed sample
        - The delete_index achieving the maximum

    Warning
    -------
    This helper is not the full paper-level uniform stability definition,
    because the sample is held fixed.
    """
    max_indicator = 0
    best_delete_index = 0

    for delete_index in range(sample.n):
        indicator = pointwise_loo_stability(sample, delete_index, k)
        if indicator > max_indicator:
            max_indicator = indicator
            best_delete_index = delete_index

    return (max_indicator, best_delete_index)
