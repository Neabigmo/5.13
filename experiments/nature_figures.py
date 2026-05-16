"""Generate submission figures using the local nature-figure conventions.

The figure contract follows external/nature-skills/skills/nature-figure:
editable SVG is primary, PDF and 300-dpi PNG are secondary exports, and every
panel carries a distinct piece of manuscript evidence.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


PALETTE = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "baseline_dark": "#484878",
    "baseline_mid": "#7884B4",
    "baseline_soft": "#B4C0E4",
    "hero_soft": "#F0C0CC",
    "hero_base": "#E4CCD8",
    "delta_up": "#2E9E44",
    "delta_down": "#B64342",
    "neutral_light": "#D8D8D8",
    "neutral_mid": "#767676",
    "neutral_dark": "#4D4D4D",
    "neutral_black": "#272727",
    "gold": "#E6B450",
    "teal": "#42949E",
}


def setup_matplotlib():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Mandatory nature-figure SVG text rules.
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
    plt.rcParams["svg.fonttype"] = "none"
    plt.rcParams.update(
        {
            "pdf.fonttype": 42,
            "font.size": 7.5,
            "axes.spines.right": False,
            "axes.spines.top": False,
            "axes.linewidth": 0.8,
            "legend.frameon": False,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.bbox": "tight",
        }
    )
    return plt


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_pub(fig, stem: Path) -> None:
    stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(stem.with_suffix(".svg"))
    fig.savefig(stem.with_suffix(".pdf"))
    fig.savefig(stem.with_suffix(".png"), dpi=300)


def add_panel_label(ax, label: str, x: float = -0.08, y: float = 1.04) -> None:
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        fontsize=9,
        fontweight="bold",
        ha="left",
        va="bottom",
        color=PALETTE["neutral_black"],
    )


def quiet_ax(ax) -> None:
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def draw_token(ax, x: float, y: float, text: str, color: str, width: float = 0.22) -> None:
    import matplotlib.patches as patches

    rect = patches.FancyBboxPatch(
        (x - width / 2, y - 0.055),
        width,
        0.11,
        boxstyle="round,pad=0.015,rounding_size=0.015",
        linewidth=0.7,
        edgecolor=PALETTE["neutral_dark"],
        facecolor=color,
    )
    ax.add_patch(rect)
    ax.text(x, y, text, ha="center", va="center", fontsize=6.7)


def figure_perturbation_semantics(output_dir: Path, captions: list[str]) -> None:
    """Schematic: LOO couples deletion and evaluation; replace-one decouples both."""
    plt = setup_matplotlib()
    fig = plt.figure(figsize=(7.2, 3.7))
    gs = fig.add_gridspec(2, 3, width_ratios=[1.0, 1.0, 1.0], height_ratios=[1.0, 1.0])
    axes = [fig.add_subplot(gs[i, j]) for i in range(2) for j in range(3)]
    titles = [
        "Original sample",
        "LOO: delete and evaluate same occurrence",
        "Replace-one: arbitrary replacement, arbitrary query",
        "Operation",
        "Evaluation point",
        "What LOO cannot certify",
    ]
    for ax, title, label in zip(axes, titles, list("abcdef")):
        quiet_ax(ax)
        add_panel_label(ax, label)
        ax.set_title(title, fontsize=8, pad=4)

    ax = axes[0]
    for i, token in enumerate(["(a,0)", "(b,0)", "(c,1)"]):
        draw_token(ax, 0.22 + i * 0.25, 0.55, token, PALETTE["neutral_light"])

    ax = axes[1]
    draw_token(ax, 0.22, 0.60, "(a,0)", "#FFE5E0")
    draw_token(ax, 0.50, 0.60, "(b,0)", PALETTE["neutral_light"])
    draw_token(ax, 0.78, 0.60, "(c,1)", PALETTE["neutral_light"])
    ax.annotate("", xy=(0.22, 0.28), xytext=(0.22, 0.50), arrowprops={"arrowstyle": "->", "lw": 1.2})
    ax.text(0.22, 0.20, "query = deleted occurrence", ha="center", fontsize=6.5)

    ax = axes[2]
    draw_token(ax, 0.22, 0.60, "(a,1)", PALETTE["hero_base"])
    draw_token(ax, 0.50, 0.60, "(b,0)", PALETTE["neutral_light"])
    draw_token(ax, 0.78, 0.60, "(c,1)", PALETTE["neutral_light"])
    ax.annotate("", xy=(0.70, 0.28), xytext=(0.22, 0.50), arrowprops={"arrowstyle": "->", "lw": 1.2})
    ax.text(0.70, 0.20, "query chosen independently", ha="center", fontsize=6.5)

    ax = axes[3]
    ax.text(0.50, 0.62, "delete-one", ha="center", fontsize=8, color=PALETTE["blue_main"], fontweight="bold")
    ax.text(0.50, 0.38, "insert-one", ha="center", fontsize=8, color=PALETTE["teal"], fontweight="bold")
    ax.text(0.50, 0.16, "replace-one = delete + insert", ha="center", fontsize=6.8)

    ax = axes[4]
    ax.plot([0.15, 0.85], [0.52, 0.52], color=PALETTE["neutral_mid"], lw=1.2)
    ax.scatter([0.22, 0.70], [0.52, 0.52], s=[70, 70], color=[PALETTE["blue_main"], PALETTE["delta_down"]])
    ax.text(0.22, 0.30, "LOO", ha="center", fontsize=7)
    ax.text(0.70, 0.30, "worst-case query", ha="center", fontsize=7)

    ax = axes[5]
    ax.text(0.5, 0.62, "zero LOO", ha="center", fontsize=9, color=PALETTE["blue_main"], fontweight="bold")
    ax.text(0.5, 0.40, "does not imply", ha="center", fontsize=7)
    ax.text(0.5, 0.20, "zero replace-one", ha="center", fontsize=9, color=PALETTE["delta_down"], fontweight="bold")

    fig.suptitle("Perturbation operation and evaluation point are separate choices", fontsize=10)
    fig.tight_layout()
    save_pub(fig, output_dir / "fig1_perturbation_semantics")
    plt.close(fig)
    captions.append("Figure 1. Perturbation semantics. LOO couples deletion to evaluation at the deleted occurrence, whereas replace-one decouples both the edited occurrence and the evaluation query.")


def figure_margin_mechanism(output_dir: Path, captions: list[str]) -> None:
    """Schematic of the signed-margin crossing for odd and even k."""
    plt = setup_matplotlib()
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=True)
    transitions = [("Odd k", -1, 1, "strict majority crosses zero"), ("Even k", 0, 2, "tie-breaking threshold crosses")]
    for ax, (title, before, after, note), label in zip(axes, transitions, "ab"):
        add_panel_label(ax, label)
        ax.axhline(0, color=PALETTE["neutral_mid"], lw=0.9, ls="--")
        ax.plot([0, 1], [before, after], color=PALETTE["delta_down"], lw=2.0, marker="o")
        ax.scatter([0], [before], s=60, color=PALETTE["blue_main"], zorder=3, label="original")
        ax.scatter([1], [after], s=60, color=PALETTE["delta_down"], zorder=3, label="after replacement")
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["before", "after"])
        ax.set_ylim(-3.1, 3.1)
        ax.set_title(title, fontsize=8)
        ax.set_ylabel("signed top-k margin" if label == "a" else "")
        ax.text(0.5, -2.55, note, ha="center", fontsize=6.5)
    axes[1].legend(loc="upper left", fontsize=6.2)
    fig.suptitle("Replacement instability is a margin-crossing event", fontsize=10)
    fig.tight_layout()
    save_pub(fig, output_dir / "fig2_margin_crossing")
    plt.close(fig)
    captions.append("Figure 2. Margin mechanism. The constructive separations move the signed top-k vote margin from -1 to +1 for odd k and from 0 to +2 for even k under deterministic tie-breaking.")


def grouped_mean(records: list[dict[str, Any]], keys: tuple[str, ...], value: str) -> dict[tuple[Any, ...], float]:
    grouped: dict[tuple[Any, ...], list[float]] = {}
    for record in records:
        grouped.setdefault(tuple(record[k] for k in keys), []).append(float(record[value]))
    return {key: float(np.mean(vals)) for key, vals in grouped.items()}


def figure_synthetic(output_dir: Path, synthetic_payload: dict[str, Any], captions: list[str]) -> None:
    plt = setup_matplotlib()
    agg = synthetic_payload.get("aggregates", [])
    filtered = [
        r
        for r in agg
        if r.get("conflict_ratio") == 0.0
        and r.get("noise_ratio") == 0.0
        and r.get("n_vertices") == min(a.get("n_vertices", 0) for a in agg)
    ] or agg
    k_values = sorted({int(r["k"]) for r in filtered})
    dup_values = sorted({float(r["duplicate_ratio"]) for r in filtered})
    sep = np.full((len(k_values), len(dup_values)), np.nan)
    vuln = np.full_like(sep, np.nan)
    for r in filtered:
        i = k_values.index(int(r["k"]))
        j = dup_values.index(float(r["duplicate_ratio"]))
        sep[i, j] = float(r["separation_frequency"])
        vuln[i, j] = float(r.get("mean_vulnerable_query_rate", 0.0))

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1))
    for ax, matrix, title, cmap, label in [
        (axes[0], sep, "Strict separation frequency", "Reds", "a"),
        (axes[1], vuln, "Vulnerable-query rate", "Blues", "b"),
    ]:
        add_panel_label(ax, label)
        im = ax.imshow(matrix, aspect="auto", cmap=cmap, vmin=0, vmax=1)
        ax.set_xticks(range(len(dup_values)))
        ax.set_xticklabels([f"{d:.1f}" for d in dup_values])
        ax.set_yticks(range(len(k_values)))
        ax.set_yticklabels([str(k) for k in k_values])
        ax.set_xlabel("duplicate ratio")
        ax.set_ylabel("k")
        ax.set_title(title, fontsize=8)
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if not np.isnan(matrix[i, j]):
                    ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", fontsize=6.2)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    fig.suptitle("Synthetic graph metrics: duplicates expose the LOO/replace-one gap", fontsize=10)
    fig.tight_layout()
    save_pub(fig, output_dir / "fig3_synthetic_results")
    plt.close(fig)
    captions.append("Figure 3. Synthetic graph-metric benchmark. Separation frequency and vulnerable-query rate are computed from the full reproducible benchmark aggregates.")


def figure_tabular(output_dir: Path, tabular_payload: dict[str, Any], captions: list[str]) -> None:
    plt = setup_matplotlib()
    agg = tabular_payload.get("aggregates", [])
    datasets = sorted({r["dataset"] for r in agg})
    k_values = sorted({int(r["k"]) for r in agg})
    pretty = {
        "iris": "Iris",
        "wine": "Wine",
        "breast_cancer": "Breast cancer",
        "digits": "Digits",
    }
    x = np.arange(len(datasets))
    width = 0.78 / max(len(k_values), 1)
    colors = [PALETTE["baseline_dark"], PALETTE["baseline_mid"], PALETTE["hero_base"], PALETTE["hero_soft"]]

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.2), sharex=True)
    for ax, metric, ci_key, title, ylabel, label in [
        (axes[0], "separation_frequency", "separation_ci", "LOO-stable but replace-one-unstable", "frequency", "a"),
        (axes[1], "mean_vulnerable_query_rate", "vuln_rate_ci", "Queries within |margin| <= 2", "rate", "b"),
    ]:
        add_panel_label(ax, label)
        for idx, k in enumerate(k_values):
            means = []
            cis = []
            for ds in datasets:
                rows = [r for r in agg if r["dataset"] == ds and int(r["k"]) == k]
                means.append(float(rows[0].get(metric, 0.0)) if rows else 0.0)
                cis.append(float(rows[0].get(ci_key, 0.0)) if rows else 0.0)
            ax.bar(
                x + (idx - (len(k_values) - 1) / 2) * width,
                means,
                width=width,
                yerr=cis,
                capsize=2,
                color=colors[idx % len(colors)],
                edgecolor="white",
                linewidth=0.5,
                label=f"k={k}",
            )
        ax.set_ylim(0, 1.08)
        ax.set_ylabel(ylabel)
        ax.set_title(title, fontsize=8)
        ax.set_xticks(x)
        ax.set_xticklabels([pretty.get(ds, ds) for ds in datasets], rotation=25, ha="right")
    axes[1].legend(loc="upper right", fontsize=6.3, ncol=2)
    fig.suptitle("Tabular data: LOO evidence and replacement robustness separate empirically", fontsize=10)
    fig.tight_layout()
    save_pub(fig, output_dir / "fig4_tabular_results")
    plt.close(fig)
    captions.append("Figure 4. Tabular benchmark. Separation frequency and vulnerable-query rate are summarized across the UCI-style binary tabular datasets with 95% confidence intervals.")


def figure_hierarchy(output_dir: Path, captions: list[str]) -> None:
    plt = setup_matplotlib()
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    quiet_ax(ax)
    nodes = {
        "delete": (0.18, 0.66, "pointwise\ndelete-one"),
        "loo": (0.18, 0.30, "LOO"),
        "insert": (0.50, 0.66, "uniform\ninsert-one"),
        "replace": (0.82, 0.66, "uniform\nreplace-one"),
        "counter": (0.82, 0.30, "pointwise\nreplace-one"),
    }
    for key, (x, y, text) in nodes.items():
        color = PALETTE["neutral_light"] if key != "counter" else PALETTE["hero_base"]
        draw_token(ax, x, y, text, color, width=0.24)
    ax.annotate("", xy=(0.18, 0.40), xytext=(0.18, 0.56), arrowprops={"arrowstyle": "->", "lw": 1.2})
    ax.annotate("", xy=(0.72, 0.66), xytext=(0.60, 0.66), arrowprops={"arrowstyle": "->", "lw": 1.2})
    ax.plot([0.30, 0.42], [0.66, 0.66], color="black", lw=1.2)
    ax.text(0.36, 0.70, "+", ha="center", va="center", fontsize=11)
    ax.plot([0.28, 0.72], [0.30, 0.30], color=PALETTE["delta_down"], lw=1.5, ls="--")
    ax.text(0.50, 0.23, "no implication: explicit k-NN separations", ha="center", fontsize=7, color=PALETTE["delta_down"])
    ax.text(0.50, 0.88, "The hierarchy is about operations and evaluation points, not one scalar notion of stability.", ha="center", fontsize=8)
    fig.tight_layout()
    save_pub(fig, output_dir / "fig5_stability_hierarchy")
    plt.close(fig)
    captions.append("Figure 5. Stability hierarchy. Uniform replace-one can be bounded through delete-one plus insert-one, but pointwise LOO does not control pointwise replace-one.")


def write_captions(output_dir: Path, captions: list[str]) -> None:
    (output_dir / "captions.md").write_text(
        "# Figure Captions\n\n" + "\n\n".join(f"- {caption}" for caption in captions) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Nature-style manuscript figures.")
    parser.add_argument("--synthetic_json", type=Path, required=True)
    parser.add_argument("--tabular_json", type=Path, required=True)
    parser.add_argument("--output_dir", type=Path, default=ROOT / "outputs" / "figures")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    captions: list[str] = []
    synthetic_payload = load_json(args.synthetic_json)
    tabular_payload = load_json(args.tabular_json)

    figure_perturbation_semantics(args.output_dir, captions)
    figure_margin_mechanism(args.output_dir, captions)
    figure_synthetic(args.output_dir, synthetic_payload, captions)
    figure_tabular(args.output_dir, tabular_payload, captions)
    figure_hierarchy(args.output_dir, captions)
    write_captions(args.output_dir, captions)
    print(f"Generated Nature-style figures in {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
