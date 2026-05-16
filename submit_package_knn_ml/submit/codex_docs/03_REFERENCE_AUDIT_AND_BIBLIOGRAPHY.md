# Reference audit and bibliography expansion plan

This document audits the current reference list and gives Codex precise instructions for expanding the literature review without inventing citations.

---

## 1. Current bibliography audit

| Current ref | Status | Use in paper | Action |
|---|---|---|---|
| Bousquet & Elisseeff (2002), *Stability and Generalization*, JMLR | Real and central | uniform stability/generalization | Keep. Use as the anchor for stability. |
| Bousquet, Klochkov & Zhivotovskiy (2020), *Sharper bounds for uniformly stable algorithms* | Real | modern high-probability uniform stability | Keep. Verify PMLR pages. |
| Cover (1968), *Estimation by the nearest neighbor rule* | Real | nearest-neighbor classical background | Keep. |
| Cover & Hart (1967), *Nearest neighbor pattern classification* | Real and essential | 1-NN/k-NN risk background | Keep. |
| Devroye & Wagner (1979), deleted/holdout error estimates | Real | deleted estimates | Keep. |
| Devroye & Wagner (1979), potential function rules | Real | local discrimination rules/stability history | Keep, but cite only where relevant. |
| Feldman & Vondrak (2019), high-probability stability | Real | modern stability bounds | Keep. Verify conference/proceedings pages. |
| Fix & Hodges (1951) | Real classic technical report | origin of nonparametric discrimination | Keep. Format carefully. |
| Hardt, Recht & Singer (2016) | Real | stability and optimization | Keep, but mention as modern stability background, not directly related to k-NN. |
| Kearns & Ron (1999) | Real and relevant | LOO/stability/CV | Keep. |
| Kutin & Niyogi (2002) | Real | weaker stability notions | Keep. Use UAI/arXiv/technical report format consistently. |
| Liang & Barber (2023) | Real | conformal/training-conditional coverage | Keep if conformal paragraph remains. |
| Pournaderi & Xiang (2024) | Real | uniform stability and conformal coverage | Keep if conformal paragraph remains. |
| Rogers & Wagner (1978) | Real and relevant | finite-sample local discrimination/deleted estimates | Keep. |
| Stone (1977) | Real | k-NN/nonparametric consistency | Keep. |

No obviously fabricated references remain in the current 15-item PDF bibliography. Earlier drafts had riskier items; the current list is cleaner.

---

## 2. Places where references and claims need better alignment

### 2.1 Stability paragraph

Current claim:

```text
Classical algorithmic stability studies how a learning rule changes when the training sample is perturbed, primarily to control generalization error under an i.i.d. sampling model.
```

Support with:

- Bousquet & Elisseeff (2002);
- Kutin & Niyogi (2002);
- Shalev-Shwartz et al. (2010);
- Feldman & Vondrak (2019);
- Bousquet et al. (2020);
- Hardt et al. (2016) only for optimization dynamics.

### 2.2 Nearest-neighbor paragraph

Current claim:

```text
Nearest-neighbor work studies statistical performance under distributional sampling rather than fixed-sample adversarial perturbation.
```

Support with:

- Fix & Hodges (1951);
- Cover & Hart (1967);
- Cover (1968);
- Stone (1977);
- Devroye, Gyorfi & Lugosi (1996) as a broader monograph;
- Hall, Park & Samworth (2008) or Samworth (2012) if discussing k choice/weighted k-NN.

### 2.3 Deleted estimates and local discrimination

Current claim:

```text
Deleted estimates have substantial classical history around nearest-neighbor methods.
```

Support with:

- Rogers & Wagner (1978);
- Devroye & Wagner (1979a,b);
- Kearns & Ron (1999) for LOO/stability links.

### 2.4 Conformal stability paragraph

Only keep this if the paragraph is concise. Support with:

- Vovk, Gammerman & Shafer (2005) for conformal foundations;
- Barber et al. (2021) for jackknife+;
- Liang & Barber (2023);
- Pournaderi & Xiang (2024);
- Lee & Zhang (2025) optional if discussing explicitly LOO-stable conformal methods.

### 2.5 Training-set perturbation motivation

If adding one paragraph motivating replacement robustness as a training-set perturbation concept, use:

- Biggio, Nelson & Laskov (2012), poisoning attacks against SVMs;
- Koh & Liang (2017), influence functions and training point effects;
- Steinhardt, Koh & Liang (2017), certified defenses against data poisoning;
- Barreno et al. (2010), broader security of machine learning.

Important: do not imply this paper solves poisoning. Say only that these literatures motivate careful training-set perturbation semantics.

---

## 3. Recommended added references

Codex should add the following if they are used in the prose.

### Algorithmic stability / learning theory

1. **Shalev-Shwartz, Shamir, Srebro, and Sridharan (2010)**  
   `Learnability, Stability and Uniform Convergence`, JMLR 11:2635-2670.  
   Insert after Bousquet & Elisseeff in Section 2.1.  
   Use to say stability is related to learnability and uniform convergence, not merely a single bound.

2. **Mukherjee, Niyogi, Poggio, and Rifkin (2006)**  
   `Learning theory: stability is sufficient for generalization and necessary and sufficient for consistency of empirical risk minimization`, Advances in Computational Mathematics 25:161-193.  
   Insert in Section 2.1 or LOO/CV paragraph.  
   Use to distinguish CVloo-style stability from the fixed finite-sample semantics in this paper.

3. **Rakhlin, Mukherjee, and Poggio (2005)**  
   `Stability results in learning theory`, Analysis and Applications 3(4):397-419.  
   Optional background if Section 2.1 needs more depth.

### Nearest-neighbor and local rules

4. **Devroye, Gyorfi, and Lugosi (1996)**  
   `A Probabilistic Theory of Pattern Recognition`, Springer.  
   Insert in Section 2.2.  
   Use to separate distributional k-NN theory from fixed-sample perturbation witnesses.

5. **Hall, Park, and Samworth (2008)**  
   `Choice of neighbor order in nearest-neighbor classification`, Annals of Statistics 36(5):2135-2152.  
   Use only if discussing k choice beyond toy k values.

6. **Samworth (2012)**  
   `Optimal weighted nearest neighbour classifiers`, Annals of Statistics 40(5):2733-2763.  
   Use only in the extension paragraph on weighted k-NN.

### Cross-validation / conformal / predictive inference

7. **Kohavi (1995)**  
   `A study of cross-validation and bootstrap for accuracy estimation and model selection`, IJCAI.  
   Optional if the introduction mentions practitioner interpretation of cross-validation.

8. **Vovk, Gammerman, and Shafer (2005)**  
   `Algorithmic Learning in a Random World`, Springer.  
   Use as conformal foundation if conformal paragraph remains.

9. **Barber, Candes, Ramdas, and Tibshirani (2021)**  
   `Predictive inference with the jackknife+`, Annals of Statistics 49(1):486-507.  
   Use if discussing jackknife+ stability/coverage.

### Training-set perturbations / poisoning motivation

10. **Biggio, Nelson, and Laskov (2012)**  
    `Poisoning attacks against support vector machines`, ICML.  
    Use only for motivation.

11. **Koh and Liang (2017)**  
    `Understanding Black-box Predictions via Influence Functions`, ICML.  
    Use to connect individual training points to prediction behavior, not as a stability theorem.

12. **Steinhardt, Koh, and Liang (2017)**  
    `Certified Defenses for Data Poisoning Attacks`, NeurIPS.  
    Use to motivate worst-case training-set perturbation thinking.

13. **Barreno et al. (2010)**  
    `The security of machine learning`, Machine Learning 81:121-148.  
    Useful because it is in the same target journal and frames adversarial ML broadly.

---

## 4. Suggested revised related-work paragraphs

### Stability paragraph

```text
Algorithmic stability studies how a learned predictor changes when the training sample is perturbed, typically in order to control generalization under an i.i.d. sampling model. Bousquet and Elisseeff introduced uniform stability as a central sufficient condition for generalization, while Kutin and Niyogi and Mukherjee et al. developed weaker and CVloo-related variants. Later work clarified the relationship between stability, learnability, and uniform convergence and sharpened high-probability bounds. These works differ from the present paper in their objective: they ask how stability controls risk, whereas we ask which finite-sample perturbation/evaluation convention is actually certified by LOO evidence.
```

### Nearest-neighbor paragraph

```text
Nearest-neighbor classification has a classical distributional theory, beginning with Fix and Hodges and the risk analysis of Cover and Hart and Cover, with consistency results later developed by Stone and subsequent monographs. Deleted-estimate analyses by Rogers and Wagner and Devroye and Wagner are closest in spirit, because they connect local discrimination rules with leave-one-out-style evaluation. Our results are complementary: they do not challenge distributional consistency, but show that a fixed finite sample can be perfectly LOO-stable and still admit an adversarial replace-one prediction flip.
```

### Perturbation/security motivation paragraph

```text
A separate line of work studies how individual training points affect predictions or can be manipulated adversarially. Influence-function analyses and data-poisoning work motivate replacement-style perturbation questions, although they usually study different model classes and threat models. We use this literature only as motivation for being explicit about perturbation semantics; our results are exact finite-sample statements for deterministic k-NN.
```

---

## 5. Bibliography hygiene rules for Codex

1. No reference may be added unless Codex can verify title, authors, venue/year, and relevance.
2. Do not cite a paper for a claim it does not make.
3. Do not cite conformal-prediction papers to support k-NN stability theorems.
4. Do not cite poisoning papers to imply replacement robustness is the same as poisoning robustness.
5. Prefer primary sources over Wikipedia or secondary pages.
6. If using arXiv-only papers, mark them as arXiv preprints unless published.
7. Keep reference style consistent with the final Springer template.
8. Use `refs.bib` as the single source; do not hand-type reference lists.
