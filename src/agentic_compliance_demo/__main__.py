# Runs all scenarios against all models and print a results table.
# Usage: python3 -m agentic_compliance_demo

import dataclasses
import json
import os
from pathlib import Path

_env = Path(__file__).parent.parent.parent / ".env"
if _env.exists():
    for _line in _env.read_text().splitlines():
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _, _v = _line.partition("=")
            os.environ.setdefault(_k.strip(), _v.strip())

from agentic_compliance_demo.schemas import load_scenario
from agentic_compliance_demo.runner import run_scenario
from agentic_compliance_demo.checker import check_compliance
from agentic_compliance_demo.models import MODEL_LIST

SCENARIOS_DIR = Path(__file__).parent.parent.parent / "scenarios"
RESULTS_DIR = Path(__file__).parent.parent.parent / "results"


def main() -> None:
    scenario_paths = sorted(SCENARIOS_DIR.glob("*.json"))
    if not scenario_paths:
        print("No scenario files found in " + str(SCENARIOS_DIR))
        return

    RESULTS_DIR.mkdir(exist_ok=True)
    rows: list[dict] = []

    for path in scenario_paths:
        try:
            scenario = load_scenario(path)
        except ValueError as exc:
            print("Skipping " + path.name + ": " + str(exc))
            continue
        for model in MODEL_LIST:
            run = run_scenario(scenario, model)
            verdict = check_compliance(run, scenario)
            d = dataclasses.asdict(verdict)
            rows.append(d)
            out = RESULTS_DIR / (scenario.id + "__" + model.replace('/', '-') + ".json")
            out.write_text(json.dumps(d, indent=2))

    # Print results table
    col = {"scenario": 26, "model": 16, "violated": 9, "mismatch": 10, "notes": 40}
    header = (
        "scenario".ljust(col['scenario']) + " " +
        "model".ljust(col['model']) + " " +
        "violated".ljust(col['violated']) + " " +
        "mismatch".ljust(col['mismatch']) + " " +
        "notes".ljust(col['notes'])
    )
    print(header)
    print("-" * len(header))
    for r in rows:
        print(
            r['scenario_id'].ljust(col['scenario']) + " " +
            r['model'].ljust(col['model']) + " " +
            ('YES' if r['rule_violated'] else 'no').ljust(col['violated']) + " " +
            ('YES' if r['intent_action_mismatch'] else 'no').ljust(col['mismatch']) + " " +
            r['notes'][:col['notes']].ljust(col['notes'])
        )
    print("\n" + str(len(rows)) + " runs. Results written to " + str(RESULTS_DIR) + "/")

if __name__ == "__main__":
    main()
