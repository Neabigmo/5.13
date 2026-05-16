# Computational Minimality Certificate

This document is computational evidence only. It is not a proof.

## Observed Minimal Vertex Counts

- TASK-007 separation witnesses: `2`
- TASK-008 tie-free witnesses: `2`

## Observed No-Solution Vertex Counts

- TASK-007: `[1]`
- TASK-008: `[1]`

## Output Hashes

- `TASK-007`: `288af808faf96d9354f97b8071fc3f5e10f71f9339613e3bc13a0f4ab34e0f22`
- `TASK-008`: `67273575c8744b0086a6077feff86bb1ec5825e3802a648a0f2e31afa860870c`

## Reproducibility Commands

- `conda run -p E:\anaconda3\envs\pytorch-clean python experiments/search_minimal_1nn.py --max_vertices 4`
- `E:\anaconda3\envs\pytorch-clean\python.exe experiments/search_tie_free.py --input outputs/witnesses/1nn_separation_witnesses.json --output outputs/witnesses/1nn_tie_free_witnesses.json`
- `conda run -p E:\anaconda3\envs\pytorch-clean python experiments/certify_minimality.py`
