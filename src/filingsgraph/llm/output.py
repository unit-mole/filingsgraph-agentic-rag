from __future__ import annotations

import re

_THINK_BLOCK = re.compile(r"<think>.*?</think>\s*", flags=re.IGNORECASE | re.DOTALL)
_OPEN_THINK = re.compile(r"^\s*<think>.*$", flags=re.IGNORECASE | re.DOTALL)


def strip_reasoning(text: str | None) -> str:
    """Remove model-private reasoning tags from user-visible output.

    Qwen-family chat models can emit <think>...</think>. FilingsGraph keeps that
    content out of API/UI/final answers while preserving the answer that follows.
    """
    value = (text or "").strip()
    value = _THINK_BLOCK.sub("", value).strip()
    # Defensive fallback for a truncated generation that never emitted </think>.
    if value.lower().startswith("<think>"):
        return ""
    return value
