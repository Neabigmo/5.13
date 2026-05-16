"""Tests for stability indicators.

Tests distinguish delete-one, insert-one, replace-one, and LOO stability.
"""

import numpy as np
import pytest

from knn_stability.knn import LabeledSample, predict_knn
from knn_stability.metrics import FiniteMetricSpace
from knn_stability.stability import (
    binary_loss,
    delete_one_sample,
    replace_one_sample,
    insert_one_sample,
    add_one_sample,
    pointwise_delete_one_stability,
    pointwise_replace_one_stability,
    pointwise_insert_one_stability,
    pointwise_add_one_stability,
    pointwise_loo_stability,
    uniform_delete_one_stability,
    uniform_replace_one_stability,
    fixed_sample_max_insert_one_stability,
    uniform_add_one_stability,
    uniform_loo_stability,
)


class TestBinaryLoss:
    def test_correct_prediction_gives_zero_loss(self):
        assert binary_loss(0, 0) == 0
        assert binary_loss(1, 1) == 0

    def test_incorrect_prediction_gives_unit_loss(self):
        assert binary_loss(0, 1) == 1
        assert binary_loss(1, 0) == 1



class TestDeleteOneSample:
    @pytest.fixture
    def line_metric(self):
        return FiniteMetricSpace(
            points=['a', 'b', 'c'],
            distances=[[0.0, 1.0, 2.0], [1.0, 0.0, 1.0], [2.0, 1.0, 0.0]],
        )

    def test_delete_first_occurrence(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1, 2], [0, 1, 0], line_metric)
        deleted = delete_one_sample(sample, 0)
        assert deleted.point_indices == (1, 2)
        assert deleted.labels == (1, 0)

    def test_delete_last_occurrence(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1, 2], [0, 1, 0], line_metric)
        deleted = delete_one_sample(sample, 2)
        assert deleted.point_indices == (0, 1)
        assert deleted.labels == (0, 1)

    def test_delete_middle_occurrence(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1, 2], [0, 1, 0], line_metric)
        deleted = delete_one_sample(sample, 1)
        assert deleted.point_indices == (0, 2)
        assert deleted.labels == (0, 0)

    def test_delete_out_of_bounds_raises(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1], [0, 1], line_metric)
        with pytest.raises(ValueError, match='out of bounds'):
            delete_one_sample(sample, 5)


class TestReplaceOneSample:
    @pytest.fixture
    def line_metric(self):
        return FiniteMetricSpace(
            points=['a', 'b', 'c'],
            distances=[[0.0, 1.0, 2.0], [1.0, 0.0, 1.0], [2.0, 1.0, 0.0]],
        )

    def test_replace_point_only(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1, 2], [0, 1, 0], line_metric)
        replaced = replace_one_sample(sample, 1, new_point_idx=2, new_label=1)
        assert replaced.point_indices == (0, 2, 2)
        assert replaced.labels == (0, 1, 0)

    def test_replace_label_only(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1, 2], [0, 1, 0], line_metric)
        replaced = replace_one_sample(sample, 0, new_point_idx=0, new_label=1)
        assert replaced.point_indices == (0, 1, 2)
        assert replaced.labels == (1, 1, 0)

    def test_replace_both(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1, 2], [0, 1, 0], line_metric)
        replaced = replace_one_sample(sample, 1, new_point_idx=2, new_label=0)
        assert replaced.point_indices == (0, 2, 2)
        assert replaced.labels == (0, 0, 0)

    def test_replace_invalid_point_raises(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1], [0, 1], line_metric)
        with pytest.raises(ValueError, match='out of bounds'):
            replace_one_sample(sample, 0, new_point_idx=10, new_label=0)

    def test_replace_invalid_label_raises(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1], [0, 1], line_metric)
        with pytest.raises(ValueError, match='new_label must be'):
            replace_one_sample(sample, 0, new_point_idx=0, new_label=2)


class TestInsertOneSample:
    @pytest.fixture
    def line_metric(self):
        return FiniteMetricSpace(
            points=['a', 'b', 'c'],
            distances=[[0.0, 1.0, 2.0], [1.0, 0.0, 1.0], [2.0, 1.0, 0.0]],
        )

    def test_insert_first_changes_order(self, line_metric):
        sample = LabeledSample.from_arrays([1, 2], [1, 0], line_metric)
        inserted = insert_one_sample(sample, insert_position=0, new_point_idx=0, new_label=0)
        assert inserted.point_indices == (0, 1, 2)
        assert inserted.labels == (0, 1, 0)

    def test_insert_last_matches_append(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1], [0, 1], line_metric)
        inserted = insert_one_sample(sample, insert_position=sample.n, new_point_idx=2, new_label=0)
        added = add_one_sample(sample, new_point_idx=2, new_label=0)
        assert inserted.point_indices == added.point_indices
        assert inserted.labels == added.labels
        assert len(inserted) == 3

    def test_insert_duplicate_allowed(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1], [0, 1], line_metric)
        inserted = insert_one_sample(sample, insert_position=1, new_point_idx=0, new_label=1)
        assert inserted.point_indices == (0, 0, 1)
        assert inserted.labels == (0, 1, 1)

    def test_insert_position_valid_range(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1], [0, 1], line_metric)
        with pytest.raises(ValueError, match='out of bounds'):
            insert_one_sample(sample, insert_position=-1, new_point_idx=0, new_label=0)
        with pytest.raises(ValueError, match='out of bounds'):
            insert_one_sample(sample, insert_position=3, new_point_idx=0, new_label=0)


class TestPointwiseDeleteOneStability:
    @pytest.fixture
    def line_metric(self):
        return FiniteMetricSpace(
            points=['a', 'b', 'c'],
            distances=[[0.0, 1.0, 2.0], [1.0, 0.0, 1.0], [2.0, 1.0, 0.0]],
        )

    def test_no_stability_change(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1, 2], [0, 1, 0], line_metric)
        indicator = pointwise_delete_one_stability(
            sample, delete_index=0, query_point_idx=2, query_label=0, k=1
        )
        assert indicator == 0

    def test_stability_change(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1, 2], [0, 1, 1], line_metric)
        indicator = pointwise_delete_one_stability(
            sample, delete_index=0, query_point_idx=0, query_label=0, k=1
        )
        assert indicator == 1

    def test_k_prime_adjustment(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1, 2], [0, 1, 0], line_metric)
        indicator = pointwise_delete_one_stability(
            sample, delete_index=0, query_point_idx=0, query_label=0, k=3
        )
        assert indicator == 0


class TestPointwiseReplaceOneStability:
    @pytest.fixture
    def line_metric(self):
        return FiniteMetricSpace(
            points=['a', 'b', 'c'],
            distances=[[0.0, 1.0, 2.0], [1.0, 0.0, 1.0], [2.0, 1.0, 0.0]],
        )

    def test_replace_same_no_change(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1, 2], [0, 1, 0], line_metric)
        indicator = pointwise_replace_one_stability(
            sample, replace_index=1, new_point_idx=1, new_label=1,
            query_point_idx=0, query_label=0, k=1
        )
        assert indicator == 0

    def test_replace_one_can_differ_from_delete_one(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1, 2], [0, 1, 0], line_metric)
        delete_indicator = pointwise_delete_one_stability(
            sample, delete_index=0, query_point_idx=2, query_label=0, k=1
        )
        replace_indicator = pointwise_replace_one_stability(
            sample,
            replace_index=0,
            new_point_idx=2,
            new_label=1,
            query_point_idx=2,
            query_label=0,
            k=1,
        )
        assert delete_indicator == 0
        assert replace_indicator == 1


class TestPointwiseInsertOneStability:
    @pytest.fixture
    def line_metric(self):
        return FiniteMetricSpace(
            points=['a', 'b', 'c'],
            distances=[[0.0, 1.0, 2.0], [1.0, 0.0, 1.0], [2.0, 1.0, 0.0]],
        )

    def test_insert_same_point(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1, 2], [0, 1, 0], line_metric)
        indicator = pointwise_insert_one_stability(
            sample, insert_position=sample.n, new_point_idx=0, new_label=0,
            query_point_idx=0, query_label=0, k=1
        )
        assert indicator == 0

    def test_replace_equals_delete_then_insert_at_deleted_position(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1, 2], [0, 1, 0], line_metric)
        delete_index = 1
        replacement_point = 2
        replacement_label = 0
        query_point_idx = 0
        query_label = 0

        deleted = delete_one_sample(sample, delete_index)
        rebuilt = insert_one_sample(
            deleted,
            insert_position=delete_index,
            new_point_idx=replacement_point,
            new_label=replacement_label,
        )
        replaced = replace_one_sample(
            sample,
            replace_index=delete_index,
            new_point_idx=replacement_point,
            new_label=replacement_label,
        )

        assert rebuilt.point_indices == replaced.point_indices
        assert rebuilt.labels == replaced.labels

        replace_indicator = pointwise_replace_one_stability(
            sample,
            replace_index=delete_index,
            new_point_idx=replacement_point,
            new_label=replacement_label,
            query_point_idx=query_point_idx,
            query_label=query_label,
            k=1,
        )
        insert_indicator = pointwise_insert_one_stability(
            deleted,
            insert_position=delete_index,
            new_point_idx=replacement_point,
            new_label=replacement_label,
            query_point_idx=query_point_idx,
            query_label=query_label,
            k=1,
        )
        pred_sample = predict_knn(sample, query_point_idx, 1)
        pred_deleted = predict_knn(deleted, query_point_idx, 1)
        delete_loss_gap = abs(binary_loss(pred_sample, query_label) - binary_loss(pred_deleted, query_label))
        assert replace_indicator <= delete_loss_gap + insert_indicator


class TestCompatibilityAddOneWrapper:
    @pytest.fixture
    def line_metric(self):
        return FiniteMetricSpace(
            points=['a', 'b', 'c'],
            distances=[[0.0, 1.0, 2.0], [1.0, 0.0, 1.0], [2.0, 1.0, 0.0]],
        )

    def test_add_same_point(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1, 2], [0, 1, 0], line_metric)
        indicator = pointwise_add_one_stability(
            sample, new_point_idx=0, new_label=0,
            query_point_idx=0, query_label=0, k=1
        )
        assert indicator == 0


class TestPointwiseLooStability:
    @pytest.fixture
    def line_metric(self):
        return FiniteMetricSpace(
            points=['a', 'b', 'c'],
            distances=[[0.0, 1.0, 2.0], [1.0, 0.0, 1.0], [2.0, 1.0, 0.0]],
        )

    def test_loo_evaluates_at_deleted(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1, 2], [0, 1, 0], line_metric)
        indicator = pointwise_loo_stability(sample, delete_index=0, k=1)
        assert indicator == 1

    def test_loo_self_removed(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1, 2], [0, 1, 0], line_metric)
        indicator = pointwise_loo_stability(sample, delete_index=1, k=1)
        assert indicator == 1

    def test_loo_duplicate_points(self, line_metric):
        sample = LabeledSample.from_arrays([0, 0, 1], [0, 1, 0], line_metric)
        indicator1 = pointwise_loo_stability(sample, delete_index=0, k=1)
        assert indicator1 == 1

    def test_loo_can_differ_from_delete_one(self, line_metric):
        sample = LabeledSample.from_arrays([0, 1, 2], [0, 1, 0], line_metric)
        delete_indicator = pointwise_delete_one_stability(
            sample, delete_index=0, query_point_idx=2, query_label=0, k=1
        )
        loo_indicator = pointwise_loo_stability(sample, delete_index=0, k=1)
        assert delete_indicator == 0
        assert loo_indicator == 1


class TestUniformStabilityHelpers:
    @pytest.fixture
    def small_metric(self):
        return FiniteMetricSpace(
            points=['a', 'b'],
            distances=[[0.0, 1.0], [1.0, 0.0]],
        )

    def test_uniform_delete_one(self, small_metric):
        sample = LabeledSample.from_arrays([0, 1], [0, 1], small_metric)
        max_ind, del_idx, query = uniform_delete_one_stability(sample, k=1)
        assert isinstance(max_ind, (int, np.integer))
        assert 0 <= del_idx < sample.n
        assert isinstance(query, tuple) and len(query) == 2

    def test_uniform_replace_one(self, small_metric):
        sample = LabeledSample.from_arrays([0, 1], [0, 1], small_metric)
        max_ind, pt, lbl, query = uniform_replace_one_stability(sample, 0, k=1)
        assert isinstance(max_ind, (int, np.integer))
        assert 0 <= pt < sample.metric.n
        assert lbl in (0, 1)

    def test_uniform_add_one(self, small_metric):
        sample = LabeledSample.from_arrays([0], [0], small_metric)
        max_ind, query = uniform_add_one_stability(sample, 1, 1, k=1)
        assert isinstance(max_ind, (int, np.integer))
        assert isinstance(query, tuple) and len(query) == 2

    def test_fixed_sample_max_insert_one(self, small_metric):
        sample = LabeledSample.from_arrays([0], [0], small_metric)
        max_ind, insert_pos, pt, lbl, query = fixed_sample_max_insert_one_stability(sample, k=1)
        assert isinstance(max_ind, (int, np.integer))
        assert 0 <= insert_pos <= sample.n
        assert 0 <= pt < sample.metric.n
        assert lbl in (0, 1)
        assert isinstance(query, tuple) and len(query) == 2

    def test_uniform_loo(self, small_metric):
        sample = LabeledSample.from_arrays([0, 1], [0, 1], small_metric)
        max_ind, del_idx = uniform_loo_stability(sample, k=1)
        assert isinstance(max_ind, (int, np.integer))
        assert 0 <= del_idx < sample.n


class TestComputationalLimitations:
    @pytest.fixture
    def small_metric(self):
        return FiniteMetricSpace(
            points=['a', 'b', 'c'],
            distances=[[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]],
        )

    def test_replace_complexity(self, small_metric):
        sample = LabeledSample.from_arrays([0, 1], [0, 1], small_metric)
        max_ind, _, _, _ = uniform_replace_one_stability(sample, 0, k=1)
        assert max_ind in (0, 1)

    def test_loo_tractable(self, small_metric):
        sample = LabeledSample.from_arrays([0, 1, 2], [0, 1, 0], small_metric)
        loo_max, _ = uniform_loo_stability(sample, k=1)
        del_max, _, _ = uniform_delete_one_stability(sample, k=1)
        assert loo_max in (0, 1)
        assert del_max in (0, 1)


class TestIntegration:
    def test_stability_with_graph_metric(self):
        from knn_stability.graph_metrics import adjacency_to_graph_metric
        adjacency = {0: {1, 2}, 1: {0, 2}, 2: {0, 1}}
        metric = adjacency_to_graph_metric(adjacency)
        sample = LabeledSample.from_arrays([0, 1, 2], [0, 1, 1], metric)
        indicator = pointwise_delete_one_stability(sample, 0, 0, 0, k=2)
        assert indicator in (0, 1)
        loo_ind = pointwise_loo_stability(sample, 0, k=2)
        assert loo_ind in (0, 1)

    def test_stability_with_path_graph(self):
        from knn_stability.graph_metrics import adjacency_to_graph_metric
        adjacency = {0: {1}, 1: {0, 2}, 2: {1, 3}, 3: {2}}
        metric = adjacency_to_graph_metric(adjacency)
        sample = LabeledSample.from_arrays([0, 1, 2, 3], [0, 0, 1, 1], metric)
        indicator = pointwise_replace_one_stability(
            sample, 1, new_point_idx=3, new_label=0,
            query_point_idx=0, query_label=0, k=3
        )
        assert indicator in (0, 1)


def test_module_docstring() -> None:
    from knn_stability import stability
    assert '02_DEFINITIONS_SPEC' in stability.__doc__
    assert 'tractable' in stability.__doc__.lower() or 'complexity' in stability.__doc__.lower()
    assert 'fixed-sample brute-force maxima' in stability.__doc__.lower()
