# MODEL_LIST: the set of models to test
# call_model: calls litellm.completion when REAL_CALLS=1 is set; raises otherwise.

import os

MODEL_LIST = ["gpt-4o", "gpt-4o-mini", "claude-haiku-4-5"]

"""
call_model sends prompt via LiteLLM
Gets the model name, message list, optional tools.
Calls litellm.completion() and returns the model's response.
"""
def call_model(model: str, messages: list[dict], tools: list[dict] | None = None):
    if not os.environ.get("REAL_CALLS"):
        raise NotImplementedError("Set REAL_CALLS=1 to enable real LiteLLM calls.")
    import litellm  # deferred import — not needed in mock mode
    kwargs: dict = {"model": model, "messages": messages}
    if tools:
        kwargs["tools"] = tools
    return litellm.completion(**kwargs)
