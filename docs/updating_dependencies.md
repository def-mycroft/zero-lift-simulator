# Updating Dependencies

This project manages third‑party packages using `pyproject.toml`.
Follow these steps whenever you need to add or upgrade a library.

1. Edit the `[project]` section of `pyproject.toml` and list the package
   under `dependencies`.
2. Run `pip install -e .` to install the project along with its updated
   requirements.
3. Execute `pytest` to ensure everything works with the new versions.

Keeping dependencies pinned in version control makes setups reproducible
and prevents missing package errors like the one shown in `bugfix_add_deps.md`.
