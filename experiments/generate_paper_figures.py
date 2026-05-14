"""Generate publication-oriented figures for the paper draft."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def setup_matplotlib():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.titlesize": 12,
            "figure.titlesize": 14,
            "axes.labelsize": 10,
            "savefig.bbox": "tight",
        }
    )
    return plt


def save_triplet(fig, stem: Path) -> None:
    fig.savefig(stem.with_suffix(".pdf"))
    fig.savefig(stem.with_suffix(".svg"))
    fig.savefig(stem.with_suffix(".png"), dpi=200)


def draw_occurrences(ax, sample_order, labels, title, highlight=None):
    ax.set_title(title)
    ax.set_xlim(-0.5, len(sample_order) - 0.5)
    ax.set_ylim(-1.1, 1.1)
    ax.axhline(0, color="#999999", linewidth=1.0, linestyle="--")
    for idx, (point, label) in enumerate(zip(sample_order, labels)):
        face = "#f4f7fb" if highlight != idx else "#ffe9b3"
        edge = "#30475e"
        ax.add_patch(
            __import__("matplotlib").patches.FancyBboxPatch(
                (idx - 0.33, -0.35),
                0.66,
                0.7,
                boxstyle="round,pad=0.03,rounding_size=0.05",
                linewidth=1.5,
                edgecolor=edge,
                facecolor=face,
            )
        )
        ax.text(idx, 0.16, f"x={point}", ha="center", va="center", fontsize=9)
        ax.text(idx, -0.12, f"y={label}", ha="center", va="center", fontsize=9)
        ax.text(idx, -0.75, f"#{idx}", ha="center", va="center", fontsize=8, color="#666666")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def draw_graph_metric(ax, adjacency_list, labels, title):
    import matplotlib.pyplot as plt

    vertices = sorted(int(v) for v in adjacency_list)
    if len(vertices) == 2:
        positions = {vertices[0]: (-0.8, 0.0), vertices[1]: (0.8, 0.0)}
    else:
        positions = {}
        for i, vertex in enumerate(vertices):
            angle = 2 * math.pi * i / len(vertices)
            positions[vertex] = (math.cos(angle), math.sin(angle))

    for v in vertices:
        for n in adjacency_list[str(v)] if isinstance(next(iter(adjacency_list.keys())), str) else adjacency_list[v]:
            n = int(n)
            if v < n:
                ax.plot(
                    [positions[v][0], positions[n][0]],
                    [positions[v][1], positions[n][1]],
                    color="#4a4a4a",
                    linewidth=1.8,
                    zorder=1,
                )

    for v in vertices:
        x, y = positions[v]
        fill = "#d8eefc" if labels[v] == 0 else "#ffd6d6"
        circ = plt.Circle((x, y), 0.22, facecolor=fill, edgecolor="#1f2937", linewidth=1.8, zorder=2)
        ax.add_patch(circ)
        ax.text(x, y + 0.04, f"{v}", ha="center", va="center", fontsize=11, fontweight="bold")
        ax.text(x, y - 0.13, f"label {labels[v]}", ha="center", va="center", fontsize=8)

    ax.set_title(title)
    ax.set_aspect("equal")
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.0, 1.0)
    ax.axis("off")


def figure_stability_notions(output_dir: Path, captions: list[str]) -> None:
    plt = setup_matplotlib()
    fig, axes = plt.subplots(1, 3, figsize=(14, 3.8))
    panels = [
        ("Delete-one", "delete one occurrence\nthen evaluate arbitrary $(x,y)$"),
        ("Replace-one", "replace one occurrence\nthen evaluate arbitrary $(x,y)$"),
        ("LOO", "delete one occurrence\nthen evaluate that deleted occurrence"),
    ]
    for ax, (title, subtitle) in zip(axes, panels):
        ax.add_patch(
            __import__("matplotlib").patches.FancyBboxPatch(
                (0.08, 0.20),
                0.84,
                0.60,
                boxstyle="round,pad=0.03,rounding_size=0.04",
                transform=ax.transAxes,
                facecolor="#f7fafc",
                edgecolor="#2d3748",
                linewidth=1.6,
            )
        )
        ax.text(0.5, 0.68, title, transform=ax.transAxes, ha="center", va="center", fontsize=12, fontweight="bold")
        ax.text(0.5, 0.43, subtitle, transform=ax.transAxes, ha="center", va="center", fontsize=10)
        ax.axis("off")
    fig.suptitle("Three perturbation notions differ by both operation and evaluation point")
    save_triplet(fig, output_dir / "stability_notions_diagram")
    plt.close(fig)
    captions.append("`stability_notions_diagram`: Three-panel schematic separating delete-one, replace-one, and LOO by both perturbation operation and evaluation point.")


def figure_uniform_calculus(output_dir: Path, captions: list[str]) -> None:
    plt = setup_matplotlib()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.axis("off")
    ax.text(0.18, 0.72, "replace-one", ha="center", va="center", fontsize=13, fontweight="bold", transform=ax.transAxes)
    ax.text(0.56, 0.72, "delete-one + add-one", ha="center", va="center", fontsize=13, fontweight="bold", transform=ax.transAxes)
    ax.annotate("", xy=(0.44, 0.72), xytext=(0.28, 0.72), arrowprops=dict(arrowstyle="->", lw=2.2), xycoords=ax.transAxes)
    ax.text(0.36, 0.78, "uniform bound", ha="center", va="center", fontsize=10, transform=ax.transAxes)
    ax.text(0.18, 0.34, "LOO", ha="center", va="center", fontsize=13, fontweight="bold", transform=ax.transAxes)
    ax.text(0.56, 0.34, "delete-one at deleted occurrence", ha="center", va="center", fontsize=13, fontweight="bold", transform=ax.transAxes)
    ax.annotate("", xy=(0.44, 0.34), xytext=(0.28, 0.34), arrowprops=dict(arrowstyle="->", lw=2.2), xycoords=ax.transAxes)
    ax.text(
        0.5,
        0.08,
        "Uniform relations do not imply that pointwise LOO controls pointwise replace-one.",
        ha="center",
        va="center",
        fontsize=10,
        transform=ax.transAxes,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#fff5f5", edgecolor="#c53030"),
    )
    save_triplet(fig, output_dir / "uniform_calculus_diagram")
    plt.close(fig)
    captions.append("`uniform_calculus_diagram`: Operation-level diagram showing the delete-plus-add decomposition of replace-one and the evaluation-point restriction that makes LOO special.")


def figure_knn_boundary(output_dir: Path, captions: list[str]) -> None:
    plt = setup_matplotlib()
    fig, ax = plt.subplots(figsize=(9, 2.6))
    ax.set_xlim(-0.5, 6.8)
    ax.set_ylim(-1.0, 1.0)
    ax.axis("off")
    ax.text(0.2, 0.55, "query $x$", fontsize=11)
    ax.scatter([1, 2, 3, 4, 5, 6], [0, 0, 0, 0, 0, 0], s=120, c=["#3182ce"] * 3 + ["#e2e8f0"] * 3, edgecolors="#1f2937")
    for idx in range(1, 7):
        ax.text(idx, -0.25, f"$\\pi_S^x({idx})$", ha="center", fontsize=9)
    ax.axvline(3.5, ymin=0.18, ymax=0.82, color="#c53030", linestyle="--", linewidth=2)
    ax.text(3.5, 0.55, "top-$k$ boundary", color="#c53030", ha="center", fontsize=10)
    ax.text(2.0, 0.32, "inside top-$k$", ha="center", fontsize=10)
    ax.text(5.2, 0.32, "outside top-$k$", ha="center", fontsize=10)
    save_triplet(fig, output_dir / "knn_topk_boundary")
    plt.close(fig)
    captions.append("`knn_topk_boundary`: Ordered neighbor list around a query, highlighting the top-k prefix and the boundary across which deletions or insertions can change the signed margin.")


def figure_knn_variants(output_dir: Path, captions: list[str]) -> None:
    plt = setup_matplotlib()
    variants = [
        ("knn_topk_stable_deletion", "Outside-top-k deletion leaves the top-k vote unchanged"),
        ("knn_topk_margin_flip", "Removing an in-top-k occurrence can expose a new boundary neighbor"),
        ("knn_replace_one_insertion_flip", "Replace-one can swap label mass across the top-k threshold"),
    ]
    for filename, title in variants:
        fig, ax = plt.subplots(figsize=(7, 2.6))
        ax.axis("off")
        ax.text(0.5, 0.74, title, ha="center", transform=ax.transAxes, fontsize=12, fontweight="bold")
        ax.text(0.22, 0.34, "before", ha="center", transform=ax.transAxes, fontsize=10)
        ax.text(0.78, 0.34, "after", ha="center", transform=ax.transAxes, fontsize=10)
        ax.annotate("", xy=(0.62, 0.5), xytext=(0.38, 0.5), arrowprops=dict(arrowstyle="->", lw=2), xycoords=ax.transAxes)
        ax.add_patch(__import__("matplotlib").patches.Rectangle((0.08, 0.22), 0.22, 0.18, transform=ax.transAxes, facecolor="#d8eefc", edgecolor="#1f2937"))
        ax.add_patch(__import__("matplotlib").patches.Rectangle((0.70, 0.22), 0.22, 0.18, transform=ax.transAxes, facecolor="#ffd6d6", edgecolor="#1f2937"))
        save_triplet(fig, output_dir / filename)
        plt.close(fig)
    captions.append("`knn_topk_stable_deletion`, `knn_topk_margin_flip`, and `knn_replace_one_insertion_flip`: schematic variants for the perturbation criterion discussion.")


def figure_minimal_witness(output_dir: Path, captions: list[str]) -> None:
    plt = setup_matplotlib()
    fig, axes = plt.subplots(2, 2, figsize=(10, 6))
    before_sample = ([0, 1], [0, 0])
    after_sample = ([0, 1], [1, 0])
    draw_graph_metric(axes[0, 0], {"0": [1], "1": [0]}, [0, 0], "Graph metric")
    draw_occurrences(axes[0, 1], before_sample[0], before_sample[1], "Original sample $S$", highlight=0)
    draw_occurrences(axes[1, 0], after_sample[0], after_sample[1], "Replace-one sample $S^{0\\leftarrow(a,1)}$", highlight=0)
    axes[1, 1].axis("off")
    axes[1, 1].text(0.1, 0.78, "At query $a$ with evaluation label $0$:", fontsize=11, fontweight="bold", transform=axes[1, 1].transAxes)
    axes[1, 1].text(0.1, 0.56, "Original 1-NN prediction: $0$", fontsize=10, transform=axes[1, 1].transAxes)
    axes[1, 1].text(0.1, 0.40, "After replace-one: $1$", fontsize=10, transform=axes[1, 1].transAxes)
    axes[1, 1].text(0.1, 0.24, "LOO maximum remains $0$ on this sample.", fontsize=10, transform=axes[1, 1].transAxes)
    axes[1, 1].text(
        0.1,
        0.08,
        "This is an explicit witness, not a theorem of minimality.",
        fontsize=10,
        color="#9b2c2c",
        transform=axes[1, 1].transAxes,
    )
    fig.suptitle("Minimal 1-NN separation witness")
    save_triplet(fig, output_dir / "minimal_1nn_witness_before_after")
    plt.close(fig)
    captions.append("`minimal_1nn_witness_before_after`: The two-point graph witness and its adversarial replace-one perturbation, showing unchanged LOO but flipped replace-one loss.")


def figure_tie_breaking(output_dir: Path, captions: list[str]) -> None:
    plt = setup_matplotlib()
    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.axis("off")
    ax.scatter([0.2, 0.5, 0.8], [0.5, 0.5, 0.5], s=[80, 120, 120], c=["#4a5568", "#d8eefc", "#ffd6d6"], edgecolors="#1f2937")
    ax.text(0.2, 0.62, "query", ha="center", transform=ax.transAxes)
    ax.text(0.5, 0.62, "occurrence #i", ha="center", transform=ax.transAxes)
    ax.text(0.8, 0.62, "occurrence #j", ha="center", transform=ax.transAxes)
    ax.text(0.5, 0.28, "distance ties break by smaller sample index", ha="center", transform=ax.transAxes, fontsize=10)
    ax.text(0.5, 0.12, "label vote ties break toward label 0", ha="center", transform=ax.transAxes, fontsize=10, bbox=dict(boxstyle="round,pad=0.2", facecolor="#f7fafc", edgecolor="#2d3748"))
    save_triplet(fig, output_dir / "tie_breaking_microscope")
    plt.close(fig)
    captions.append("`tie_breaking_microscope`: A close-up reminder that distance ties are resolved by sample index before vote ties are resolved toward label 0.")


def figure_k_gadgets(output_dir: Path, captions: list[str], gadget_payload: dict) -> None:
    plt = setup_matplotlib()
    grouped = {}
    for candidate in gadget_payload["candidates"]:
        grouped.setdefault(candidate["k"], candidate)
    fig, axes = plt.subplots(1, len(grouped), figsize=(4.2 * len(grouped), 4))
    if len(grouped) == 1:
        axes = [axes]
    for ax, k in zip(axes, sorted(grouped)):
        candidate = grouped[k]
        zeros = sum(1 for label in candidate["labels"] if label == 0)
        ones = sum(1 for label in candidate["labels"] if label == 1)
        ax.bar(["label 0", "label 1"], [zeros, ones], color=["#d8eefc", "#ffd6d6"], edgecolor="#1f2937")
        ax.set_title(f"odd k = {k}")
        ax.set_ylabel("occurrences")
        ax.text(0.5, 0.92, "candidate, not proof", transform=ax.transAxes, ha="center", color="#9b2c2c", fontsize=9)
        ax.text(0.5, 0.82, f"LOO={candidate['loo_max']}  Rep={candidate['replace_max']}", transform=ax.transAxes, ha="center", fontsize=9)
    fig.suptitle("Odd-k repeated-occurrence gadget candidates")
    save_triplet(fig, output_dir / "k_gadget_candidates")
    plt.close(fig)
    captions.append("`k_gadget_candidates`: Odd-k repeated-occurrence candidate patterns from deterministic finite search. The figure is explicitly labeled as computational evidence only.")


def figure_regimes_map(output_dir: Path, captions: list[str]) -> None:
    plt = setup_matplotlib()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axis("off")
    layers = [
        ("finite pointwise worst-case", "#fff5f5"),
        ("finite uniform worst-case", "#fefcbf"),
        ("distributional expected stability", "#e6fffa"),
        ("asymptotic consistency", "#ebf8ff"),
    ]
    for idx, (label, color) in enumerate(layers):
        y = 0.12 + idx * 0.18
        ax.add_patch(__import__("matplotlib").patches.FancyBboxPatch((0.18, y), 0.64, 0.12, boxstyle="round,pad=0.02", transform=ax.transAxes, facecolor=color, edgecolor="#2d3748"))
        ax.text(0.5, y + 0.06, label, ha="center", va="center", transform=ax.transAxes, fontsize=11)
    ax.text(0.5, 0.03, "Sections 6 and 7 live near the top; Section 8 explains why the bottom layer is different.", ha="center", transform=ax.transAxes, fontsize=9)
    save_triplet(fig, output_dir / "stability_regimes_map")
    plt.close(fig)
    captions.append("`stability_regimes_map`: Layered view of the paper's regimes, distinguishing finite pointwise effects from uniform, distributional, and asymptotic viewpoints.")


def write_captions(output_dir: Path, captions: list[str]) -> None:
    (output_dir / "captions.md").write_text("# Figure Captions\n\n" + "\n\n".join(f"- {line}" for line in captions) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate publication-oriented paper figures.")
    parser.add_argument("--output_dir", type=Path, default=ROOT / "outputs" / "figures")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    captions: list[str] = []
    gadget_payload = load_json(ROOT / "outputs" / "witnesses" / "k_gadget_candidates.json")

    figure_stability_notions(args.output_dir, captions)
    figure_uniform_calculus(args.output_dir, captions)
    figure_knn_boundary(args.output_dir, captions)
    figure_knn_variants(args.output_dir, captions)
    figure_minimal_witness(args.output_dir, captions)
    figure_tie_breaking(args.output_dir, captions)
    figure_k_gadgets(args.output_dir, captions, gadget_payload)
    figure_regimes_map(args.output_dir, captions)
    write_captions(args.output_dir, captions)

    print(f"Generated paper figures in {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
