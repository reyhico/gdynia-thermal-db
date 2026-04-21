"""Logging utilities for gdynia-thermal-db."""

from __future__ import annotations

import logging
import logging.config
from pathlib import Path

import yaml


def setup_logging(config_path: Path | str | None = None) -> None:
    """Configure logging from a YAML config file.

    Args:
        config_path: Path to the logging YAML config. Defaults to
            ``config/logging.yaml`` relative to the project root.
    """
    if config_path is None:
        config_path = Path("config") / "logging.yaml"

    config_path = Path(config_path)

    # Ensure log directory exists
    log_dir = Path("outputs") / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    if config_path.exists():
        with open(config_path) as f:
            cfg = yaml.safe_load(f)
        logging.config.dictConfig(cfg)
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        )

    logging.getLogger(__name__).debug("Logging configured from %s", config_path)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger.

    Args:
        name: Logger name, typically ``__name__``.

    Returns:
        A configured :class:`logging.Logger` instance.
    """
    return logging.getLogger(name)
