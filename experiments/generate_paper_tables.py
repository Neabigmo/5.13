"""Generate LaTeX tables for the paper draft."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def tex_escape(value: object) -> str:
    text = str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "_": r"\_",
        "%": r"\%",
        "&": r"\&",
        "#": r"\#",
        "{": r"\{",
        "}": r"\}",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def write_table(path: Path, columns: list[str], rows: list[list[object]], note: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\small",
        r"\begin{tabular}{%s}" % ("l" * len(columns)),
        r"\toprule",
        " & ".join(tex_escape(col) for col in columns) + r" \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(" & ".join(tex_escape(cell) for cell in row) + r" \\")
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    if note:
        lines.append(r"\caption*{\footnotesize " + tex_escape(note) + "}")
    lines.append(r"\end{table}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_stability_notions_table(output_dir: Path) -> None:
    columns = ["Notion", "Perturbation", "Evaluated at", "Supremum over", "Distribution?", "Used for"]
    rows = [
        ["delete-one", "remove one occurrence", "arbitrary query-label pair", "indices and queries", "no", "uniform/pointwise perturbation analysis"],
        ["replace-one", "swap one occurrence for adversarial labeled point", "arbitrary query-label pair", "indices, replacements, queries", "no", "strong local perturbation control"],
        ["add-one", "append one occurrence", "arbitrary query-label pair", "added points and queries", "no", "decomposition of replace-one"],
        ["LOO", "delete one occurrence", "that deleted occurrence", "delete index only", "no", "cross-validation style local stability"],
        ["uniform stability", "usually replace-one in classical literature", "fresh test point or worst-case query", "all samples", "often yes", "generalization bounds"],
    ]
    write_table(
        output_dir / "stability_notions.tex",
        columns,
        rows,
        note="Computational witness sections use fixed-sample worst-case indicators, not distributional expected stability.",
    )


def build_minimal_witnesses_table(output_dir: Path, tie_free_payload: dict) -> None:
    rows = []
    seen = set()
    for witness in tie_free_payload["witnesses"]:
        key = (tuple(witness["sample_order"]), tuple(witness["labels"]))
        if witness["num_vertices"] != 2 or key in seen:
            continue
        seen.add(key)
        rows.append(
            [
                witness["num_vertices"],
                witness["num_edges"],
                f"order={witness['sample_order']}; labels={witness['labels']}",
                1,
                witness["loo_max"],
                witness["replace_max"],
                "explicit witness; certificate-level minimality only",
            ]
        )
    write_table(
        output_dir / "minimal_witnesses.tex",
        ["Vertices", "Edges", "Sample", "k", "max LOO", "max replace-one", "Status"],
        rows,
        note="The witness row is hand-checkable, while minimality over the search space remains computational evidence.",
    )


def build_k_gadget_candidates_table(output_dir: Path, gadget_payload: dict) -> None:
    rows = []
    grouped = {}
    for candidate in gadget_payload["candidates"]:
        grouped.setdefault(candidate["k"], candidate)
    for k in sorted(grouped):
        candidate = grouped[k]
        rows.append(
            [
                k,
                candidate["num_vertices"],
                candidate["sample_length"],
                candidate["loo_max"],
                candidate["replace_max"],
                "computational candidate only",
                "experiments/search_k_gadgets.py",
            ]
        )
    write_table(
        output_dir / "k_gadget_candidates.tex",
        ["k", "vertices", "sample size", "max LOO", "max replace-one", "status", "script"],
        rows,
        note="Odd-k rows summarize one representative candidate per k and are not theorem statements.",
    )


def build_certificate_summary_table(output_dir: Path, certificate_payload: dict) -> None:
    rows = [
        [
            "TASK-007",
            certificate_payload["observed_minimal_vertex_counts"]["task_007"],
            certificate_payload["observed_no_solution_ranges"]["task_007"],
            certificate_payload["source_outputs"]["task_007"]["sha256"][:12] + "...",
            "computational evidence only",
        ],
        [
            "TASK-008",
            certificate_payload["observed_minimal_vertex_counts"]["task_008"],
            certificate_payload["observed_no_solution_ranges"]["task_008"],
            certificate_payload["source_outputs"]["task_008"]["sha256"][:12] + "...",
            "computational evidence only",
        ],
    ]
    write_table(
        output_dir / "certificate_summary.tex",
        ["Artifact", "Observed min vertices", "No-solution range", "Hash", "Status"],
        rows,
        note="Certificate tables summarize finite search outputs and do not upgrade them to proof.",
    )


def build_reproducibility_summary_table(output_dir: Path, reproducibility_md: str) -> None:
    commands = re.findall(r"```powershell\n(.*?)\n```", reproducibility_md, flags=re.S)
    rows = [
        ["tests", "python -m pytest", commands[0].strip(), "see REPRODUCIBILITY.md", "passed"],
        ["minimal 1-NN search", "search_minimal_1nn.py", commands[1].strip(), "5B7A8925688A...", "generated"],
        ["tie-free search", "search_tie_free.py", commands[2].strip(), "A52AA8A77A9A...", "generated"],
        ["minimality certificate", "certify_minimality.py", commands[3].strip(), "92F85B16F79D...", "generated"],
        ["k-gadget search", "search_k_gadgets.py", commands[4].strip(), "B3204D99A02A...", "generated"],
    ]
    write_table(
        output_dir / "reproducibility_summary.tex",
        ["Artifact", "Script", "Command", "Output hash", "Status"],
        rows,
        note="Full commands and environment details are listed in outputs/REPRODUCIBILITY.md.",
    )


def build_related_work_map(output_dir: Path, lit_table_md: str) -> None:
    lines = [line for line in lit_table_md.splitlines() if line.startswith("|")][2:]
    rows = []
    for line in lines[:8]:
        parts = [part.strip() for part in line.strip("|").split("|")]
        rows.append([parts[0], parts[3], parts[4], parts[5], "yes" if "NN" in parts[0] or "Neighbor" in parts[0] else "no", parts[6]])
    write_table(
        output_dir / "related_work_map.tex",
        ["Work", "Perturbation", "Evaluation point", "Guarantee type", "k-NN?", "Relation to this paper"],
        rows,
        note="This map is a condensed companion to docs/literature/LIT_TABLE.md.",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate LaTeX tables for the paper draft.")
    parser.add_argument("--output_dir", type=Path, default=ROOT / "outputs" / "tables")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    tie_free_payload = load_json(ROOT / "outputs" / "witnesses" / "1nn_tie_free_witnesses.json")
    gadget_payload = load_json(ROOT / "outputs" / "witnesses" / "k_gadget_candidates.json")
    certificate_payload = load_json(ROOT / "outputs" / "witnesses" / "1nn_minimality_certificate.json")
    reproducibility_md = (ROOT / "outputs" / "REPRODUCIBILITY.md").read_text(encoding="utf-8")
    lit_table_md = (ROOT / "docs" / "literature" / "LIT_TABLE.md").read_text(encoding="utf-8")

    build_stability_notions_table(args.output_dir)
    build_minimal_witnesses_table(args.output_dir, tie_free_payload)
    build_k_gadget_candidates_table(args.output_dir, gadget_payload)
    build_certificate_summary_table(args.output_dir, certificate_payload)
    build_reproducibility_summary_table(args.output_dir, reproducibility_md)
    build_related_work_map(args.output_dir, lit_table_md)

    print(f"Generated tables in {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
