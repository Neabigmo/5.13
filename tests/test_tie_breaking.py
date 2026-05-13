"""Tests for deterministic tie-breaking helpers."""

import numpy as np
import pytest

from knn_stability.tie_breaking import (
    break_label_tie,
    compute_majority_vote,
    order_neighbors_by_distance_and_index,
    select_k_neighbors,
)


class TestOrderNeighborsByDistanceAndIndex:
    """Test neighbor ordering with deterministic tie-breaking."""

    def test_ascending_distances(self):
        """Neighborhood ordered by strictly increasing distance."""
        # 3 points: query is at index 0
        # dists to query: point 0 = 0, point 1 = 1, point 2 = 2
        distances = [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
        result = order_neighbors_by_distance_and_index(0, [0, 1, 2], distances)
        np.testing.assert_array_equal(result, [0, 1, 2])

    def test_distance_tie_broken_by_index(self):
        """Points at equal distance ordered by smaller sample index first."""
        # Query at index 0, points 1 and 2 are both at distance 1 from query
        distances = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
        result = order_neighbors_by_distance_and_index(0, [0, 1, 2], distances)
        # Point 0 at dist 0, then point 1 (index 1) before point 2 (index 2)
        np.testing.assert_array_equal(result, [0, 1, 2])

    def test_distance_tie_at_later_position(self):
        """Tie-breaking by index applies at any distance level."""
        # Query at index 3, points 0, 1, 2 all at distance 2 from point 3
        distances = [
            [0, 1, 1, 2],
            [1, 0, 1, 2],
            [1, 1, 0, 2],
            [2, 2, 2, 0],
        ]
        result = order_neighbors_by_distance_and_index(3, [0, 1, 2, 3], distances)
        # Point 3 at dist 0, then points 0, 1, 2 at dist 2 (index order)
        np.testing.assert_array_equal(result, [3, 0, 1, 2])

    def test_sample_occurrences_can_be_subset_of_metric_space(self):
        """Ordering respects explicit sample occurrences."""
        # 5 points in metric space, sample uses only points 0, 2, 4.
        distances = [[0, 1, 2, 3, 4], [1, 0, 1, 2, 3], [2, 1, 0, 1, 2],
                     [3, 2, 1, 0, 1], [4, 3, 2, 1, 0]]
        result = order_neighbors_by_distance_and_index(0, [0, 2, 4], distances)
        # Distances: point 0=0, point 2=2, point 4=4
        np.testing.assert_array_equal(result, [0, 1, 2])

    def test_query_point_not_in_sample_occurrences(self):
        """Query at index outside sample ordering still works."""
        distances = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
        result = order_neighbors_by_distance_and_index(2, [0, 1], distances)
        # Distances from point 2: point 0=1, point 1=1 (tie by index)
        np.testing.assert_array_equal(result, [0, 1])

    def test_single_point_sample(self):
        """Single point sample."""
        distances = [[0, 1], [1, 0]]
        result = order_neighbors_by_distance_and_index(0, [0], distances)
        np.testing.assert_array_equal(result, [0])

    def test_query_idx_out_of_bounds(self):
        """Query index out of bounds raises ValueError."""
        distances = [[0, 1], [1, 0]]
        with pytest.raises(ValueError, match="out of bounds"):
            order_neighbors_by_distance_and_index(5, [0, 1], distances)

    def test_sample_point_index_out_of_bounds(self):
        """Sample occurrence referencing a missing metric point raises ValueError."""
        distances = [[0, 1], [1, 0]]
        with pytest.raises(ValueError, match="outside the metric space"):
            order_neighbors_by_distance_and_index(0, [0, 2], distances)

    def test_empty_sample(self):
        """Empty sample returns empty ordering."""
        distances = [[0]]
        result = order_neighbors_by_distance_and_index(0, [], distances)
        np.testing.assert_array_equal(result, np.array([], dtype=int))

    def test_duplicate_metric_points_remain_distinct_occurrences(self):
        """Duplicate sample points stay distinct through occurrence-index ordering."""
        distances = [[0, 1], [1, 0]]
        result = order_neighbors_by_distance_and_index(1, [0, 0, 1], distances)
        # The exact query-point occurrence comes first at distance 0.
        # The two copies of point 0 then appear in occurrence-index order.
        np.testing.assert_array_equal(result, [2, 0, 1])


class TestBreakLabelTie:
    """Test label vote tie-breaking: 0 ≺ 1 (ties favor 0)."""

    def test_strict_majority_label_0(self):
        """Strict majority for label 0 returns 0."""
        result = break_label_tie([5, 3])
        assert result == 0

    def test_strict_majority_label_1(self):
        """Strict majority for label 1 returns 1."""
        result = break_label_tie([3, 5])
        assert result == 1

    def test_tie_returns_0(self):
        """Equal votes returns 0 per tie-breaking rule (0 ≺ 1)."""
        result = break_label_tie([3, 3])
        assert result == 0

    def test_tie_with_unequal_vote_counts(self):
        """Label with strictly higher count wins, even if both >= 0."""
        result = break_label_tie([10, 10])  # Tie
        assert result == 0
        result = break_label_tie([0, 1])  # Not a tie
        assert result == 1

    def test_zero_votes_both_labels(self):
        """Zero votes for both labels returns 0 (tie-breaking)."""
        result = break_label_tie([0, 0])
        assert result == 0

    def test_single_vote_each_tie_breaks_to_0(self):
        """One vote each ties, returns 0."""
        result = break_label_tie([1, 1])
        assert result == 0

    def test_insufficient_labels_raises(self):
        """Fewer than 2 labels raises ValueError."""
        with pytest.raises(ValueError, match="at least 2 elements"):
            break_label_tie([5])

    def test_empty_array_raises(self):
        """Empty array raises ValueError."""
        with pytest.raises(ValueError, match="at least 2 elements"):
            break_label_tie([])

    def test_numpy_array_input(self):
        """NumPy array input is accepted."""
        votes = np.array([3, 2])
        result = break_label_tie(votes)
        assert result == 0


class TestSelectKNeighbors:
    """Test k-neighbor selection with tie-breaking."""

    def test_k_equals_1(self):
        """k=1 selects the closest neighbor."""
        distances = [[0, 2, 1], [2, 0, 1], [1, 1, 0]]
        result = select_k_neighbors(0, [0, 1, 2], distances, 1)
        np.testing.assert_array_equal(result, [0])

    def test_k_equals_sample_size(self):
        """k=sample_size returns all neighbors in order."""
        distances = [[0, 1, 2], [1, 0, 1], [2, 1, 0]]
        result = select_k_neighbors(0, [0, 1, 2], distances, 3)
        np.testing.assert_array_equal(result, [0, 1, 2])

    def test_k_with_distance_ties(self):
        """k neighbors selected with tie-breaking for equal distances."""
        # Query at index 0, points 1 and 2 at same distance
        distances = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
        result = select_k_neighbors(0, [0, 1, 2], distances, 2)
        # Should pick point 0 (dist 0) and point 1 (dist 1, lower index)
        np.testing.assert_array_equal(result, [0, 1])

    def test_k_zero_raises(self):
        """k=0 raises ValueError."""
        distances = [[0, 1], [1, 0]]
        with pytest.raises(ValueError, match="at least 1"):
            select_k_neighbors(0, [0, 1], distances, 0)

    def test_k_exceeds_sample_size_raises(self):
        """k > sample_size raises ValueError."""
        distances = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
        with pytest.raises(ValueError, match="exceeds sample_size"):
            select_k_neighbors(0, [0, 1, 2], distances, 5)


class TestComputeMajorityVote:
    """Test majority vote computation with tie-breaking."""

    def test_unanimous_label_0(self):
        """All neighbors vote label 0, returns 0."""
        result = compute_majority_vote([0, 0, 0])
        assert result == 0

    def test_unanimous_label_1(self):
        """All neighbors vote label 1, returns 1."""
        result = compute_majority_vote([1, 1, 1])
        assert result == 1

    def test_strict_majority_0(self):
        """More votes for 0 than 1 returns 0."""
        result = compute_majority_vote([0, 1, 0])
        assert result == 0

    def test_strict_majority_1(self):
        """More votes for 1 than 0 returns 1."""
        result = compute_majority_vote([0, 1, 1])
        assert result == 1

    def test_tie_breaks_to_0(self):
        """Equal votes (1,1) returns 0 per tie-breaking rule."""
        result = compute_majority_vote([0, 1])
        assert result == 0

    def test_tie_3_each(self):
        """Tie with 3 votes each returns 0."""
        result = compute_majority_vote([0, 1, 0, 1, 0, 1])
        assert result == 0

    def test_empty_neighbors(self):
        """Empty neighbor list returns 0 (zero votes is a tie)."""
        result = compute_majority_vote([])
        assert result == 0

    def test_only_label_0_present(self):
        """Only label 0 present returns 0."""
        result = compute_majority_vote([0, 0])
        assert result == 0

    def test_only_label_1_present(self):
        """Only label 1 present returns 1."""
        result = compute_majority_vote([1, 1, 1])
        assert result == 1

    def test_neighbor_labels_as_numpy_array(self):
        """NumPy array of labels is accepted."""
        labels = np.array([0, 1, 1])
        result = compute_majority_vote(labels)
        assert result == 1


class TestIntegrationDistanceAndLabelTies:
    """Integration tests combining distance and label tie-breaking."""

    def test_distance_tie_then_label_tie(self):
        """Both distance and label ties are correctly resolved."""
        # Setup: Query at point 0
        # Points 1 and 2 at distance 1 (tie, resolved by index)
        # Among k=2 neighbors (points 0, 1): labels 0 and 1 (tie, resolved to 0)
        distances = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]

        # Order neighbors
        ordered = order_neighbors_by_distance_and_index(0, [0, 1, 2], distances)
        np.testing.assert_array_equal(ordered, [0, 1, 2])

        # Select k=2 neighbors
        neighbors = select_k_neighbors(0, [0, 1, 2], distances, 2)
        np.testing.assert_array_equal(neighbors, [0, 1])

        # Labels: point 0 has label 0, point 1 has label 1
        # In practice, labels come from sample, here we test the vote
        labels = np.array([0, 1])  # Point 0 is 0, Point 1 is 1
        vote = compute_majority_vote(labels)
        assert vote == 0  # Tie between [0,1] -> 0

    def test_full_pipeline_with_ties(self):
        """Full k-NN prediction pipeline with ties."""
        # Create sample of 4 points on a line
        # Point 0: dist 0 to itself, 1 to 1, 1 to 2, 2 to 3
        # Point 1: dist 1 to 0, 0 to itself, 1 to 2, 1 to 3
        # etc.
        distances = [
            [0, 1, 1, 2],  # query at 0
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [2, 1, 1, 0],
        ]

        # Select k=3 neighbors for query at point 0
        neighbors = select_k_neighbors(0, [0, 1, 2, 3], distances, 3)
        # Expected: point 0 (dist 0), then 1,2 (dist 1, by index), then 3 (dist 2)
        # So [0, 1, 2]
        np.testing.assert_array_equal(neighbors, [0, 1, 2])

    def test_scenario_with_distance_tie_at_k_boundary(self):
        """Test tie-breaking when k boundary falls at a distance tie."""
        distances = [[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]]

        # k=2: should pick point 0 and point with smallest index among 1,2,3
        neighbors = select_k_neighbors(0, [0, 1, 2, 3], distances, 2)
        np.testing.assert_array_equal(neighbors, [0, 1])

        # k=3: should pick point 0, 1, 2
        neighbors = select_k_neighbors(0, [0, 1, 2, 3], distances, 3)
        np.testing.assert_array_equal(neighbors, [0, 1, 2])


def test_module_docstring() -> None:
    """Verify module docstring references frozen spec."""
    from knn_stability import tie_breaking
    assert "02_DEFINITIONS_SPEC" in tie_breaking.__doc__
    assert "0 ≺ 1" in tie_breaking.__doc__ or "0 \\prec 1" in tie_breaking.__doc__
