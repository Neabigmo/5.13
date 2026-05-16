# Machine Learning journal submission plan

Target journal: *Machine Learning* (Springer). This plan prepares a Springer Nature-style submission folder, but Codex must verify the latest journal-specific instructions from the official Springer page immediately before submission.

Official pages to verify manually in browser before final upload:

- `https://link.springer.com/journal/10994`
- `https://link.springer.com/journal/10994/aims-and-scope`
- `https://link.springer.com/journal/10994/how-to-publish-with-us`
- `https://link.springer.com/journal/10994/submission-guidelines`
- `https://www.springernature.com/gp/authors/campaigns/latex-author-support`

---

## 1. Fit assessment

The manuscript is a plausible fit for *Machine Learning* if framed as:

```text
a finite-sample perturbation semantics and stability analysis for deterministic nearest-neighbor learning.
```

It should not be framed as a broad local-learning-rule theory unless the DLVR/general local-rule results are made formal.

Why it fits:

- it studies a classical ML algorithm;
- it contributes to learning-theoretic stability semantics;
- it combines exact finite-sample theory with reproducible experiments;
- it clarifies how a widely used validation diagnostic should and should not be interpreted.

Risk factors:

- contribution may look narrow if experiments remain thin;
- if the code/paper insert-one mismatch remains, reviewers can reject on rigor;
- if figures look like posters or are placed after references, the manuscript looks unpolished;
- if hierarchy rows lack explicit counterexamples, the theory looks overextended.

---

## 2. Required submission folder contents

This `submit/` folder contains a recommended structure:

```text
submit/
├── manuscript/
│   ├── main.tex
│   ├── refs.bib
│   ├── declarations.tex
│   ├── sections/
│   ├── figures/
│   └── tables/
├── supplementary/
│   ├── README.md
│   ├── environment.yml
│   ├── RUN_EXPERIMENTS.md
│   └── reproducibility_checklist.md
├── editorial/
│   ├── cover_letter.md
│   ├── submission_checklist.md
│   ├── data_code_availability.md
│   └── suggested_reviewers.md
└── codex_docs/
```

Codex should copy or port the final paper into `submit/manuscript/` only after all tests and experiments are complete.

---

## 3. Springer Nature format notes

The included `manuscript/main.tex` is a Springer Nature `sn-jnl` skeleton. It is not a substitute for downloading the latest official template. Before final submission, Codex should:

1. download the latest Springer Nature LaTeX template;
2. copy `sn-jnl.cls` and any required `.bst` files into `submit/manuscript/` if allowed by the template license;
3. select the bibliography style recommended for *Machine Learning*;
4. compile locally from a clean directory;
5. upload both PDF and source files as required by Editorial Manager.

If the final journal instructions prefer a Word template or a different LaTeX format, adapt the folder accordingly.

---

## 4. Declarations to prepare

Prepare these statements in `declarations.tex`:

- Funding: state grants or `The authors received no specific funding for this work.`
- Competing interests: state none if true.
- Data availability: all generated data and public datasets.
- Code availability: GitHub repository URL and archived DOI if available.
- Author contributions: fill in author names.
- Ethics approval: `Not applicable` for public/synthetic data, if true.
- Consent to participate/publish: `Not applicable`, if true.
- Generative AI use: disclose if AI tools were used for editing, coding assistance, or figure drafting, according to current Springer policy.

Do not invent statements; use placeholders where user input is required.

---

## 5. Cover letter angle

The cover letter should not repeat the abstract. It should say why *Machine Learning* readers care:

- k-NN is a canonical local learning rule;
- LOO is historically important for nearest-neighbor methods and validation;
- stability language is often used across learning theory and practice;
- this paper gives an exact finite-sample boundary for what LOO can certify.

Avoid claiming practical robustness improvements unless the paper includes an algorithmic mitigation.

---

## 6. Final pre-upload checklist

Before upload:

```bash
cd submit/manuscript
latexmk -pdf -interaction=nonstopmode main.tex
```

Then verify:

- PDF title and author metadata are correct.
- All figures appear before references or in appendices intentionally.
- No overfull hboxes in important display areas.
- All references are cited.
- No cited reference is missing from `refs.bib`.
- No uncited reference remains unless allowed.
- Figures are vector PDF or high-resolution PNG.
- Supplementary code package includes environment and commands.
- Declarations are complete.
- Cover letter is plain text/PDF as required by the portal.
