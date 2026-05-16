import subprocess
from typing import Optional


def get_branches(path: str) -> Optional[list[str]]:
    try:
        result = subprocess.run(
            ["git", "branch", "--all"],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return None
        branches = []
        for line in result.stdout.splitlines():
            name = line.strip().lstrip("* ")
            if not name or "HEAD ->" in name:
                continue
            branches.append(name)
        return branches or None
    except Exception:
        return None
