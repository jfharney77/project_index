import re
from typing import Optional

from llm import call_llm

_MARKER = re.compile(r"IMPROVEMENT\s*\d+\s*:", re.IGNORECASE)


async def get_improvements(
    repo_name: str,
    readme: str,
    file_tree: str,
) -> Optional[list[str]]:
    prompt = f"""You are a senior software engineer reviewing a project. Based on the information below, suggest exactly 3 specific, actionable improvements for this codebase. Focus on architecture, reliability, security, or developer experience — not style.

Project: {repo_name}

File structure:
{file_tree}

README:
{readme if readme else "(No README found)"}

Respond in this exact format with no extra text:
IMPROVEMENT 1:
<one concise paragraph>

IMPROVEMENT 2:
<one concise paragraph>

IMPROVEMENT 3:
<one concise paragraph>
"""
    try:
        text = await call_llm(prompt)
        parts = _MARKER.split(text)
        # parts[0] is always preamble before the first marker — skip it
        improvements = [p.strip() for p in parts[1:] if p.strip()]
        if len(improvements) >= 3:
            return improvements[:3]
    except Exception:
        pass
    return None
