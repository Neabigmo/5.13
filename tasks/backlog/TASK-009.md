# TASK-009: Generate minimality certificate

## Owner

Claude Code

## Goal

Generate computational no-solution tables, reproducibility commands, and output hashes.

## Context

This is computational evidence only.

## Required work

1. Create certificate output files under `outputs/tables/` or `outputs/witnesses/`.
2. Record search ranges and assumptions.
3. Include hashes for generated outputs.

## Do not do

- Do not call the certificate a proof.
- Do not change search constraints without reporting it.

## Validation

Run pytest and the certificate script.

## Report

Return structured report.

