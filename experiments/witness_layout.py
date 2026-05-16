"""Small layout helpers for witness visualizations and tests."""

from __future__ import annotations

import math


def layout_by_degree(adjacency):
    """Place a high-degree vertex in the center and remaining vertices on a circle."""
    vertices = sorted(int(k) for k in adjacency.keys())
    positions = {}

    center = max(vertices, key=lambda v: len(adjacency[str(v)]))
    positions[center] = (0, 0)

    leaves = [v for v in vertices if v != center]
    if not leaves:
        return positions, center

    for i, leaf in enumerate(sorted(leaves)):
        angle = 2 * math.pi * i / len(leaves)
        positions[leaf] = (math.cos(angle), math.sin(angle))

    return positions, center
