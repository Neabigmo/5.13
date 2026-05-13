# Code Architecture

## Package

Python package: `knn_stability`.

Initial modules:

- `metrics.py`: finite metric spaces and validation.
- `graph_metrics.py`: unweighted connected graph shortest-path metrics.
- `tie_breaking.py`: deterministic point and label tie-breaking.
- `knn.py`: deterministic k-NN prediction.
- `stability.py`: stability indicators after definitions are frozen.
- `enumeration.py`: small finite search utilities.
- `witnesses.py`: witness serialization and validation.

## Tests

Tests live in `tests/` and mirror the module structure. Tests should cover edge cases before large experiments are trusted.

## Experiments

Experiments live in `experiments/`, use deterministic parameters, and save outputs to `outputs/`.

## Outputs

- Witness JSON: `outputs/witnesses/`.
- Tables: `outputs/tables/`.
- Figures: `outputs/figures/`.
- Logs: `outputs/logs/`, not committed.

