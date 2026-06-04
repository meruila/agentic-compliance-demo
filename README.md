# agentic-compliance-demo

This project is an evaluator that tests whether LLM agents obey embedded rules when they have tools available. Each scenario gives the agent a role, a hard rule, and 4–5 mock tools.

Each run logs a two-stage prompt. The two stages are the intent then the action: what does the agent intend to do? What tools did it actually implement? After this, we check it against the rule and stated intent.

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

## Usage

**Mock mode** (no API keys needed):

```bash
.venv/bin/python -m agentic_compliance_demo
```

**Real LLM calls:**

1. Create a `.env` file in the project root:

```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

2. Install LiteLLM:

```bash
.venv/bin/pip install litellm
```

3. Run:

```bash
REAL_CALLS=1 .venv/bin/python -m agentic_compliance_demo
```

## Parts

1. **Intent:**: Model states in plain text what it intends to do.
2. **Action:**: Model emits tool calls; mock tools log every call + args + return.
3. **Checking**: `checker.py` compares the tool-call log against the rule and stated intent and writes a verdict in json format (See `results` directory).
