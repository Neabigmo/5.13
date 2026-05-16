# Stability Hierarchy Proof Audit

Status: active audit scaffold

This file tracks which hierarchy claims are backed by explicit theorem,
proposition, or counterexample references in the active manuscript.

## Proven / supported entries

- `uniform delete-one + uniform insert-one => uniform replace-one`
  - Source: [paper/sections/04_uniform_calculus.tex](/H:/2026try/5.13/paper/sections/04_uniform_calculus.tex)
  - Reference key: `prop:4.1`

- `LOO does not imply replace-one`
  - Source: [paper/sections/06_minimal_1nn.tex](/H:/2026try/5.13/paper/sections/06_minimal_1nn.tex)
  - Supported further by: [paper/sections/07_odd_k_separation.tex](/H:/2026try/5.13/paper/sections/07_odd_k_separation.tex), [paper/sections/08_even_k_separation.tex](/H:/2026try/5.13/paper/sections/08_even_k_separation.tex)

- `pointwise delete-one and pointwise insert-one are incomparable`
  - Source: [paper/sections/B_hierarchy_counterexamples.tex](/H:/2026try/5.13/paper/sections/B_hierarchy_counterexamples.tex)
  - Requirement: keep proposition/counterexample labels explicit in manuscript text and hierarchy table

## Must not appear without explicit support

- Any row whose only justification is "standard"
- Any row whose only justification is "different evaluation quantification"
- Any claim about full uniform comparability of delete-one and insert-one unless
  the manuscript includes a proof or explicit open-problem label

## Audit actions

- The hierarchy table in the manuscript must map each retained row to an
  explicit theorem, proposition, or counterexample label.
- Open problems must be labeled as open problems, not as implications or
  non-implications.
