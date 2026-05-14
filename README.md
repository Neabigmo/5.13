# k-NN Stability Calculus

Working paper project:

**A Stability Calculus for Local Learning Rules: Delete-One, Replace-One, and Leave-One-Out Characterizations for k-Nearest Neighbors**

This repository studies deterministic finite-sample perturbation notions for
local learning rules, with k-nearest neighbors as the main example. The current
goal is a reproducible, submission-oriented paper package with clear boundaries
between theorem statements, computational certificates, conjectures, and
discussion claims.

Computational witnesses in this repository are **not proofs** unless the paper
explicitly upgrades a statement after Codex proof audit.

## Main Locations

- `paper/`: LaTeX draft
- `src/knn_stability/`: core deterministic k-NN and stability code
- `experiments/`: witness, certificate, figure, and table scripts
- `outputs/witnesses/`: computational witness and certificate JSON files
- `outputs/figures/`: generated paper figures
- `outputs/tables/`: generated LaTeX tables
- `outputs/REPRODUCIBILITY.md`: environment, commands, logs, and hashes
- `docs/literature/`: novelty gate and literature mapping
- `docs/proof-notes/`: claim registry and proof-note boundary documents
- `tasks/`: active and completed execution tasks

## Environment

Use the existing environment and preferred LaTeX installation:

```powershell
E:\anaconda3\envs\pytorch-clean\python.exe -V
E:\anaconda3\envs\pytorch-clean\python.exe -m pytest
D:\texlive\2025\bin\windows\latexmk.exe -pdf -output-directory=paper paper\main.tex
```

If a command later needs network access, set:

```powershell
$env:HTTP_PROXY = "http://127.0.0.1:7897"
$env:HTTPS_PROXY = "http://127.0.0.1:7897"
$env:ALL_PROXY = "socks5://127.0.0.1:7897"
```

## Reproduce Current Artifacts

Run tests:

```powershell
E:\anaconda3\envs\pytorch-clean\python.exe -m pytest
```

Regenerate witness and certificate artifacts:

```powershell
E:\anaconda3\envs\pytorch-clean\python.exe experiments\search_minimal_1nn.py --max_vertices 4
E:\anaconda3\envs\pytorch-clean\python.exe experiments\search_tie_free.py --input outputs\witnesses\1nn_separation_witnesses.json --output outputs\witnesses\1nn_tie_free_witnesses.json
E:\anaconda3\envs\pytorch-clean\python.exe experiments\certify_minimality.py --separation outputs\witnesses\1nn_separation_witnesses.json --tie_free outputs\witnesses\1nn_tie_free_witnesses.json --json_output outputs\witnesses\1nn_minimality_certificate.json --markdown_output outputs\tables\1nn_minimality_certificate.md
E:\anaconda3\envs\pytorch-clean\python.exe experiments\search_k_gadgets.py --k_values 3 5 7 --min_vertices 2 --max_vertices 2 --length_modes equal_k --max_candidates_per_k 3
```

Generate paper figures and tables:

```powershell
E:\anaconda3\envs\pytorch-clean\python.exe experiments\generate_paper_figures.py
E:\anaconda3\envs\pytorch-clean\python.exe experiments\generate_paper_tables.py
```

Build the paper:

```powershell
D:\texlive\2025\bin\windows\latexmk.exe -pdf -output-directory=paper paper\main.tex
```

## Coordination Model

- Codex owns definitions, proofs, novelty assessment, and final integration.
- Claude Code only receives bounded task cards and must not redefine
  mathematical concepts.
- Task state is tracked in `tasks/TASK_INDEX.md`.

## Reproducibility Notes

See [outputs/REPRODUCIBILITY.md](/H:/2026try/5.13/outputs/REPRODUCIBILITY.md)
for logs, hashes, and the exact current artifact-generation baseline.
