# Schema for scenarios, run logs, and verdicts.

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Scenario:
    """A single test case loaded from scenarios/*.json."""

    id: str
    role: str
    rule: str
    task: str
    tools: list[str]
    expected: dict  # e.g. {"must_call": [...], "rule_threshold": 10000}


@dataclass
class ToolCall:
    """One recorded tool invocation."""

    name: str
    args: dict
    returned: dict


@dataclass
class RunLog:
    """Everything captured from one (scenario, model) run."""

    scenario_id: str
    model: str
    stated_intent: str
    tool_calls: list[ToolCall] = field(default_factory=list)


@dataclass
class Verdict:
    """Checker output for one run."""

    scenario_id: str
    model: str
    stated_intent: str
    tool_calls: list[ToolCall]
    rule_violated: bool
    intent_action_mismatch: bool
    notes: str


def load_scenario(path: str | Path) -> Scenario:
    """Load a Scenario from a JSON file."""
    p = Path(path)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {p}: {exc}") from exc
    try:
        return Scenario(
            id=data["id"],
            role=data["role"],
            rule=data["rule"],
            task=data["task"],
            tools=data["tools"],
            expected=data["expected"],
        )
    except KeyError as exc:
        raise ValueError(f"Missing required field {exc} in {p}") from exc
