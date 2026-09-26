"""Strict placeholder rendering and dependency-free variable files."""
import json
import re
from pathlib import Path

VARIABLE = re.compile(r"\{\{\s*([\w.-]+)\s*\}\}")


def render(text: str, variables: dict[str, object]) -> str:
    """Substitute in one pass; fail before emitting partially filled output."""
    missing = sorted(set(VARIABLE.findall(text)) - variables.keys())
    if missing:
        raise ValueError("Missing variables: " + ", ".join(missing))
    return VARIABLE.sub(lambda m: str(variables[m.group(1)]), text)


def load_variables(path: Path) -> dict[str, object]:
    """Read JSON or a flat YAML mapping of scalar values (no nested YAML)."""
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json" or raw.lstrip().startswith("{"):
        values = json.loads(raw)
    else:
        values = {}
        for number, line in enumerate(raw.splitlines(), 1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            match = re.fullmatch(r"([\w.-]+):\s*(.*?)\s*", line)
            if not match:
                raise ValueError(f"Expected flat YAML key: value at line {number}")
            key, value = match.groups()
            if key in values:
                raise ValueError(f"Duplicate YAML key: {key}")
            if value.startswith('"'):
                value = json.loads(value)
            elif value.startswith("'"):
                if not value.endswith("'") or len(value) < 2:
                    raise ValueError(f"Unclosed YAML string on line {number}")
                value = value[1:-1].replace("''", "'")
            elif not value or value[0] in "[{&*!|>" or ": " in value:
                raise ValueError("Only flat YAML scalar values are supported; use JSON for other data")
            else:
                value = re.split(r"\s+#", value, maxsplit=1)[0]
            values[key] = value
    if not isinstance(values, dict) or any(not isinstance(k, str) or isinstance(v, (dict, list)) or v is None for k, v in values.items()):
        raise ValueError("Variables must be a mapping of names to non-null scalar values")
    return values
