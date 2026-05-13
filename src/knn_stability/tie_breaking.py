"""Deterministic tie-breaking helpers.

Implements the frozen tie-breaking policy from:
docs/project-control/02_DEFINITIONS_SPEC.md

Neighbor ordering is lexicographic by:
1. smaller distance to the query point
2. smaller sample index in the ordered tuple

Label vote ties are resolved by fixed label order: 0 ≺ 1
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike


def order_neighbors_by_distance_and_index(
    query_point_idx: int,
    sample_point_indices: ArrayLike,
    distances: ArrayLike,
) -> np.ndarray:
    """Order sample occurrences lexicographically by distance then occurrence index.

    Parameters
    ----------
    query_point_idx : int
        Index of the query point in the metric space.
    sample_point_indices : ArrayLike
        Sequence whose i-th entry is the metric-space point index used by the
        i-th sample occurrence.
    distances : ArrayLike
        2D distance matrix of shape (n, n) where n is the number of points
        in the metric space.

    Returns
    -------
    np.ndarray
        Array of sample occurrence indices ordered lexicographically by:
        1. ascending distance to query point
        2. ascending sample occurrence index (for distance ties)

    Notes
    -----
    This helper works at the sample-occurrence level rather than the metric
    point level, so duplicate points and conflicting labels remain distinct.
    """
    dist_matrix = np.asarray(distances, dtype=np.float64)
    sample_points = np.asarray(sample_point_indices, dtype=np.int64)
    metric_size = dist_matrix.shape[0]

    if query_point_idx < 0 or query_point_idx >= metric_size:
        raise ValueError(
            f"query_point_idx {query_point_idx} out of bounds for metric space of size {metric_size}"
        )

    if sample_points.ndim != 1:
        raise ValueError(
            f"sample_point_indices must be one-dimensional, got shape {sample_points.shape}"
        )

    if np.any(sample_points < 0) or np.any(sample_points >= metric_size):
        raise ValueError(
            "sample_point_indices contains a point index outside the metric space"
        )

    if sample_points.size == 0:
        return np.array([], dtype=np.int64)

    sample_occurrence_indices = np.arange(sample_points.size, dtype=np.int64)
    sample_distances = dist_matrix[query_point_idx, sample_points]

    # numpy.lexsort sorts by the last key first, so the tuple order is
    # (secondary_key, primary_key).
    sorted_order = np.lexsort((sample_occurrence_indices, sample_distances))

    return sorted_order


def break_label_tie(vote_counts: ArrayLike) -> int:
    """Resolve label vote ties in favor of the smaller label (0 ≺ 1).

    Parameters
    ----------
    vote_counts : ArrayLike
        Array or sequence of vote counts where index i corresponds to
        the number of votes for label i. Must contain at least indices
        0 and 1 for binary classification.

    Returns
    -------
    int
        The predicted label. Returns the label with strictly higher vote count.
        In case of a tie, returns the smaller label (0).

    Raises
    ------
    ValueError
        If vote_counts does not have at least 2 elements.

    Notes
    -----
    Per the frozen spec: "ties are always broken in favor of label 0"

    Example
    -------
    >>> break_label_tie([3, 3])  # Tie -> returns 0
    0
    >>> break_label_tie([3, 4])  # Label 1 has more votes -> returns 1
    1
    >>> break_label_tie([5, 2])  # Label 0 has more votes -> returns 0
    0
    """
    votes = np.asarray(vote_counts, dtype=np.int64)

    if votes.size < 2:
        raise ValueError(
            f"vote_counts must have at least 2 elements for binary classification, "
            f"got size {votes.size}"
        )

    # Compare votes for label 0 and label 1
    count_0 = int(votes[0])
    count_1 = int(votes[1])

    if count_0 > count_1:
        return 0
    elif count_1 > count_0:
        return 1
    else:
        # Tie: per spec, favor label 0 (0 ≺ 1)
        return 0


def select_k_neighbors(
    query_point_idx: int,
    sample_point_indices: ArrayLike,
    distances: ArrayLike,
    k: int,
) -> np.ndarray:
    """Select the first k neighbors using deterministic tie-breaking.

    Parameters
    ----------
    query_point_idx : int
        Index of the query point in the metric space.
    sample_point_indices : ArrayLike
        Sequence whose i-th entry is the metric-space point index used by the
        i-th sample occurrence.
    distances : ArrayLike
        2D distance matrix.
    k : int
        Number of neighbors to select. Must satisfy 1 <= k <= len(sample_point_indices).

    Returns
    -------
    np.ndarray
        Array of k neighbor indices ordered by distance then index.

    Raises
    ------
    ValueError
        If k is out of valid range.
    """
    sample_points = np.asarray(sample_point_indices, dtype=np.int64)
    if k < 1:
        raise ValueError(f"k must be at least 1, got {k}")
    if k > sample_points.size:
        raise ValueError(
            f"k={k} exceeds sample_size={sample_points.size}"
        )

    ordered = order_neighbors_by_distance_and_index(
        query_point_idx,
        sample_points,
        distances,
    )
    return ordered[:k]


def compute_majority_vote(neighbor_labels: ArrayLike) -> int:
    """Compute the majority label from k neighbor labels with tie-breaking.

    Parameters
    ----------
    neighbor_labels : ArrayLike
        Array of k labels from the selected neighbors.

    Returns
    -------
    int
        The majority label (0 or 1), with ties broken in favor of 0.

    Example
    -------
    >>> compute_majority_vote([0, 1, 0])  # 2 zeros, 1 one -> returns 0
    0
    >>> compute_majority_vote([1, 1, 0])  # 2 ones, 1 zero -> returns 1
    1
    >>> compute_majority_vote([0, 1])  # Tie (1,1) -> returns 0
    0
    """
    labels = np.asarray(neighbor_labels, dtype=np.int64)

    # Count votes for each label
    unique_labels, counts = np.unique(labels, return_counts=True)

    # Initialize vote counts for binary labels 0 and 1
    vote_counts = np.zeros(2, dtype=np.int64)
    for label, count in zip(unique_labels, counts):
        if label in (0, 1):
            vote_counts[label] = count

    return break_label_tie(vote_counts)
