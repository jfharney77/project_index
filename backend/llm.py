import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

PROVIDER = os.environ.get("LLM_PROVIDER", "ollama").lower()

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://172.30.48.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3")

CEREBRAS_API_KEY = os.environ.get("CEREBRAS_API_KEY", "")
CEREBRAS_MODEL = os.environ.get("CEREBRAS_MODEL", "gpt-oss-120b")
CEREBRAS_BASE_URL = "https://api.cerebras.ai/v1"


async def _call_ollama(prompt: str) -> str:
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")


async def _call_cerebras(prompt: str) -> str:
    if not CEREBRAS_API_KEY:
        raise ValueError("CEREBRAS_API_KEY must be set in .env")
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{CEREBRAS_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {CEREBRAS_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": CEREBRAS_MODEL,
                "messages": [{"role": "user", "content": prompt}],
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


async def generate_summary(
    repo_name: str,
    readme_content: str,
    file_tree: str,
    metadata_summary: str,
) -> dict[str, str]:
    prompt = f"""You are analyzing a software project. Based on the information below, provide:
1. A concise summary of what this project does (2-4 sentences).
2. Instructions on how to run/use this project.

Project name: {repo_name}

File structure:
{file_tree}

Project statistics:
{metadata_summary}

README content:
{readme_content if readme_content else "(No README found)"}

Respond in this exact format:
SUMMARY:
<your summary here>

HOW TO RUN:
<your run instructions here>
"""

    try:
        if PROVIDER == "cerebras":
            text = await _call_cerebras(prompt)
        else:
            text = await _call_ollama(prompt)
        return _parse_response(text)
    except Exception as e:
        return {
            "summary": f"Failed to generate summary: {str(e)}",
            "how_to_run": f"Could not generate run instructions. Provider: {PROVIDER}. Check your configuration.",
        }


def _parse_response(text: str) -> dict[str, str]:
    summary = ""
    how_to_run = ""

    if "SUMMARY:" in text and "HOW TO RUN:" in text:
        parts = text.split("HOW TO RUN:")
        summary_part = parts[0].split("SUMMARY:")[-1].strip()
        how_to_run_part = parts[1].strip()
        summary = summary_part
        how_to_run = how_to_run_part
    else:
        summary = text.strip()
        how_to_run = "See project README for run instructions."

    return {"summary": summary, "how_to_run": how_to_run}
