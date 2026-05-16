import re
import subprocess
from typing import Optional

# Only display SSH remotes — HTTPS URLs may contain embedded tokens
_SSH_PATTERN = re.compile(r"^git@([^:]+):(.+)$")


def get_remote_origin(path: str) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            raw = result.stdout.strip()
            match = _SSH_PATTERN.match(raw)
            if match:
                return f"{match.group(1)}/{match.group(2)}"
    except Exception:
        pass
    return None
