# Contributing

Use Python 3.11 or newer. Install `pip install -e . -r requirements-dev.txt` and run `pytest -q` before submitting a change.

Keep prompts generic and grounded in verified business facts. Include an early AI disclosure, opt-out / DNC handling, escalation, and outbound voicemail handling. Use plain hyphens and avoid superlatives, vendor references, or invented outcomes.

Add new prompt metadata to `catalog.json` and update `prompts/README.md`. Run `python scripts/bundle_library.py` after editing prompts or the catalog so installed packages include the same content. Run `vap lint path/to/prompt.md`, then the full tests. The parametrized library check includes templates and examples.

Keep runtime dependencies in the standard library. Tests and the demo must run offline without credentials. Do not commit secrets or customer information.
