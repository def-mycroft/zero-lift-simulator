from __future__ import annotations

"""Utilities for querying git history."""

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from datetime import timezone, timedelta

import subprocess

try:
    from git import Repo
except ModuleNotFoundError:  # pragma: no cover - fallback without GitPython
    Repo = None


_REPO_ROOT = Path(__file__).resolve().parents[1]
if Repo is not None:
    _REPO = Repo(_REPO_ROOT)
    HEAD_COMMIT = _REPO.head.commit.hexsha
else:
    _REPO = None
    HEAD_COMMIT = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=_REPO_ROOT, text=True
    ).strip()

try:
    DENVER_TZ = ZoneInfo("US/Denver")
except ZoneInfoNotFoundError:  # pragma: no cover - fallback when tzdata missing
    DENVER_TZ = timezone(timedelta(hours=-7))


def last_commit_info(path: Path) -> tuple[str, datetime]:
    """Return the last commit SHA and datetime for ``path``.

    Parameters
    ----------
    path:
        File path to inspect. It must be within the project repository.
    """
    rel = path.relative_to(_REPO_ROOT)
    if Repo is not None:
        commit = next(_REPO.iter_commits(paths=str(rel), max_count=1))
        dt = commit.committed_datetime.astimezone(DENVER_TZ)
        sha = commit.hexsha
    else:
        sha = subprocess.check_output(
            ["git", "log", "-n", "1", "--pretty=format:%H", "--", str(rel)],
            cwd=_REPO_ROOT,
            text=True,
        ).strip()
        dt_str = subprocess.check_output(
            ["git", "log", "-n", "1", "--pretty=format:%cI", "--", str(rel)],
            cwd=_REPO_ROOT,
            text=True,
        ).strip()
        dt = datetime.fromisoformat(dt_str).astimezone(DENVER_TZ)
    return sha, dt


def append_git_info(path: Path) -> None:
    """Append git commit info to ``path`` in place."""
    sha, dt = last_commit_info(path)
    text = path.read_text(encoding="utf-8").rstrip() + "\n"
    lines = text.splitlines()
    # remove existing Git Info section if present
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].startswith("# Git Info"):
            lines = lines[:i]
            break
    lines.append("# Git Info")
    lines.append(f"Commit: {sha}")
    lines.append(f"Date: {dt.isoformat()}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def tracked_files() -> list[Path]:
    """Return all file paths tracked by the git repository."""
    if Repo is not None:
        files = _REPO.git.ls_files().splitlines()
    else:
        files = subprocess.check_output(["git", "ls-files"], cwd=_REPO_ROOT, text=True).splitlines()
    return [Path(p) for p in files]

