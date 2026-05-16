# Codex task cards

Use these as small, reviewable tasks. Each task should be one branch or one clean commit.

---

## TASK-ML-001: definition synchronization

Goal: make paper, docs, and code agree on delete/insert/replace/LOO.

Steps:

1. Update `docs/project-control/02_DEFINITIONS_SPEC.md` from append-only add-one to insertion-position insert-one.
2. Add decision record `docs/decision-records/DR-001-insert-one.md`.
3. Update paper definitions.
4. Search for `add-one`, `add_one`, `S \oplus z`, and `append`.

Acceptance:

- All paper-level statements use insert-one.
- Append-only add-one is either removed or explicitly marked non-paper helper.
- Tests still pass or are updated in TASK-ML-002.

---

## TASK-ML-002: perturbation primitive refactor

Goal: implement insertion at arbitrary sample position.

Steps:

1. Implement `insert_one_sample`.
2. Implement `pointwise_insert_one_stability`.
3. Implement fixed-sample max insert stability over all positions.
4. Update replace-one decomposition tests.

Required tests:

- `test_insert_first_changes_order`
- `test_insert_last_matches_append`
- `test_replace_equals_delete_then_insert_at_deleted_position`
- `test_insert_position_valid_range`

---

## TASK-ML-003: theorem witness tests

Goal: verify all analytic constructions.

Steps:

1. Add witness constructors for k=1, odd k, even k.
2. Add tests for k=1..15.
3. Save witness verification table.

Acceptance:

- Every theoretical witness has LOO_max=0 and REP_max=1.
- Odd margins are -1 -> +1.
- Even margins are 0 -> +2.

---

## TASK-ML-004: hierarchy table proof audit

Goal: only keep relationships that are proved.

Steps:

1. Create `docs/proof-audit/stability_hierarchy.md`.
2. For every table row, attach theorem/proposition/counterexample.
3. Remove or demote rows without explicit evidence.
4. Add appendix counterexamples where needed.

Acceptance:

- No row says `standard` or `different evaluation quantification` as its only reference.

---

## TASK-ML-005: experiment runner

Goal: create a reproducible experiment pipeline.

Steps:

1. Add `experiments/run_all.py`.
2. Add YAML config.
3. Add raw output writing and manifest checksums.
4. Add summary table generation.
5. Add figure generation.

Acceptance:

- One command rebuilds all experiment outputs.
- Raw data and summaries are separate.
- Manifest includes git hash, package versions, seed, and file checksums.

---

## TASK-ML-006: synthetic graph experiments

Goal: implement Experiment C.

Steps:

1. Generate connected ER graphs.
2. Implement controlled duplicate/conflict/noise sampler.
3. Run factorial grid.
4. Compute Wilson intervals.
5. Generate heatmap and tables.

Acceptance:

- At least 200 trials per main configuration.
- No contradictory trend statements remain.

---

## TASK-ML-007: tabular experiments

Goal: implement Experiment D.

Steps:

1. Load sklearn Iris, Wine, Breast Cancer, Digits.
2. Standardize features.
3. Run all one-vs-rest binary conversions.
4. Run subsampling grid.
5. Report strict_gap, LOO_max, REP_max, vulnerable-query rate.

Acceptance:

- k=1 vulnerable rate is interpreted as expected, not surprising.
- Tables include confidence intervals.

---

## TASK-ML-008: diagnostic theorem and experiment

Goal: formalize and test the margin diagnostic.

Steps:

1. Add lemma for odd k: `exists_replace_flip iff |M| <= 2`.
2. Prove it in the paper.
3. Implement diagnostic precision/recall test.
4. Report even-k behavior separately.

Acceptance:

- Odd-k precision and recall are exactly 1 in code tests.
- Even-k is not overstated.

---

## TASK-ML-009: figure rebuild

Goal: replace poster-like figures with journal figures.

Steps:

1. Create Figure 1-6 from `04_FIGURE_DESIGN_BRIEF.md`.
2. Use vector outputs.
3. Remove internal figure numbers.
4. Place figures in source near first reference.

Acceptance:

- No figure appears after references unless appendix.
- Text readable at single-column width.

---

## TASK-ML-010: reference audit and BibTeX

Goal: verify every reference and expand related work.

Steps:

1. Verify all current references.
2. Add selected references from `03_REFERENCE_AUDIT_AND_BIBLIOGRAPHY.md`.
3. Remove any unused references.
4. Make reference style consistent with Springer template.

Acceptance:

- No fabricated or unverifiable references.
- Every citation supports the sentence containing it.

---

## TASK-ML-011: Springer submission package

Goal: compile a clean submission package.

Steps:

1. Download/verify latest Springer Nature template.
2. Port manuscript into `submit/manuscript/`.
3. Fill declarations and cover letter.
4. Compile from clean directory.
5. Zip source and supplementary materials.

Acceptance:

- `submit/` contains manuscript PDF/source, figures, tables, supplement, cover letter, declarations, and checklist.
