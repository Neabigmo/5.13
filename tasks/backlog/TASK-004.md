# TASK-004: Implement deterministic tie-breaking

## Owner

Claude Code

## Goal

Implement deterministic point and label tie-breaking exactly as frozen by Codex.

## Context

Use only the frozen tie-breaking section of `docs/project-control/02_DEFINITIONS_SPEC.md`.

## Required work

1. Implement stable ordering helpers.
2. Implement label tie-breaking helper.
3. Add tests covering distance ties and label vote ties.

## Do not do

- Do not invent or alter tie-breaking policy.
- Do not implement k-NN prediction beyond helpers needed for tests.

## Validation

```powershell
conda run -p E:\anaconda3\envs\pytorch-clean python -m pytest
```

## Report

Return structured report.

