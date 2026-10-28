"""Persistence: the hidden .actiontrack/ data folder and the item store."""

from pathlib import Path

DATA_DIR_NAME = ".actiontrack"


def data_dir(base: Path | str | None = None) -> Path:
    """Return the .actiontrack/ folder under base (default: cwd), creating it."""
    path = Path(base if base is not None else Path.cwd()) / DATA_DIR_NAME
    path.mkdir(exist_ok=True)
    return path
