from __future__ import annotations

import argparse
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--include-test", action="store_true", help="Run frozen TEST metrics. Do this only after DEV tuning is frozen.")
    args = ap.parse_args()

    modules = [
        ["scripts.evaluate_retrieval", "--split", "dev"],
        ["scripts.evaluate_financial", "--split", "dev"],
        ["scripts.evaluate_agent", "--split", "dev"],
        ["scripts.evaluate_temporal"],
        ["scripts.evaluate_graph"],
        ["scripts.evaluate_grounding"],
        ["scripts.ablate_graph"],
        ["scripts.ablate_structured"],
    ]
    if args.include_test:
        modules.extend(
            [
                ["scripts.evaluate_retrieval", "--split", "test"],
                ["scripts.evaluate_financial", "--split", "test"],
                ["scripts.evaluate_agent", "--split", "test"],
                ["scripts.evaluate_system"],
                ["scripts.build_ablation_table"],
                ["scripts.export_failure_analysis"],
            ]
        )
    for spec in modules:
        print("\n===", " ".join(spec), "===")
        r = subprocess.run([sys.executable, "-m", *spec])
        if r.returncode:
            raise SystemExit(r.returncode)


if __name__ == "__main__":
    main()
