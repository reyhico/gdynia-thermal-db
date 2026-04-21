"""Path resolution helpers."""

from __future__ import annotations

from pathlib import Path


def ensure_dir(path: Path | str) -> Path:
    """Create directory (and parents) if it doesn't exist.

    Args:
        path: Directory path to create.

    Returns:
        The resolved :class:`~pathlib.Path`.
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def project_root() -> Path:
    """Return the project root directory.

    Walks up from this file's location to find the pyproject.toml.

    Returns:
        Path to the project root.
    """
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    return here.parents[3]  # fallback: src/gdynia_thermal_db/utils/__file__


def data_path(*parts: str) -> Path:
    """Return an absolute path under the project data directory.

    Args:
        *parts: Path components relative to ``data/``.

    Returns:
        Resolved absolute path.
    """
    return project_root() / "data" / Path(*parts)


def output_path(*parts: str) -> Path:
    """Return an absolute path under the project outputs directory.

    Args:
        *parts: Path components relative to ``outputs/``.

    Returns:
        Resolved absolute path.
    """
    return project_root() / "outputs" / Path(*parts)
