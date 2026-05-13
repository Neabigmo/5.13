# TASK-007: Search minimal 1-NN witnesses

## Owner

Claude Code

## Goal

Enumerate small graph metric examples and produce witness JSON for 1-NN separation candidates.

## Context

Use frozen definitions and implemented modules. Computational witnesses are not proofs.

## Required work

1. Enumerate the specified finite graph search space.
2. Record constraints and assumptions.
3. Save witness JSON under `outputs/witnesses/`.
4. Provide reproducibility command.

## Do not do

- Do not claim minimality as theorem.
- Do not change stability definitions.

## Validation

```powershell
conda run -p E:\anaconda3\envs\pytorch-clean python experiments/search_minimal_1nn.py --max_vertices 4
```

## Report

Return search space, constraints, witnesses, no-solution ranges, output paths, and commands.

