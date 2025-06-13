from __future__ import annotations

"""Utilities for querying git history."""

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from datetime import timezone, timedelta

from git import Repo


_REPO = Repo(Path(__file__).resolve().parents[1])

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
    rel = path.relative_to(_REPO.working_tree_dir)
    commit = next(_REPO.iter_commits(paths=str(rel), max_count=1))
    dt = commit.committed_datetime.astimezone(DENVER_TZ)
    return commit.hexsha, dt


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
    return [Path(p) for p in _REPO.git.ls_files().splitlines()]

