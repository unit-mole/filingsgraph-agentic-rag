from __future__ import annotations
import subprocess
import sys


def main():
    modules = [
        ["scripts.evaluate_retrieval", "--split", "dev"],
        ["scripts.evaluate_retrieval", "--split", "test"],
        ["scripts.evaluate_financial"],
        ["scripts.evaluate_temporal"],
        ["scripts.evaluate_graph"],
        ["scripts.evaluate_agent"],
        ["scripts.evaluate_grounding"],
        ["scripts.ablate_graph"],
        ["scripts.ablate_structured"],
        ["scripts.evaluate_system"],
        ["scripts.build_ablation_table"],
        ["scripts.export_failure_analysis"],
    ]
    for spec in modules:
        print("\n===", " ".join(spec), "===")
        r = subprocess.run([sys.executable, "-m", *spec])
        if r.returncode:
            raise SystemExit(r.returncode)


if __name__ == "__main__":
    main()
