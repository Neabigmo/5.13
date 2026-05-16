# Full experiment redesign specification

The current experiments should be rebuilt rather than patched. The paper's theoretical results are finite-sample and exact; the experiments should therefore be designed as an audit trail for the mechanism, not as a vague empirical appendix.

---

## 1. Experimental goals

The experiments must answer five questions:

1. **Implementation correctness**: do the code primitives reproduce the theoretical witnesses for every tested k?
2. **Search/minimality evidence**: in bounded finite graph spaces, where do LOO/replace-one gaps first appear?
3. **Structural frequency**: how often do strict gaps appear in random finite graph metrics as duplicates, conflicts, noise, n, and k vary?
4. **Diagnostic accuracy**: does the margin condition predict replace-one vulnerability exactly for odd k and how does it behave for even k?
5. **Tabular relevance**: on standard Euclidean datasets, how often do LOO-stable samples still contain replace-one-vulnerable queries?

Experiments are not needed to prove the separation theorem. They are needed to show that the mechanism is not merely a toy construction and to validate code-level definitions.

---

## 2. Required code primitives

Before running experiments, implement and test these primitives.

```python
topk_indices(sample, query_point_idx, k) -> tuple[int, ...]
signed_margin(sample, query_point_idx, k) -> int
predict_knn(sample, query_point_idx, k) -> int
insert_one_sample(sample, insert_position, point_idx, label) -> LabeledSample
replace_one_sample(sample, replace_index, point_idx, label) -> LabeledSample
pointwise_loo_indicator(sample, delete_index, k) -> int
pointwise_replace_indicator(sample, replace_index, point_idx, label, query_point_idx, query_label, k) -> int
exists_replace_flip(sample, query_point_idx, k) -> bool
fixed_sample_loo_max(sample, k) -> int
fixed_sample_replace_max(sample, k) -> int
```

Important naming rule: avoid calling fixed-sample brute-force maxima `uniform_*` in code. Paper-level uniform stability ranges over all samples; experiment code mostly ranges over one sample.

---

## 3. Metrics to report

For each sample `S` and k:

```text
LOO_max(S,k)       = max_i Delta_loo(S,i)
REP_max(S,k)       = max_{i,z,x,y} Delta_rep(S,i,z,x,y)
strict_gap(S,k)    = 1{LOO_max=0 and REP_max=1}
loo_unstable(S,k)  = 1{LOO_max=1}
rep_vulnerable_rate(S,k) = fraction of query points x with exists_replace_flip(S,x,k)=1
margin_flag_rate(S,k)    = fraction of query points x with |M_k(S,x)| <= 2
margin_precision/recall  = compare |M_k|<=2 to exists_replace_flip
mean_abs_margin          = average_x |M_k(S,x)|
min_abs_margin           = min_x |M_k(S,x)|
```

For binary 0-1 loss, reporting prediction flips is cleaner than reporting loss changes. The paper can define both and note that for binary 0-1 loss an absolute loss change occurs exactly when prediction changes, for a fixed query label.

---

## 4. Experiment A: theorem witness verification

Purpose: verify that all theoretical witnesses are implemented correctly.

### A1. Minimal 1-NN witness

Sample: `[(a,0),(b,0)]`, k=1.

Report:

| k | n | LOO_max | REP_max | replacement | query | margin_before | margin_after |
|---|---:|---:|---:|---|---|---:|---:|

Expected: LOO_max=0, REP_max=1, margin -1 -> +1 at query a.

### A2. Odd-k construction

For `m=1..10`, k=2m+1.

Sample:

```text
(a,0) repeated m+1
(a,1) repeated m
(b,0) repeated m
```

Expected:

- all LOO indicators are 0;
- replace first `(a,0)` by `(a,1)` flips query `(a,0)`;
- margin at a: -1 -> +1.

### A3. Even-k deterministic tie-breaking construction

For `m=1..10`, k=2m.

Sample:

```text
(a,0) repeated m
(a,1) repeated m
(b,0) repeated m
```

Expected:

- all LOO indicators are 0 under label tie-break 0;
- replace first `(a,0)` by `(a,1)` flips query `(a,0)`;
- margin at a: 0 -> +2;
- mark as tie-dependent.

Output files:

```text
outputs/raw/theorem_witness_verification.jsonl
outputs/tables/theorem_witness_verification.csv
outputs/tables/theorem_witness_verification.tex
```

---

## 5. Experiment B: bounded exhaustive graph search

Purpose: provide computational certificates, not theorem replacements.

### B1. Search spaces

Run three nested spaces:

1. **simple no-duplicate occurrence space**
   - connected unlabeled or labeled graphs with |V| <= 5;
   - sample uses each vertex exactly once;
   - all sample orders;
   - all binary labelings;
   - k in {1,3,5} where valid.

2. **bounded duplicate occurrence space**
   - connected graphs with |V| <= 4;
   - sample size n <= 7;
   - all point-index sequences up to symmetries if feasible;
   - all binary label sequences;
   - k in {1,2,3,4,5} where valid.

3. **two-point exact family search**
   - metric space {a,b};
   - all samples up to n <= 12;
   - all binary labels;
   - all k <= min(n,9);
   - classify all strict-gap samples by count pattern.

### B2. What to report

- number of graphs/samples evaluated;
- number of skipped invalid samples;
- minimal n and |X| for strict gaps;
- counts by k;
- whether gaps require duplicates/conflicting labels in each space;
- representative witness JSON.

### B3. Warning language

Use this exact wording in the paper:

```text
The exhaustive search is a bounded computational certificate for the enumerated spaces. It is not used as a substitute for the analytic witness constructions.
```

Output files:

```text
outputs/raw/exhaustive_graph_search.jsonl
outputs/witnesses/minimal_witnesses.json
outputs/tables/exhaustive_search_summary.csv
outputs/tables/exhaustive_search_summary.tex
```

---

## 6. Experiment C: random graph metric factorial study

Purpose: show structural frequency under controlled finite metric sampling.

### C1. Graph generation

- model: Erdos-Renyi connected graphs `G(q,p)`;
- q in `{2,3,4,5,8,10}`;
- p in `{0.3,0.5,0.8}`;
- reject disconnected graphs;
- metric: shortest-path distance.

### C2. Sample generation

Use sample sizes:

```text
n in {10, 25, 50}
```

Factors:

```text
duplicate_ratio in {0.0, 0.25, 0.5, 0.75}
conflict_ratio  in {0.0, 0.25, 0.5}
label_noise     in {0.0, 0.1, 0.2}
k               in {1,2,3,4,5,7,9}, only if k <= n
```

Trials:

- at least 200 independent trials per configuration for main tables;
- 50 is too small for publication-quality frequency claims.

### C3. Sampling protocol

Codex must implement this explicitly and document it:

1. Draw a base class probability for each vertex.
2. Draw sample point occurrences with controlled duplicate ratio.
3. Assign labels according to vertex class probability.
4. Introduce conflicts by forcing selected vertices to contain both labels.
5. Apply independent label noise.
6. Store the full seed and generated sample.

Do not leave duplicate/conflict/noise definitions vague.

### C4. Main outputs

- heatmap: strict_gap frequency by duplicate_ratio and k, faceted by conflict/noise level;
- line plot: vulnerable-query rate vs k, with confidence intervals;
- table: logistic regression or simple effect-size summary showing duplicate_ratio as a driver.

Use Wilson intervals for binary frequencies. Bootstrap over trials is also acceptable; use one consistently.

Output files:

```text
outputs/raw/random_graph_trials.parquet
outputs/tables/random_graph_summary.csv
outputs/figures/random_graph_gap_heatmap.pdf
outputs/figures/random_graph_margin_rate.pdf
```

---

## 7. Experiment D: Euclidean/tabular benchmark

Purpose: show that the phenomenon can occur in non-graph Euclidean metric samples.

### D1. Datasets

Use stable built-in datasets first, because they are reproducible without network access:

- Iris;
- Wine;
- Breast Cancer Wisconsin;
- Digits.

Optional if internet is available and license permits:

- selected OpenML binary classification datasets, but keep them supplementary.

### D2. Preprocessing

- standardize continuous features using training-subsample statistics;
- use Euclidean distance;
- binary conversions:
  - one-vs-rest for every class, not only class 0;
  - for naturally binary datasets, keep labels as given;
- sample sizes: `{25,50,100,200}` where valid;
- subsamples: at least 200 random subsamples per dataset/binary task/sample size.

### D3. Metrics

Report:

- strict_gap frequency;
- LOO_max frequency;
- REP_max frequency;
- vulnerable-query rate;
- margin distribution.

Do not only report `strict_gap`. It hides cases where replace-one vulnerability exists but LOO is already unstable.

### D4. Interpretation rules

If k=1 gives vulnerable-query rate 1.0, explain that this is mathematically expected because the signed 1-NN margin has absolute value 1. Do not present it as a surprising empirical discovery.

If strict_gap is high for Iris/Digits, explain it through the leave-one-out nearest-neighbor agreement rate.

Output files:

```text
outputs/raw/tabular_trials.parquet
outputs/tables/tabular_summary.csv
outputs/tables/tabular_summary.tex
outputs/figures/tabular_gap_by_dataset.pdf
outputs/figures/tabular_margin_histograms.pdf
```

---

## 8. Experiment E: diagnostic precision and recall

Purpose: validate the margin diagnostic against brute-force replacement search.

For each sample/query/k:

```text
flag(x) = 1{|M_k(S,x)| <= 2}
truth(x) = 1{exists a replace-one perturbation flipping prediction at x}
```

Report separately for:

- odd k;
- even k with tie-break 0;
- even k with tie-break 1, if implemented;
- randomized tie-breaking only if expectation is clearly defined.

Expected:

- odd k: precision=1, recall=1 if arbitrary replacement points are allowed and the implementation is correct;
- even k: report asymmetry, do not force a theorem unless proved.

Output files:

```text
outputs/tables/diagnostic_precision_recall.csv
outputs/figures/diagnostic_confusion_by_k.pdf
```

---

## 9. Experiment F: tie-breaking ablation

Purpose: show even-k dependence on deterministic tie-breaking.

Implement tie-breaking modes:

```text
label_tie = 0
label_tie = 1
sample_index_tie = ascending
sample_index_tie = descending
```

Optional randomized mode requires a clear stochastic definition:

- either shared randomness across original and perturbed predictors;
- or independent randomness;
- or expected loss under predictor randomness.

Do not mix these.

Report:

- even-k strict_gap frequency under each deterministic tie-breaking mode;
- which witness families survive or reverse.

---

## 10. Reproducibility contract

Create a single runner:

```bash
conda run -n pytorch-clean python experiments/run_all.py \
  --config experiments/configs/ml_main.yaml \
  --output-dir outputs/ml_main \
  --seed 20260516
```

The runner must:

1. save a copy of the config;
2. save git commit hash;
3. save Python/package versions;
4. write raw results before summaries;
5. generate tables from raw results;
6. generate figures from summary data;
7. produce a run manifest with checksums.

Required manifest:

```text
outputs/ml_main/MANIFEST.json
```

It should include:

- command;
- start/end time;
- git commit;
- random seed root;
- files generated;
- sha256 checksums;
- test status.

---

## 11. What the paper should say about experiments

Suggested opening:

```text
The preceding sections give worst-case finite-sample constructions. The experiments below have a different role: they audit the implementation, quantify how often the margin-crossing mechanism appears in sampled finite metrics, and test the margin diagnostic against exhaustive replacement search.
```

Suggested closing:

```text
The experiments should not be read as distributional guarantees. They show that the same finite-sample mechanism responsible for the analytic witnesses is detectable in broader sampled configurations, and that the signed-margin diagnostic provides a compact way to locate vulnerable queries.
```
