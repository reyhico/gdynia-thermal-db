"""I/O helpers for reading and writing data products."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
import yaml


def read_yaml(path: Path | str) -> dict[str, Any]:
    """Read a YAML file into a Python dict.

    Args:
        path: Path to the YAML file.

    Returns:
        Parsed YAML as a dictionary.
    """
    with open(path) as f:
        return yaml.safe_load(f) or {}


def write_yaml(data: dict[str, Any], path: Path | str) -> None:
    """Write a Python dict to a YAML file.

    Args:
        data: Data to serialize.
        path: Destination file path.
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


def read_json(path: Path | str) -> Any:
    """Read a JSON file.

    Args:
        path: Path to the JSON file.

    Returns:
        Parsed JSON object.
    """
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(data: Any, path: Path | str, indent: int = 2) -> None:
    """Write data to a JSON file.

    Args:
        data: Data to serialize.
        path: Destination file path.
        indent: JSON indentation level.
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False, default=str)


def save_dataframe(df: pd.DataFrame, path: Path | str, **kwargs: Any) -> None:
    """Save a DataFrame to CSV, inferring the format from the file extension.

    Args:
        df: DataFrame to save.
        path: Destination file path (.csv, .parquet, or .json).
        **kwargs: Additional keyword arguments passed to the underlying writer.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    ext = path.suffix.lower()
    if ext == ".csv":
        df.to_csv(path, index=False, **kwargs)
    elif ext == ".parquet":
        df.to_parquet(path, index=False, **kwargs)
    elif ext == ".json":
        df.to_json(path, orient="records", indent=2, **kwargs)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
