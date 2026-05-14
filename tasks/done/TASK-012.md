# TASK-012: Implement k-gadget search

## Owner

Claude Code

## Goal

Search or verify k-NN gadget candidates for k=3,5,7.

## Context

Use accepted 1-NN witness logic and frozen definitions.
This task is exploratory computational evidence only.

Use deterministic finite searches only. It is acceptable to restrict the
search space, but every restriction must be written into the output metadata.
Duplicate sample occurrences and conflicting labels are allowed by the frozen
definitions and may be used in candidate gadgets.

## Required work

1. Implement deterministic search or verification for k=3,5,7.
2. Save outputs with parameters and seeds if any.
3. Report candidate patterns without theorem claims.
4. Include a reproducibility command.

## Do not do

- Do not generalize to all k in prose.
- Do not call candidates proofs.
- Do not silently exclude duplicate sample occurrences.

## Validation

Run pytest and the relevant experiment.

## Report

Return structured report.
