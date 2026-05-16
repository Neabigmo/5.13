# Codex master revision plan for the Machine Learning submission

Project: deterministic k-NN stability and the LOO / replace-one gap  
Target journal: *Machine Learning* (Springer)  
Primary working title: **Leave-One-Out Stability Does Not Certify Replacement Robustness in k-Nearest Neighbors**  
Repository assumed from connected GitHub search: `Neabigmo/5.13`  
Uploaded draft reviewed: `main.pdf`, 19 pages, dated 2026-05-15.

This document is written as an executable plan for Codex. Codex should treat it as the top-level control file, split tasks into small commits, and keep a paper-quality standard throughout.

---

## 0. Immediate verdict

The paper is promising and can be aimed at *Machine Learning*, but it is not ready to submit in its current state. The current draft has a clean central idea: LOO is a coupled deletion diagnostic, whereas replace-one robustness is an adversarial replacement notion evaluated at arbitrary queries. The theoretical spine is now clearer than earlier drafts, but the manuscript still needs:

1. a strict code-paper consistency pass;
2. a full proof/reference/numbering audit;
3. a rebuilt experimental section with reproducible tables and confidence intervals;
4. figure redesign into journal-style vector diagrams;
5. a Springer Nature/Machine Learning submission package.

Codex should not weaken the target. The correct approach is to make the claim narrower, cleaner, and more defensible.

---

## 1. Critical issue found by comparing paper and repository

### 1.1 Insert-one in the paper vs append-only add-one in the repository

The current PDF defines insert-one as insertion at any position `j` and uses this in the replace-one decomposition:

```text
S^{i <- z} = (S^{-i}) \oplus_i z.
```

This matters because the sample order is semantically relevant for deterministic tie-breaking. In contrast, the repository's frozen spec and code still implement `add-one` as **append at the end**:

```text
S \oplus z = append z at the end.
```

The code-level `add_one_sample` also appends only. This is not a harmless naming difference. It invalidates any code experiment claiming to test the paper's insert-one calculus. Codex must fix this first.

Required change:

- Rename paper-level notion consistently to `insert-one`, not `add-one`.
- In code, implement:

```python
def insert_one_sample(sample, insert_position, new_point_idx, new_label):
    # 0-based position in code, allowed 0 <= insert_position <= sample.n
```

- Replace `pointwise_add_one_stability` with `pointwise_insert_one_stability` that enumerates insertion position.
- Replace `uniform_add_one_stability` with `fixed_sample_max_insert_one_stability` or similar.
- Keep `add_one_sample` only as a deprecated wrapper if needed, clearly marked as append-only and not used in the paper.
- Add tests proving:
  - insertion at the beginning changes tie-breaking order;
  - insertion at the old deleted index reconstructs replace-one after delete-one;
  - append-only insertion is insufficient for Proposition 4.2.

Acceptance criterion: `pytest` must include a test named `test_replace_equals_delete_then_insert_at_same_position`.

---

## 2. Recommended final narrative

The paper should not be framed as a broad theory of all local learning rules. The strongest and safest story is:

> Leave-one-out evaluation controls a very specific coupled perturbation: delete the evaluated training occurrence and evaluate at that same occurrence. Replacement robustness asks a different question: after replacing one training occurrence, can the prediction change at an arbitrary query? For deterministic k-NN these notions separate sharply, and the separation is exactly explained by a signed top-k vote margin.

The tone should be precise, restrained, and theorem-driven. Avoid sounding like a blog post or a manifesto.

### 2.1 What the paper should claim

Use this hierarchy of claims:

1. **Definition-level contribution**: delete-one, insert-one, replace-one, and LOO are different perturbation/evaluation conventions.
2. **Algebraic contribution**: replace-one decomposes into delete-one followed by insert-one; LOO cannot be substituted because its evaluation point is not free.
3. **k-NN mechanism**: deterministic k-NN prediction changes exactly when the signed top-k margin crosses the decision threshold.
4. **Finite witness contribution**: for every odd k and for even k under deterministic tie-breaking, there exist finite metric samples with zero LOO indicators but a replace-one flip.
5. **Empirical diagnostic contribution**: the margin distribution identifies vulnerable queries and shows the mechanism appears beyond hand-crafted witnesses.

### 2.2 What the paper should not overclaim

Do not claim:

- that LOO is useless;
- that k-NN is generally unstable in distributional/asymptotic risk;
- that experiments prove the theorem;
- that the diagnostic is universally necessary/sufficient for all perturbation types and all k;
- that the local-vote-rule extension is solved;
- that the even-k result is tie-free.

Preferred phrasing:

> The result identifies a semantic boundary of LOO evidence rather than a failure of LOO cross-validation as an error-estimation tool.

---

## 3. Proposed paper structure

Use this structure for the Machine Learning submission.

```text
1. Introduction
   1.1 What LOO does and does not certify
   1.2 Minimal two-point witness
   1.3 Contributions and scope

2. Related Work
   2.1 Algorithmic stability and generalization
   2.2 Nearest-neighbor classification and deleted estimates
   2.3 Cross-validation, conformal prediction, and training-set perturbations

3. Perturbation Semantics
   3.1 Ordered finite samples and deterministic k-NN
   3.2 Delete-one, insert-one, replace-one
   3.3 LOO as coupled delete-and-evaluate-at-deleted-occurrence

4. Uniform Perturbation Calculus
   4.1 Replace-one = delete-one + insert-one
   4.2 Uniform bound
   4.3 Why LOO cannot replace delete-one control

5. Margin-Crossing Mechanism for Deterministic k-NN
   5.1 Top-k ordering
   5.2 Signed margin
   5.3 Margin-crossing proposition
   5.4 Vulnerability diagnostic

6. Separations
   6.1 Minimal 1-NN witness
   6.2 Odd-k construction
   6.3 Even-k construction and deterministic tie-breaking
   6.4 What remains open for even k

7. Stability Hierarchy
   Only include rigorously proved implications and counterexamples.

8. Experiments
   8.1 Goals and metrics
   8.2 Theorem verification and computational certificates
   8.3 Synthetic graph metrics
   8.4 Euclidean/tabular benchmarks
   8.5 Diagnostic precision/recall
   8.6 Ablations and limitations

9. Extensions and Discussion
   9.1 What extends to local vote rules
   9.2 Limitations
   9.3 Open problems
```

Key restructuring decision: move the broad deterministic local vote rule material to the end. The current paper is strongest when the reader first sees the k-NN theorem and then hears about possible extensions.

---

## 4. Mandatory correction list from the current PDF

Codex must search the LaTeX source and fix all items below.

### 4.1 Cross-reference/type errors

- Replace every post-proof sentence saying `Theorem 4.2` with `Proposition 4.2` unless the environment is changed to theorem.
- Replace every post-proof sentence saying `Theorem 5.1` with `Proposition 5.1` unless changed consistently.
- Ensure Theorem 7.1 excludes `k=1` and says `m >= 1`; the `k=1` case is handled by the two-point theorem/proposition.
- In Appendix A.4, use the same indexing convention as the main text. The main text is 1-based; code is 0-based. Do not write `index 0` in the mathematical appendix unless explicitly declaring code indexing.
- In Section 7.3, change `For all m >= 0` to `For all m >= 1` in the LOO-at-b calculation.

### 4.2 Claims that need tightening

- Replace `sharp` with `semantically sharp` only when referring to the delete/insert/replace distinction. Do not imply metric tightness of the numerical bound unless a tightness witness is proved.
- The current diagnostic claim `|M_k(S,x)| <= 2` should be stated precisely:
  - for odd k and arbitrary replacement points allowed in `X x {0,1}`, it characterizes existence of a one-replacement prediction flip at query `x`;
  - for even k, tie-breaking makes the threshold asymmetric, so report it as a useful flag, not a universal iff statement unless proved.
- In the hierarchy table, remove entries with no explicit counterexample in the paper. Do not keep `standard` as a proof reference.

### 4.3 Current experimental contradiction

The PDF says synthetic separation frequency both decreases with k and rises from 0.32 at k=1 to 0.48 at k=5 under duplicate ratio 0.6. Codex must inspect the raw data and decide which statement is correct. If the phenomenon is non-monotone, say so and plot it. If the earlier line is wrong, delete it.

### 4.4 Figure placement and numbering

The rendered PDF places Figures 1-3 around pages 18-19, interleaved with or after references. Page 19 also shows an internal image title `Figure 8` while the caption below is `Figure 3`. This is unacceptable for journal submission.

Required LaTeX fixes:

- Move figures into the sections where they are discussed.
- Use `\FloatBarrier` before the references.
- Remove any internal figure number text inside the image files.
- Use captions as the only figure numbering mechanism.
- Use vector PDF/SVG source when possible.

---

## 5. Code/repository work plan

Work in a new branch:

```bash
git checkout -b ml-submission-rewrite
```

Use the existing environment convention in the repository:

```bash
conda run -n pytorch-clean python -V
conda run -n pytorch-clean pytest
```

If the Windows path style in the README is still needed locally, keep it in a local note, but repository scripts should also support standard conda environment names.

### Stage A: freeze definitions

Deliverables:

- `docs/project-control/02_DEFINITIONS_SPEC.md` updated from `add-one` to `insert-one`.
- A decision record: `docs/decision-records/DR-001-insert-one-vs-add-one.md`.
- LaTeX definitions updated to match.
- Code docstrings updated.

Acceptance:

- No occurrence of paper-level `add-one` remains except in a historical note.
- All `insert_position` semantics are documented as 0-based in code and 1-based in paper.

### Stage B: fix primitives and tests

Deliverables:

- `src/knn_stability/perturbations.py` or updated `stability.py`.
- Tests for delete, insert, replace, LOO, and delete-then-insert equivalence.
- Tests for all theoretical witnesses.

Acceptance:

```bash
conda run -n pytorch-clean pytest -q
```

must pass.

### Stage C: rewrite paper source

Deliverables:

- Move to Springer Nature template in `submit/manuscript/`.
- Preserve one source of truth for theorem labels.
- No manual theorem numbers in prose.

Acceptance:

- `latexmk -pdf main.tex` compiles cleanly.
- No unresolved references.
- No figures after references unless they are in appendix after the bibliography by design.

### Stage D: rebuild experiments

Use `codex_docs/02_EXPERIMENT_REDESIGN_SPEC.md` as the experiment contract.

### Stage E: rebuild figures

Use `codex_docs/04_FIGURE_DESIGN_BRIEF.md` as the figure contract.

### Stage F: reference audit

Use `codex_docs/03_REFERENCE_AUDIT_AND_BIBLIOGRAPHY.md` as the reference contract.

---

## 6. Final submission acceptance checklist

Before submission, Codex must be able to answer yes to all of these:

- Are all definitions identical across PDF, LaTeX, code, and docs?
- Does every theorem have a proof or an explicitly labeled proof sketch?
- Does every hierarchy-table entry have a theorem/proposition/counterexample reference?
- Are experiments reproducible from one command?
- Are all random seeds stored?
- Are all result tables generated from raw outputs, not manually typed?
- Are all figures referenced before or near where they appear?
- Are all figure labels readable at journal scale?
- Are all references real and used for the claim they support?
- Does the paper avoid unsupported claims about LOO, robustness, and local vote rules?
- Does the Machine Learning submission folder contain manuscript, source, figures, tables, supplementary material, cover letter, and declarations?

