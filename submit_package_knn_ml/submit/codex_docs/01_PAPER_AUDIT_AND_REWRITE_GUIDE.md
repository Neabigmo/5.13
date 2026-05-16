# Paper audit and rewrite guide

This guide gives Codex a section-by-section review of the current 19-page PDF. It is not a cosmetic copyedit list; it identifies conceptual, logical, and stylistic changes required before submitting to *Machine Learning*.

---

## 1. Global writing diagnosis

The draft has a good core and a much better narrative than earlier versions. The main idea is now visible: LOO is a restricted evaluation convention, not a replacement-robustness certificate. However, the current style still has three problems:

1. **Some sentences sound too declarative.** Phrases like `The trap`, `No asymptotics, randomness, or high-dimensional geometry is needed`, and `LOO is not wrong, it answers a different question` are useful once, but repeated rhetorical emphasis creates a blog-like tone.
2. **Some claims run ahead of the evidence.** The experiments are currently too thin to support strong practical language like `structurally stable phenomenon detectable beyond hand-crafted examples` unless rebuilt.
3. **Some formal names are inconsistent.** Proposition vs theorem, insert-one vs add-one, LOO stability vs LOO indicator, fixed-sample maxima vs uniform stability all need discipline.

Target tone:

> calm, exact, modestly ambitious, theorem-led, and useful to ML researchers who care about stability, cross-validation, and robustness.

Avoid:

- slogans as standalone paragraphs;
- `trap` more than once;
- saying `obvious`, `tautological`, or `not cosmetic` too often;
- overexplaining simple examples after the point has landed.

---

## 2. Title and abstract

### Current title

`Leave-One-Out Stability Does Not Certify Replacement Robustness in k-Nearest Neighbors`

Recommendation: keep it. It is more accurate and less overbroad than `A Stability Calculus for Local Learning Rules`.

### Abstract rewrite target

The abstract should have exactly four moves:

1. Define the common misinterpretation.
2. State the semantic reason it fails.
3. State the finite-sample separation theorem.
4. State the diagnostic/experiment contribution without overselling.

Suggested replacement:

```text
Leave-one-out evaluation is often read as evidence that a classifier is insensitive to individual training points. For deterministic k-nearest-neighbor classification, this interpretation conflates two different perturbation semantics: LOO deletes a training occurrence and evaluates at that same occurrence, whereas replacement robustness permits an arbitrary occurrence to be replaced and evaluates the resulting predictor at an arbitrary query. We formalize this distinction and show that it leads to a finite-sample separation. For every odd k, and for every even k under deterministic tie-breaking, there are finite metric samples for which all LOO indicators vanish while one replace-one perturbation flips the prediction at a designated query. The mechanism is an exact signed top-k vote-margin crossing. We further give a margin-based vulnerability diagnostic and reproducible experiments on finite graph metrics and tabular data, showing how often the same mechanism appears outside the constructed witnesses. These results clarify the semantic boundary of LOO evidence: it is a coupled deletion diagnostic, not a certificate of replacement robustness.
```

Notes:

- `finite-sample separation` is better than `sharp structural separation` unless formal sharpness is defined.
- `showing how often` is safer than `showing that the phenomenon is structurally stable`.

---

## 3. Introduction

### 1.1 The leave-one-out stability trap

Keep the core question:

```text
When a perturbation is applied to the training sample, what exactly has been perturbed, and where is the perturbed predictor evaluated?
```

This is a strong guiding question. But reduce rhetorical framing.

Replace:

```text
The reasoning seems natural: if removing a point barely changes the prediction at that same point, the classifier must be stable.
```

With:

```text
The reasoning is tempting: if deleting each training occurrence leaves the prediction at that occurrence unchanged, then the learned rule may appear insensitive to single training points.
```

Replace:

```text
the flaw is conceptual, not asymptotic
```

With:

```text
the distinction is already visible at the level of fixed finite samples.
```

### 1.2 Two-point preview

This is excellent and should remain early. Make it visually supported by a small figure. Make sure the sample tuple renders cleanly in the source.

Use one theorem/proposition later; do not overstate in the preview.

Replace:

```text
No asymptotics, randomness, or high-dimensional geometry is needed.
```

With:

```text
Thus the mismatch is not caused by asymptotics or high-dimensional geometry; it is already present in the smallest nontrivial finite metric space.
```

### 1.3 Contributions

Keep four contributions, but make them less promotional.

Recommended contribution wording:

1. Perturbation semantics: formal separation of delete, insert, replace, and LOO evaluation conventions.
2. Perturbation calculus: replace-one is delete-one followed by insert-one at the deleted position; this gives the correct direction of uniform control.
3. k-NN margin mechanism: prediction changes exactly when the signed top-k vote margin crosses the deterministic decision threshold.
4. Separations and diagnostics: finite witness families for odd and deterministic even k, plus a reproducible margin-vulnerability study.

Avoid saying `LOO cannot substitute` in the contribution list unless the exact theorem/counterexample is nearby.

---

## 4. Related work

The current related work is broadly correct but too compressed. It should distinguish these literatures clearly:

1. algorithmic stability and generalization;
2. nearest-neighbor consistency and deleted estimates;
3. cross-validation/LOO and conformal stability;
4. optional short paragraph on training-set perturbation / data poisoning as motivation, not as a direct prior.

### Suggested language for stability paragraph

```text
Classical algorithmic stability uses sample perturbations to control generalization under a sampling model. Bousquet and Elisseeff introduced uniform stability as a sufficient condition for generalization; Kutin and Niyogi studied weaker almost-everywhere variants; later work refined high-probability bounds and stability-based optimization analyses. This paper asks a different finite-sample question: not how a stability condition controls risk, but which perturbation/evaluation convention a reported stability quantity actually controls.
```

### Suggested language for nearest-neighbor paragraph

```text
Nearest-neighbor rules have a classical distributional theory, beginning with Fix and Hodges, Cover and Hart, Cover, and Stone. Deleted-estimate analyses by Rogers and Wagner and by Devroye and Wagner are especially relevant because they connect local discrimination rules with leave-one-out-style evaluation. Our results are not asymptotic risk bounds; they isolate a fixed-sample adversarial replacement gap that is invisible to LOO evaluation.
```

### Suggested language for conformal paragraph

```text
Recent conformal-prediction work again makes stability distinctions operational, particularly when moving from marginal guarantees to training-conditional guarantees. These works use stability to support coverage claims. Our setting is narrower but sharper: deterministic k-NN with 0-1 prediction loss on finite metric samples.
```

---

## 5. Definitions and semantics

### 5.1 Rename `LOO / CVloo Stability`

The object defined in Definition 3.11 is an indicator, not a full stability theory. Use:

```text
Definition 3.11 (LOO indicator).
```

Then later define `LOO-stable at sample S` if all indicators vanish.

### 5.2 State domain restrictions

Add before Definition 3.11:

```text
Throughout the LOO definitions we assume n >= 2 so that the deleted sample is nonempty. When k exceeds the post-deletion sample size, we use k' = min(k,n-1).
```

This prevents boundary ambiguity.

### 5.3 Avoid duplicate formulas

The current Section 3.3 defines LOO and then repeats all indicators. Keep the table and one compact display, not both long prose and repeated definitions.

### 5.4 Use insert-one, not add-one

The paper currently does this correctly. Ensure the repository follows it. In the paper, keep insertion position explicit because sample index is part of tie-breaking.

---

## 6. Uniform perturbation calculus

The content is right, but terminology needs precision.

Replace:

```text
Theorem 4.2 is deliberately abstract.
```

With:

```text
Proposition 4.2 is deliberately abstract.
```

Replace:

```text
The decomposition is sharp in a semantic sense
```

With:

```text
The decomposition gives the correct semantic direction of control: replace-one can be bounded by delete-one plus insert-one, but LOO supplies neither of those two uniform ingredients.
```

Add a one-sentence warning:

```text
Because deterministic tie-breaking depends on sample order, the insertion operation in this proposition must allow insertion at the deleted position, not only appending at the end.
```

This directly repairs the code-paper mismatch.

---

## 7. Margin mechanism

This is one of the strongest sections. Keep it concise.

Fix:

- `Theorem 5.1` -> `Proposition 5.1`.
- Avoid saying `every perturbation argument can be reduced` if the replacement also changes `k` or the ambient label space. Say `for the perturbations considered here`.

Add a formal lemma for the diagnostic:

```text
Lemma. For odd k, at a fixed query x, there exists a one-replacement perturbation that flips the deterministic k-NN prediction if and only if |M_k(S,x)| <= 2.
```

Then prove it separately. This will make Section 10.4 much less hand-wavy.

---

## 8. Separation theorems

### 8.1 Minimal 1-NN witness

Promote this to a formal proposition:

```text
Proposition 6.1 (Minimal 1-NN separation).
```

Do not claim a proof of minimality unless you prove no one-point witness exists. If mentioning computational search, call it a certificate within a bounded search space, not a theorem.

### 8.2 Odd-k theorem

Current theorem is basically sound. Fix minor details:

- `For all m >= 0` -> `m >= 1` in the LOO-at-b case.
- Use `k=2m+1 >= 3` in the construction statement.
- State `k=1` is Proposition 6.1, not part of Theorem 7.1.

### 8.3 Even-k theorem

Keep it, but make the dependence on deterministic tie-breaking visible in the theorem statement:

```text
Theorem 8.1 (Deterministic tie-breaking even-k separation).
```

Add in the theorem statement:

```text
under the fixed label-order tie-break 0 ≺ 1.
```

### 8.4 Tie-free even-k open problem

Good to keep, but phrase as a limitation/open problem rather than a weakness that undermines the theorem.

---

## 9. Stability hierarchy

This section currently risks overclaiming. Keep only rows that are explicitly proved.

Recommended table:

| Relationship | Status | Evidence |
|---|---|---|
| Uniform delete-one + uniform insert-one => uniform replace-one | theorem/proposition | Proposition 4.2 |
| Pointwise delete-one over all queries => LOO | immediate | definitions |
| LOO => pointwise replace-one | false | Proposition 6.1 / Theorem 7.1 / Theorem 8.1 |
| LOO => pointwise delete-one over all queries | false | Appendix counterexample |

Move `expected vs worst-case` statements to prose or remove unless a distributional setup is defined.

For `pointwise replace-one => LOO`, either give a concrete counterexample or remove the row. `Different evaluation quantification` is not enough.

---

## 10. Experiments

The current experiment section should be treated as a placeholder. It has the right intent but not enough structure. Replace it with the plan in `02_EXPERIMENT_REDESIGN_SPEC.md`.

Specific current sentence to fix:

```text
separation frequency decreases as k grows ... At k=1 ... 0.32, and it rises to 0.48 at k=5.
```

This is contradictory. Codex must recompute and then write one of:

```text
For fixed duplicate ratio 0.6, the separation frequency is non-monotone in k.
```

or

```text
The previously reported increase was caused by [bug]. After fixing insert-one semantics, the frequency decreases with k.
```

Do not write either without raw result support.

---

## 11. Extensions and discussion

The current extension to deterministic local vote rules is sensible, but should be explicitly limited.

Replace:

```text
Any deterministic local classifier whose prediction depends on a signed sum ... admits a margin-crossing criterion.
```

With:

```text
The margin-crossing proof extends to deterministic local rules whose prediction can be written as a thresholded scalar score and whose perturbations are analyzed through the induced score change.
```

Do not mention `certain decision-tree voting schemes` unless you define exactly what kind. It sounds vague.

---

## 12. AI-generated-text risk

The paper is not obviously AI-generated in grammar, but some rhetorical patterns are AI-like:

- repeated `This section answers:` openings;
- repeated `The key message is:`;
- repeated contrasts like `not X, but Y`;
- broad summary bullets after already clear paragraphs.

Fix by reducing formulaic transitions. Let section titles carry the structure.

Examples:

| Current style | Better style |
|---|---|
| `This section answers: ...` | Start directly with the mathematical question or definition. |
| `The whole point of the calculus is...` | `This is why LOO cannot be substituted for delete-one in Proposition 4.2.` |
| `The key message...` | Delete or merge into previous paragraph. |
| `not confined to hand-crafted witnesses` | `also appears in the sampled configurations reported below` |

---

## 13. Final polish pass

After all revisions, Codex should run a mechanical search for:

```text
Theorem 4.2
Theorem 5.1
add-one
current draft
v0.1
Figure 8
trap
sharp
structurally stable
obvious
tautological
```

Each occurrence must be justified or removed.
