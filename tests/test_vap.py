"""Offline behavioral tests for the CLI and every shipped prompt."""
import json
from pathlib import Path
import subprocess
import sys
import pytest
from voice_agent_prompts.cli import main
from voice_agent_prompts.library import ROOT, catalog, resolve
from voice_agent_prompts.lint import FORBIDDEN, lint
from voice_agent_prompts.render import load_variables, render

FIXTURES = Path(__file__).parent / "fixtures"
GOOD = (FIXTURES / "good.md").read_text()


def test_good_fixture():
    assert lint(GOOD) == []


def test_bad_fixture():
    assert {i.code for i in lint((FIXTURES / "bad.md").read_text())} >= {"identity", "goal", "disclosure", "opt-out", "transfer", "voicemail"}


@pytest.mark.parametrize("section,code", [("Role", "identity"), ("Goal", "goal"), ("AI disclosure", "disclosure"), ("Opt-out / DNC", "opt-out"), ("Transfer", "transfer"), ("Voicemail", "voicemail")])
def test_missing_section(section, code):
    chunks = GOOD.split("## ")
    text = "## ".join(c for c in chunks if not c.startswith(section + "\n"))
    assert code in {i.code for i in lint(text)}


@pytest.mark.parametrize("pattern", FORBIDDEN)
def test_restricted_vocabulary(pattern):
    import re
    word = re.sub(r"\\x([0-9a-f]{2})", lambda m: chr(int(m[1], 16)), pattern.replace(r"\b", ""))
    assert "forbidden" in {i.code for i in lint(GOOD + word.upper())}


@pytest.mark.parametrize("text,code", [(chr(0x2013), "punctuation"), (chr(0x2014), "punctuation"), ("85" + "%", "claims"), ("100" + ",000", "claims"), ("booking" + " rate", "claims")])
def test_other_content_rules(text, code):
    assert code in {i.code for i in lint(GOOD + text)}


def test_length_warning():
    assert any(i.warning and i.code == "length" for i in lint(GOOD, max_length=10))


def test_inbound_does_not_require_machine_handling():
    assert not lint(GOOD.split("## Voicemail")[0], call_type="inbound")


@pytest.mark.parametrize("row", catalog(), ids=lambda r: r["path"])
def test_every_shipped_prompt(row):
    assert not [i for i in lint((ROOT / row["path"]).read_text(), row["call_type"]) if not i.warning]


def test_catalog_covers_all_prompt_files():
    actual = {str(p.relative_to(ROOT)) for folder in ("prompts", "templates", "examples") for p in (ROOT / folder).rglob("*.md") if p.name != "README.md" and not p.name.startswith("WHY-")}
    assert actual == {r["path"] for r in catalog()}
    assert len(catalog()) == len(actual)


def test_niche_example_configs_load_render_and_lint():
    niches_dir = ROOT / "examples" / "niches"
    yaml_files = sorted(niches_dir.glob("*.yaml"))
    assert yaml_files
    for yaml_file in yaml_files:
        prompt_file = yaml_file.with_suffix(".md")
        assert prompt_file.is_file(), yaml_file
        variables = load_variables(yaml_file)
        rendered = render(prompt_file.read_text(encoding="utf-8"), variables)
        assert not [i for i in lint(rendered) if not i.warning]


def test_packaged_data_matches_source():
    bundled = ROOT / "voice_agent_prompts/data"
    assert (bundled / "catalog.json").read_bytes() == (ROOT / "catalog.json").read_bytes()
    for row in catalog():
        assert (bundled / row["path"]).read_bytes() == (ROOT / row["path"]).read_bytes()


@pytest.mark.parametrize("industry,call_type", [("hvac", "inbound"), ("solar", "outbound-cold"), ("general", "voicemail-amd"), (None, "reactivation")])
def test_list_filtering(industry, call_type):
    rows = catalog(industry, call_type)
    assert rows and all(r["call_type"] == call_type and (not industry or r["industry"] == industry) for r in rows)


def test_unknown_filter():
    assert catalog("nonexistent") == []


def test_render_values():
    assert render("{{ x }} {{x}} {{user.name}}", {"x": "hello", "user.name": 2}) == "hello hello 2"


def test_render_literal_values():
    assert render("{{x}}", {"x": "{{y}}"}) == "{{y}}"


def test_render_missing():
    with pytest.raises(ValueError, match="Missing variables: x, y"):
        render("{{y}} {{x}}", {})


@pytest.mark.parametrize("suffix,content", [(".json", '{"x":"a=b", "n":2}'), (".yaml", "# note\nx: 'a=b'\nn: 2\n"), (".yml", 'x: "a=b"\nn: 2 # count\n')])
def test_variable_files(tmp_path, suffix, content):
    p = tmp_path / ("vars" + suffix); p.write_text(content)
    assert render("{{x}} {{n}}", load_variables(p)) == "a=b 2"


@pytest.mark.parametrize("content,suffix", [("[]", ".json"), ('{"x":null}', ".json"), ('{"x":{}}', ".json"), ("x:\n  y: z", ".yaml"), ("x: [a]", ".yaml"), ("x: a\nx: b", ".yaml"), ("x: 'unclosed", ".yaml")])
def test_invalid_variable_files(tmp_path, content, suffix):
    p = tmp_path / ("vars" + suffix); p.write_text(content)
    with pytest.raises(ValueError):
        load_variables(p)


def test_cli_render_override(tmp_path, capsys):
    p = tmp_path / "v.json"; p.write_text('{"company":"Before"}')
    assert main(["render", "examples/demo.md", "--vars", str(p), "--var", "company=After"]) == 0
    assert "After" in capsys.readouterr().out


@pytest.mark.parametrize("args", [["show", "missing-file"], ["render", "examples/demo.md"], ["render", "examples/demo.md", "--var", "bad"], ["lint", "examples/demo.md", "--max-length", "0"]])
def test_cli_errors(args, capsys):
    assert main(args) == 2
    assert "vap:" in capsys.readouterr().err


def test_cli_lint_status(capsys):
    assert main(["lint", str(FIXTURES / "bad.md")]) == 1
    assert main(["lint", str(FIXTURES / "good.md"), "--max-length", "10"]) == 0
    assert main(["lint", str(FIXTURES / "good.md"), "--max-length", "10", "--strict"]) == 1


def test_cli_list(capsys):
    assert main(["list", "--industry", "hvac", "--call-type", "inbound"]) == 0
    output = capsys.readouterr().out
    assert "hvac-inbound.md" in output and "solar" not in output


def test_cli_show(capsys):
    assert main(["show", "demo"]) == 0
    assert "{{company}}" in capsys.readouterr().out


def test_render_file(tmp_path):
    out = tmp_path / "rendered.md"
    assert main(["render", "demo", "--var", "company=Acme", "--out", str(out)]) == 0
    assert "{{company}}" not in out.read_text()


@pytest.mark.parametrize("command", [["generate.py"], ["-m", "voice_agent_prompts", "new"]])
def test_generator_smoke(command, tmp_path):
    out = tmp_path / "new.md"
    result = subprocess.run([sys.executable, *command, "--non-interactive", "--company", "Acme", "--out", str(out)], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "Acme" in out.read_text()
    assert not [i for i in lint(out.read_text()) if not i.warning]


@pytest.mark.parametrize("vertical", ["medspa", "hvac", "healthcare", "insurance", "solar", "real-estate", "b2b-saas", "marketing-agency"])
def test_generated_verticals(vertical):
    import generate
    assert not [i for i in lint(generate.assemble(generate.VERTICALS[vertical])) if not i.warning]


def test_module_entrypoint():
    result = subprocess.run([sys.executable, "-m", "voice_agent_prompts", "list", "--industry", "hvac"], capture_output=True, text=True)
    assert result.returncode == 0 and "hvac" in result.stdout


def test_generator_preset_overrides(tmp_path):
    out = tmp_path / "preset.md"
    result = subprocess.run([sys.executable, "generate.py", "--vertical", "hvac", "--offer", "an inspection", "--industry", "custom services", "--transfer", "the support desk", "--hipaa", "--out", str(out)], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0
    text = out.read_text()
    assert all(value in text for value in ("an inspection", "custom services", "the support desk", "NEVER give medical advice"))


def test_browser_generator(tmp_path):
    import re
    import shutil
    node = shutil.which("node")
    if not node:
        pytest.skip("Optional browser JavaScript smoke check requires Node")
    html = (ROOT / "index.html").read_text()
    script = re.search(r"<script>(.*?)</script>", html, re.S)[1].split("// init")[0]
    path = tmp_path / "browser.cjs"
    path.write_text(script + '\nconsole.log(JSON.stringify(Object.values(VERTICALS).map(assemble)));\n')
    result = subprocess.run([node, str(path)], capture_output=True, text=True, check=True)
    outputs = json.loads(result.stdout)
    assert len(outputs) == 8
    for text in outputs:
        assert not [i for i in lint(text) if not i.warning]
        assert "undefined" not in text


def test_repository_content_rules():
    import re
    ignored = {".git", ".venv", "build", "dist", ".pytest_cache", "__pycache__"}
    for path in ROOT.rglob("*"):
        rel_parts = path.relative_to(ROOT).parts
        if not path.is_file() or ignored.intersection(rel_parts) or any(p.endswith(".egg-info") for p in rel_parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            continue
        assert not re.search(r"[\u2013\u2014]", text), path
        assert not any(re.search(pattern, text, re.I) for pattern in FORBIDDEN), path
        if path.suffix == ".md":
            # URL encodings, and HTML tag attributes (e.g. width="100%"), are not
            # percentages or performance figures.
            prose = re.sub(r"https?://[^\s)]+", "", text)
            prose = re.sub(r"<[^>]+>", "", prose)
            assert not re.search(r"\d\s*(?:%|percent\b)|100[,]000|\b(?:conversion|booking) rates?\b", prose, re.I), path


def test_markdown_local_links():
    import re
    for folder in ("prompts", "templates", "skills", "framework", "modules", "commands"):
        for path in (ROOT / folder).rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                assert (path.parent / target.split("#")[0]).exists(), (path, target)
