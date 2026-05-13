# TASK-011: Generate figures for witnesses

## Owner

Claude Code

## Goal

Generate clear graph figures from accepted witness JSON.

## Context

Use witness files supplied by Codex or produced by accepted tasks.

## Required work

1. Generate PDF/SVG figures under `outputs/figures/`.
2. Include labels and tie-breaking annotations if needed.
3. Save the command used.

## Do not do

- Do not alter witness data.
- Do not change theorem statements.

## Validation

Run the figure script and pytest.

## Report

Return files changed, output paths, commands, and ambiguities.

