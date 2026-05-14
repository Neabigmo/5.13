"""Deterministic finite search for odd-k gadget candidates.

This script is exploratory computational evidence for TASK-012. It searches
small graph metrics and ordered binary samples for fixed-sample separations
between LOO and replace-one stability maxima. It does not prove any statement
for all k or for all metric spaces.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from knn_stability.enumeration import enumerate_connected_graphs  # noqa: E402
from knn_stability.graph_metrics import adjacency_to_graph_metric  # noqa: E402
from knn_stability.knn import LabeledSample  # noqa: E402
from knn_stability.stability import (  # noqa: E402
    uniform_loo_stability,
    uniform_replace_one_stability,
)


def sample_lengths_for_k(k: int, modes: Iterable[str]) -> list[int]:
    """Translate length-mode names into deterministic sample lengths."""
    lengths: list[int] = []
    for mode in modes:
        if mode == "equal_k":
            candidate = k
        elif mode == "k_plus_one":
            candidate = k + 1
        else:
            raise ValueError(f"Unknown length mode: {mode}")
        if candidate not in lengths:
            lengths.append(candidate)
    return lengths


def compute_fixed_sample_metrics(sample: LabeledSample, k: int) -> dict[str, Any]:
    """Compute fixed-sample LOO and replace-one maxima for one sample."""
    loo_max, loo_index = uniform_loo_stability(sample, k)

    replace_max = 0
    replace_index = 0
    replacement_point = 0
    replacement_label = 0
    replace_query_point = 0
    replace_query_label = 0

    for candidate_index in range(sample.n):
        (
            candidate_max,
            candidate_point,
            candidate_label,
            candidate_query,
        ) = uniform_replace_one_stability(sample, candidate_index, k)
        if candidate_max > replace_max:
            replace_max = candidate_max
            replace_index = candidate_index
            replacement_point = candidate_point
            replacement_label = candidate_label
            replace_query_point, replace_query_label = candidate_query

    return {
        "loo_max": loo_max,
        "loo_witness_index": loo_index,
        "replace_max": replace_max,
        "replace_witness_index": replace_index,
        "replace_witness_replacement_point": replacement_point,
        "replace_witness_replacement_label": replacement_label,
        "replace_witness_query_point": replace_query_point,
        "replace_witness_query_label": replace_query_label,
        "separation_gap": abs(loo_max - replace_max),
    }


def candidate_from_sample(
    *,
    k: int,
    adjacency: dict[int, set[int]],
    sample: LabeledSample,
    metrics: dict[str, Any],
) -> dict[str, Any]:
    """Build a JSON-serializable candidate record."""
    adjacency_list = {
        vertex: sorted(neighbors) for vertex, neighbors in adjacency.items()
    }
    return {
        "k": k,
        "num_vertices": sample.metric.n,
        "num_edges": sum(len(neighbors) for neighbors in adjacency.values()) // 2,
        "adjacency_list": adjacency_list,
        "sample_length": sample.n,
        "sample_order": list(sample.point_indices),
        "labels": list(sample.labels),
        **metrics,
        "status": "candidate_pattern_not_a_proof",
    }


def search_k_gadgets(
    *,
    k_values: Iterable[int],
    min_vertices: int,
    max_vertices: int,
    length_modes: Iterable[str],
    max_candidates_per_k: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Search a finite graph/sample space for odd-k candidate patterns."""
    k_list = list(k_values)
    modes = list(length_modes)
    candidates: list[dict[str, Any]] = []
    stats: dict[str, Any] = {
        "graphs_evaluated": 0,
        "samples_evaluated_by_k": {str(k): 0 for k in k_list},
        "candidates_by_k": {str(k): 0 for k in k_list},
        "stopped_by_candidate_limit": {str(k): False for k in k_list},
    }

    for num_vertices in range(min_vertices, max_vertices + 1):
        labeled_points = tuple(
            (point_idx, label)
            for point_idx in range(num_vertices)
            for label in (0, 1)
        )

        for adjacency in enumerate_connected_graphs(num_vertices):
            stats["graphs_evaluated"] += 1
            metric = adjacency_to_graph_metric(adjacency)

            for k in k_list:
                if stats["candidates_by_k"][str(k)] >= max_candidates_per_k:
                    stats["stopped_by_candidate_limit"][str(k)] = True
                    continue

                for sample_length in sample_lengths_for_k(k, modes):
                    if sample_length < k:
                        continue

                    for labeled_sample in itertools.product(
                        labeled_points, repeat=sample_length
                    ):
                        stats["samples_evaluated_by_k"][str(k)] += 1
                        sample = LabeledSample(
                            metric=metric,
                            point_indices=tuple(point for point, _ in labeled_sample),
                            labels=tuple(label for _, label in labeled_sample),
                        )
                        metrics = compute_fixed_sample_metrics(sample, k)
                        if metrics["loo_max"] == metrics["replace_max"]:
                            continue

                        candidates.append(
                            candidate_from_sample(
                                k=k,
                                adjacency=adjacency,
                                sample=sample,
                                metrics=metrics,
                            )
                        )
                        stats["candidates_by_k"][str(k)] += 1
                        if (
                            stats["candidates_by_k"][str(k)]
                            >= max_candidates_per_k
                        ):
                            stats["stopped_by_candidate_limit"][str(k)] = True
                            break

                    if stats["candidates_by_k"][str(k)] >= max_candidates_per_k:
                        break

    return candidates, stats


def build_metadata(
    *,
    k_values: Iterable[int],
    min_vertices: int,
    max_vertices: int,
    length_modes: Iterable[str],
    max_candidates_per_k: int,
    candidates: list[dict[str, Any]],
    stats: dict[str, Any],
) -> dict[str, Any]:
    """Build metadata documenting TASK-012 search restrictions."""
    k_list = list(k_values)
    modes = list(length_modes)
    return {
        "task": "TASK-012",
        "description": "Deterministic finite search for odd-k LOO vs replace-one gadget candidates",
        "status": "computational_evidence_only",
        "not_a_proof": True,
        "k_values": k_list,
        "search_space": {
            "graph_type": "connected simple undirected labeled graphs",
            "vertex_range": f"{min_vertices} to {max_vertices}",
            "sample_length_modes": modes,
            "resolved_sample_lengths_by_k": {
                str(k): sample_lengths_for_k(k, modes) for k in k_list
            },
            "sample_generation": "all ordered tuples from X x {0,1} with repetition",
            "duplicates_allowed": True,
            "conflicting_labels_allowed": True,
            "tie_breaking": "distance then sample index; label ties favor 0",
        },
        "candidate_limit": {
            "max_candidates_per_k": max_candidates_per_k,
            "limits_are_search_controls_not_mathematical_claims": True,
        },
        "reproducibility_command": (
            "E:\\anaconda3\\envs\\pytorch-clean\\python.exe "
            "experiments\\search_k_gadgets.py "
            f"--k_values {' '.join(str(k) for k in k_list)} "
            f"--min_vertices {min_vertices} "
            f"--max_vertices {max_vertices} "
            f"--length_modes {' '.join(modes)} "
            f"--max_candidates_per_k {max_candidates_per_k}"
        ),
        "stability_target": {
            "loo": "fixed-sample maximum over delete indices",
            "replace_one": "fixed-sample maximum over replacement indices, replacements in X x {0,1}, and evaluation labels",
        },
        "constraints": [
            "candidate records are not theorem statements",
            "the search is deterministic and exhaustive only inside the stated finite search space",
            "duplicate sample occurrences are intentionally included",
            "conflicting labels at the same metric point are intentionally included",
            "do not generalize these candidates to all odd k without a separate proof",
        ],
        "search_stats": stats,
        "num_candidates_found": len(candidates),
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Search deterministic finite odd-k gadget candidates."
    )
    parser.add_argument(
        "--k_values",
        type=int,
        nargs="+",
        default=[3, 5, 7],
        help="Odd k values to search.",
    )
    parser.add_argument(
        "--min_vertices",
        type=int,
        default=2,
        help="Minimum connected graph size to search.",
    )
    parser.add_argument(
        "--max_vertices",
        type=int,
        default=2,
        help="Maximum connected graph size to search.",
    )
    parser.add_argument(
        "--length_modes",
        choices=["equal_k", "k_plus_one"],
        nargs="+",
        default=["equal_k"],
        help="Sample length modes to enumerate for each k.",
    )
    parser.add_argument(
        "--max_candidates_per_k",
        type=int,
        default=10,
        help="Stop recording after this many candidates per k.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "outputs" / "witnesses" / "k_gadget_candidates.json",
        help="Output JSON path.",
    )
    return parser.parse_args()


def main() -> int:
    """Run the TASK-012 finite search."""
    args = parse_args()
    if args.min_vertices < 1:
        raise SystemExit("--min_vertices must be at least 1.")
    if args.max_vertices < args.min_vertices:
        raise SystemExit("--max_vertices must be at least --min_vertices.")
    if args.max_candidates_per_k < 1:
        raise SystemExit("--max_candidates_per_k must be at least 1.")
    for k in args.k_values:
        if k < 1 or k % 2 == 0:
            raise SystemExit("--k_values must contain positive odd integers.")

    candidates, stats = search_k_gadgets(
        k_values=args.k_values,
        min_vertices=args.min_vertices,
        max_vertices=args.max_vertices,
        length_modes=args.length_modes,
        max_candidates_per_k=args.max_candidates_per_k,
    )
    metadata = build_metadata(
        k_values=args.k_values,
        min_vertices=args.min_vertices,
        max_vertices=args.max_vertices,
        length_modes=args.length_modes,
        max_candidates_per_k=args.max_candidates_per_k,
        candidates=candidates,
        stats=stats,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps({"metadata": metadata, "candidates": candidates}, indent=2),
        encoding="utf-8",
    )

    print(f"Wrote {len(candidates)} candidate records to {args.output}")
    print(f"Candidates by k: {stats['candidates_by_k']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
