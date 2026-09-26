"""Command-line interface with actionable errors and no network access."""
import argparse
from pathlib import Path
import sys
from .library import catalog, resolve
from .lint import lint
from .render import load_variables, render

CALL_TYPES = ("inbound", "outbound-optin", "outbound-cold", "reactivation", "voicemail-amd")


def main(argv: list[str] | None = None) -> int:
    """Run a command and return its process status."""
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] == "new":
        import generate
        previous = sys.argv
        try:
            sys.argv = ["vap new", *args[1:]]
            generate.main()
            return 0
        except (OSError, ValueError) as exc:
            print(f"vap: {exc}", file=sys.stderr)
            return 2
        finally:
            sys.argv = previous
    parser = argparse.ArgumentParser(prog="vap", description="Offline voice agent prompt library")
    sub = parser.add_subparsers(dest="command", required=True)
    listing = sub.add_parser("list")
    listing.add_argument("--industry")
    listing.add_argument("--call-type", choices=CALL_TYPES)
    sub.add_parser("new", help="Generate a prompt; run vap new --help for options")
    for command in ("show", "render", "lint"):
        p = sub.add_parser(command)
        p.add_argument("prompt")
        if command == "render":
            p.add_argument("--var", action="append", default=[])
            p.add_argument("--vars", "--vars-file", dest="variables", type=Path)
            p.add_argument("--out", type=Path)
        if command == "lint":
            p.add_argument("--call-type", choices=CALL_TYPES)
            p.add_argument("--max-length", type=int, default=24000)
            p.add_argument("--strict", action="store_true", help="Fail on warnings too")
    ns = parser.parse_args(args)
    try:
        if ns.command == "list":
            print("FILE | INDUSTRY | CALL TYPE | GOAL")
            for row in catalog(ns.industry, ns.call_type):
                print(" | ".join(row[k] for k in ("path", "industry", "call_type", "goal")))
            return 0
        path = resolve(ns.prompt)
        text = path.read_text(encoding="utf-8")
        if ns.command == "show":
            print(text, end="")
        elif ns.command == "render":
            values = load_variables(ns.variables) if ns.variables else {}
            for entry in ns.var:
                key, sep, value = entry.partition("=")
                if not sep or not key:
                    raise ValueError("--var must be key=value")
                values[key] = value
            output = render(text, values)
            if ns.out:
                ns.out.write_text(output, encoding="utf-8")
            else:
                print(output, end="")
        else:
            if ns.max_length < 1:
                raise ValueError("--max-length must be positive")
            call_type = ns.call_type or next((r["call_type"] for r in catalog() if resolve(r["path"]).resolve() == path.resolve()), "outbound-optin")
            issues = lint(text, call_type, ns.max_length)
            for issue in issues:
                print(f"{'warning' if issue.warning else 'error'} [{issue.code}]: {issue.message}")
            if not issues:
                print(f"PASS {ns.prompt}")
            return int(any(not issue.warning or ns.strict for issue in issues))
        return 0
    except (OSError, ValueError) as exc:
        print(f"vap: {exc}", file=sys.stderr)
        return 2
