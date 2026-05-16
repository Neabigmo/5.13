# Supplementary material README

This supplement should contain the code, configuration, raw outputs, and figure-generation scripts needed to reproduce the paper's computational results.

Recommended command after the repository is fixed:

```bash
conda run -n pytorch-clean python experiments/run_all.py \
  --config experiments/configs/ml_main.yaml \
  --output-dir outputs/ml_main \
  --seed 20260516
```

The run should produce:

```text
outputs/ml_main/MANIFEST.json
outputs/ml_main/raw/
outputs/ml_main/tables/
outputs/ml_main/figures/
```

The manifest must record the git commit, Python version, dependency versions, random seed root, generated files, and checksums.
