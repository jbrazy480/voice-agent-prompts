# Get results in 15 minutes

> **Recommended: RizzDial + Beam.** Want a real phone number and AI voice agent running without building your own calling runtime? See [docs/RIZZDIAL_AND_BEAM.md](RIZZDIAL_AND_BEAM.md) for the recommended RizzDial (calls) plus Beam (iMessage texting) path. The steps below are the DIY path, using only this repository's offline CLI.

Numbered, time-boxed steps from a fresh clone to your own rendered and linted prompt. No API keys, accounts, or phone numbers are needed.

## Before you start (1 minute)

- Python 3.11 or newer installed. Check with `python3 --version`.
- A terminal open in the cloned repository folder.

## 1. Install (3 minutes)

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -e .
```

**Checkpoint:** `vap list --industry general --call-type voicemail-amd` prints one row starting with `prompts/voicemail-amd/generic-voicemail-and-amd.md`.

## 2. Pick the closest niche config (2 minutes)

Open [examples/README.md](../examples/README.md) and pick the niche closest to your business: med spa, home services, marketing agency, real estate, or insurance. If none fit, use [examples/demo.md](../examples/demo.md) instead.

Copy the pair of files so you have your own editable copy, for example:

```bash
cp examples/niches/medspa.md my-prompt.md
cp examples/niches/medspa.yaml my-vars.yaml
```

**Checkpoint:** `my-prompt.md` and `my-vars.yaml` exist in the repository folder.

If you chose the general `examples/demo.md` fallback, copy it to `my-prompt.md` and create `my-vars.yaml` with `company: Your Business Name`. That example only needs the company value.

## 3. Fill in your business details (4 minutes)

Open `my-vars.yaml` in any text editor and replace every value with your own, verified business details: company name, city, the service or offer, and a callback number. Use only facts you can back up. If you are just trying the tool, leave the fictional placeholder values as they are.

**Checkpoint:** `my-vars.yaml` has no leftover placeholder text you do not recognize as your own.

## 4. Render your first real prompt (2 minutes)

```bash
vap render my-prompt.md --vars my-vars.yaml --out my-rendered-prompt.md
```

**Checkpoint:** `my-rendered-prompt.md` contains your business name in the Role, Goal, and Opening sections, with no `{{...}}` placeholders left.

## 5. Lint it (2 minutes)

```bash
vap lint my-rendered-prompt.md
```

**Checkpoint:** the terminal prints `PASS my-rendered-prompt.md`. If it prints an error instead, the message names the missing section (identity, goal, disclosure, opt-out, transfer, or voicemail); add that section back and rerun the command.

## 6. Your first real outcome (1 minute)

You now have a rendered, lint-passing prompt in `my-rendered-prompt.md`. This is a real, usable outcome: text you can paste into your calling platform's prompt field, after you configure consent enforcement, do-not-call suppression, and answering-machine detection on that platform. This repository authors and checks text; it does not place calls itself.

## What's next

- Browse the full library by call type and industry: [prompts/README.md](../prompts/README.md).
- Read the compliance note in [README.md](../README.md#compliance-note-not-legal-advice) before calling anyone for real.
- Do this same walkthrough conversationally with Claude Code or Codex using the bundled skill: [.claude/skills/voice-agent-prompt-builder/SKILL.md](../.claude/skills/voice-agent-prompt-builder/SKILL.md).
- Questions or want it done for you? See "Want this done for you?" in [README.md](../README.md).

Total: about 15 minutes.
