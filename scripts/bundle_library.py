"""Refresh wheel data from the reviewed source catalog and prompt files."""
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    """Copy only catalogued prompts, preserving their relative paths."""
    target = ROOT / "voice_agent_prompts" / "data"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir()
    shutil.copy2(ROOT / "catalog.json", target / "catalog.json")
    for row in json.loads((ROOT / "catalog.json").read_text()):
        path = Path(row["path"])
        dest = target / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / path, dest)


if __name__ == "__main__":
    main()
