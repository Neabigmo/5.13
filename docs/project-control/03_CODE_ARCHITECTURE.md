# Code Architecture

## Package

Python package: `knn_stability`

Active modules:

- `metrics.py`: finite metric spaces and validation
- `graph_metrics.py`: unweighted connected graph shortest-path metrics
- `tie_breaking.py`: deterministic point and label tie-breaking
- `knn.py`: deterministic k-NN prediction
- `stability.py`: perturbation primitives and stability indicators
- `diagnostic.py`: margin and stability-gap diagnostics
- `enumeration.py`: small finite search utilities
- `witnesses.py`: witness serialization and validation

## Tests

Tests live in `tests/` and mirror the module structure. Perturbation semantics
must be covered before experiments are trusted.

## Experiments

Experiments live in `experiments/`, run deterministically, and save outputs to
`outputs/`.

## Outputs

- Witness JSON: `outputs/witnesses/`
- Tables: `outputs/tables/`
- Figures: `outputs/figures/`
- Experiment summaries: `outputs/experiments/`
- Logs: `outputs/logs/`
