# Decision Record: freeze v0.1 definitions

## Date

2026-05-13

## Status

Accepted

## Context

Implementation tasks for finite metrics, k-NN, and stability cannot proceed safely while core mathematical objects remain underspecified.

## Decision

Freeze v0.1 with the following choices:

- training samples are ordered tuples of labeled occurrences;
- duplicate points are allowed;
- conflicting labels at the same point are allowed;
- query points may coincide with training points;
- LOO evaluates at the deleted occurrence itself;
- replace-one ranges over arbitrary labeled points in the finite domain for worst-case definitions;
- labels are binary `{0, 1}`;
- label ties break in favor of `0`;
- consistency discussion uses classical distributional consistency;
- uniform stability takes worst-case suprema over the full allowed perturbation and evaluation domain for each notion.

## Alternatives considered

1. Use multisets instead of ordered tuples.
2. Forbid duplicates and conflicting labels globally.
3. Leave replace-one and LOO conventions deferred until implementation time.

## Consequences

Positive:
- TASK-002 through TASK-006 now have a concrete authority source.
- Tie behavior is auditable in both code and proofs.
- Witness search can reason about duplicate and conflicting-label examples explicitly.

Negative / risks:
- Ordered-tuple semantics are slightly more concrete than some paper-level formulations.
- Favoring label `0` in vote ties is arbitrary and must always be disclosed.

## Required follow-up

- Update implementation tasks to reference the frozen spec as needed.
- Review every later theorem statement against this frozen v0.1 semantics.

