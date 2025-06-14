#!/usr/bin/env python3
# limit_output
"""Generate evaluation score and update results file."""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from limited_io import _LimitedIO  # noqa: E402


sys.stdout = _LimitedIO(sys.stdout)
sys.stderr = _LimitedIO(sys.stderr)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    import yaml  # type: ignore

    YAML_AVAILABLE = True
except Exception:
    YAML_AVAILABLE = False

from o3research.core.evaluation import evaluate  # noqa: E402


def load_metrics(path: Path) -> dict:
    """Load metrics from a JSON or YAML file."""
    text = path.read_text(encoding="utf-8")
    if path.suffix in {".yaml", ".yml"}:
        if not YAML_AVAILABLE:
            raise RuntimeError("PyYAML is required for YAML input")
        return yaml.safe_load(text)
    return json.loads(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate evaluation results")
    parser.add_argument("metrics_file", help="Path to metrics JSON or YAML file")
    args = parser.parse_args()

    metrics_path = Path(args.metrics_file)
    metrics = load_metrics(metrics_path)

    score = evaluate(metrics)

    results_path = Path("docs") / "meta" / "evaluation_results.json"
    results = {}
    if results_path.exists():
        results = json.loads(results_path.read_text(encoding="utf-8"))

    version = Path("VERSION").read_text(encoding="utf-8").strip()
    results.update(
        {
            "version": version,
            "scores": metrics,
            "score": score,
            "date": date.today().isoformat(),
        }
    )
    results.setdefault("reviewer", "Automated")

    results_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote evaluation results to {results_path}")


if __name__ == "__main__":
    main()
