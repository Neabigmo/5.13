"""Placeholder entry point for minimal 1-NN witness search.

The real search is reserved for TASK-007 after definitions and core modules are frozen.
"""

from __future__ import annotations

import argparse


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_vertices", type=int, required=True)
    args = parser.parse_args()
    raise SystemExit(
        "search_minimal_1nn.py is a placeholder until TASK-007; "
        f"received max_vertices={args.max_vertices}."
    )


if __name__ == "__main__":
    main()

