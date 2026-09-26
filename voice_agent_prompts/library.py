"""Discover the source library or its bundled wheel copy."""
import json
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent
ROOT = SOURCE if (SOURCE / "catalog.json").is_file() else Path(__file__).parent / "data"


def catalog(industry: str | None = None, call_type: str | None = None) -> list[dict]:
    """Return deterministic catalog rows with optional exact filters."""
    rows = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    return [r for r in rows if (not industry or r["industry"].casefold() == industry.casefold())
            and (not call_type or r["call_type"] == call_type)]


def resolve(name: str) -> Path:
    """Resolve a local file, catalog path, or unique filename/stem."""
    path = Path(name)
    if path.is_file():
        return path
    matches = [r for r in catalog() if name in (r["path"], Path(r["path"]).name, Path(r["path"]).stem)]
    if len(matches) != 1:
        raise ValueError(f"Prompt not found or ambiguous: {name}")
    return ROOT / matches[0]["path"]
