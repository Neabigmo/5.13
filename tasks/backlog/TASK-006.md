# TASK-006: Implement stability indicators

## Owner

Claude Code

## Goal

Implement delete-one, replace-one, LOO, and uniform brute-force stability helpers.

## Context

This task must not start until Codex freezes `docs/project-control/02_DEFINITIONS_SPEC.md`.

## Required work

1. Implement indicators matching the frozen quantifiers and evaluation points.
2. Add tests that distinguish delete-one, replace-one, and LOO.
3. Document any computational limitations.

## Do not do

- Do not alter definitions.
- Do not treat pointwise results as uniform results.

## Validation

```powershell
conda run -p E:\anaconda3\envs\pytorch-clean python -m pytest
```

## Report

Return structured report.

