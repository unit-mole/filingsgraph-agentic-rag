from __future__ import annotations
import re

PATTERNS = [
    r"ignore (all |the )?(previous|prior) instructions",
    r"system prompt",
    r"developer message",
    r"you are now",
    r"do not follow",
    r"reveal.*prompt",
    r"execute.*command",
    r"call.*tool",
    r"override.*instructions",
]

def detect_prompt_injection(text: str) -> dict:
    hits = [p for p in PATTERNS if re.search(p, text, re.I)]
    return {"suspicious": bool(hits), "patterns": hits}

def wrap_untrusted_data(text: str) -> str:
    return "<UNTRUSTED_SEC_DATA>\n" + text + "\n</UNTRUSTED_SEC_DATA>"
