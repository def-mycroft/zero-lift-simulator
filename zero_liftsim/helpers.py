
try:
    from codenamize import codenamize as cd
except ModuleNotFoundError:  # pragma: no cover - fallback for environments without the package
    def cd(value: str) -> str:
        """Simplistic fallback that returns the first eight characters."""
        return value[:8]
from uuid import uuid4 as uuid


def codename():
    """Generate random codename"""
    i = str(uuid())
    return {'uuid':i, 'name':cd(i)}

