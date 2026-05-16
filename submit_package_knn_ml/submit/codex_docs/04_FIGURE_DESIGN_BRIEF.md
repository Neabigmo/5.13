# Figure design brief for Codex / image2

The current figures have a pleasant visual direction, but they are too infographic-like and are placed incorrectly. For a journal article, figures should be simpler, more mathematical, and less poster-like.

General style:

- Use vector diagrams when possible: PDF/SVG generated from Python/matplotlib/TikZ.
- Use one muted accent color for label 0 and one for label 1.
- Use gray for non-decisive/background occurrences.
- Do not put paragraphs inside figures.
- Do not include internal figure numbers inside image files.
- All text must remain readable after the figure is scaled to single-column width.
- Captions should explain the figure; the figure itself should show the mechanism.
- Prefer clean mathematical schematics over decorative icons.

---

## Figure 1: Perturbation semantics map

Purpose: introduce the central distinction.

Layout:

- A 2-axis diagram.
- Horizontal axis: perturbation operation (`delete`, `insert`, `replace`).
- Vertical axis or side labels: evaluation convention (`deleted occurrence`, `arbitrary query`).
- Show LOO as a highlighted special case of delete-one with evaluation fixed to the deleted occurrence.
- Show replace-one as `delete + insert` with arbitrary query.

Visual content:

```text
LOO: delete i -> evaluate at x_i
Delete-one: delete i -> evaluate at arbitrary x
Insert-one: insert z at j -> evaluate at arbitrary x
Replace-one: replace i by z -> evaluate at arbitrary x
```

Do not make it a large infographic. A compact table plus arrows is enough.

Suggested caption:

```text
Perturbation notions differ both in the operation applied to the sample and in the point at which the perturbed predictor is evaluated. LOO is a coupled delete-and-evaluate-at-the-deleted-occurrence diagnostic; replace-one decouples perturbation and evaluation.
```

---

## Figure 2: Minimal two-point witness

Purpose: make the central counterexample instantly understandable.

Layout:

- Left panel: original sample with two metric points `a` and `b`, both label 0.
- Middle panel: LOO deletion cases. Deleting either point leaves a single label-0 neighbor.
- Right panel: replace first `(a,0)` with `(a,1)`, query at `a`, prediction flips.

Use only two nodes connected by one edge. Do not add decorative backgrounds.

Key annotations:

```text
LOO_max = 0
REP_max = 1
M_before(a) = -1
M_after(a) = +1
```

Suggested caption:

```text
The minimal 1-NN separation. Both leave-one-out deletions preserve the deleted point's prediction, but replacing the occurrence at a by the opposite label flips the prediction at query a.
```

---

## Figure 3: Margin-crossing mechanism

Purpose: show that all perturbation effects reduce to a threshold crossing.

Layout:

- A horizontal signed-margin axis.
- Threshold at 0.
- Region `M <= 0`: prediction 0.
- Region `M > 0`: prediction 1.
- Arrow examples: `-1 -> +1` for odd k, `0 -> +2` for even k.

Add a small top-k vote strip above the axis:

```text
0-vote contributes -1
1-vote contributes +1
```

Suggested caption:

```text
For deterministic binary k-NN with label ties resolved to 0, the prediction is 1 exactly when the signed top-k vote margin is positive. A perturbation changes the prediction exactly when it moves the margin across this threshold.
```

---

## Figure 4: Odd-k construction family

Purpose: summarize the proof without showing every duplicate individually.

Layout:

- Two metric locations `a` and `b`.
- At `a`, show two stacked count boxes: `(m+1) x label 0`, `m x label 1`.
- At `b`, show one count box: `m x label 0`.
- Left side: before replacement, top-k at a has margin `-(m+1)+m=-1`.
- Right side: after replacing one `(a,0)` by `(a,1)`, margin is `+1`.

Use count notation instead of drawing dozens of copies. It will look cleaner.

Suggested caption:

```text
Odd-k witness family. Duplicate occurrences keep every LOO evaluation on the label-0 side of the threshold, while replacing one decisive label-0 occurrence by label 1 moves the query-a margin from -1 to +1.
```

---

## Figure 5: Even-k and tie-breaking

Purpose: show why the even-k theorem is tie-dependent.

Layout:

- Same count style as Figure 4.
- Before: at a, `m x label 0` and `m x label 1`, margin 0, tie -> prediction 0.
- After: replacement gives margin +2, prediction 1.
- Include a small tie-breaking box: `M=0 -> label 0` under `0 ≺ 1`.

Do not make a full three-row flowchart. The current page-19 tie-breaking diagram is too poster-like and too text-heavy.

Suggested caption:

```text
Even-k separation under deterministic label-order tie-breaking. The original query-a vote is tied and is resolved to label 0; one replacement moves the margin to +2. This dependence on the tie-breaking convention is absent from the odd-k construction.
```

---

## Figure 6: Experiment overview/results figure

Purpose: one compact main-results figure for the experimental section.

Use generated plots from data, not image2 artwork.

Suggested panels:

- Panel A: heatmap of strict-gap frequency over duplicate ratio and k for synthetic graph metrics.
- Panel B: vulnerable-query rate vs k with confidence intervals.
- Panel C: tabular dataset strict-gap frequency by dataset and k.

Rules:

- Use matplotlib, no seaborn requirement if running in this environment; in the repository either is fine if dependencies are controlled.
- Use vector PDF for submission.
- Keep axis labels short.
- Put detailed configuration in caption or appendix table.

Suggested caption:

```text
Empirical occurrence of the LOO/replace-one gap. Strict-gap frequencies and vulnerable-query rates are computed from exhaustive replacement search on each sampled configuration; intervals indicate 95% Wilson confidence intervals over independent trials.
```

---

## Appendix figures

Only keep appendix figures if they add distinct information.

### Appendix Figure A1: Deletion cases

Show two cases:

1. deleted occurrence outside top-k: top-k unchanged;
2. deleted occurrence inside top-k: rank k+1 promoted.

Make it much simpler than the current figure on page 18. Use only boxes and arrows; no dense small text.

### Appendix Figure A2: Replace-one mechanisms

Show two mechanisms:

1. geometry changes top-k membership;
2. label changes while neighborhood membership remains effectively fixed.

Again: two small panels, no poster-style explanation blocks.

---

## image2 prompt template

Use this template for mechanism figures, then manually polish in vector form if possible:

```text
Create a clean academic journal vector-style diagram, white background, minimal muted colors, no decorative icons, no internal figure number. Show [mechanism]. Use label 0 as muted blue boxes/circles and label 1 as muted orange boxes/circles; non-decisive points gray. Use large readable text, short mathematical annotations only, and leave explanatory detail for the caption. The diagram should look like a theorem illustration in a machine learning journal, not like a poster or slide infographic.
```

For final submission, prefer recreating image2 drafts with TikZ/matplotlib to guarantee font consistency.
