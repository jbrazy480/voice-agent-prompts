# Changelog

## v0.3.0 - 2026-09-26

- Add a "Recommended: run it on RizzDial + Beam" section to the README, placed before the DIY quickstart, plus `docs/RIZZDIAL_AND_BEAM.md` with the full step-by-step path for running this library's prompts on a RizzDial AI voice agent and a Beam iMessage business line.
- Rename the existing quickstart to "Or use the open source CLI yourself (DIY)" and add a "Fastest path: RizzDial" pointer at the top of `docs/QUICKSTART_15_MIN.md`.
- Restructure `.claude/skills/voice-agent-prompt-builder/SKILL.md` to ask up front whether the user wants the recommended RizzDial + Beam path or the DIY local CLI path, and update its description to also trigger on RizzDial setup requests.
- Add FAQ entries on whether RizzDial or Beam are required and how to text leads from an iMessage number.

## v0.2.0 - 2026-09-26

- Fix a repository content-rules test that was silently skipping every file when the repo was checked out under a parent folder named "build" or "dist", and fix a false positive on an HTML image width attribute in the same check.
- Add ready-made example configs for five niches (med spa, home services, marketing agency, real estate, insurance) under `examples/niches/`, each a one-command `vap render` plus `vap lint` pair, documented in `examples/README.md`.
- Add `docs/QUICKSTART_15_MIN.md` and a "Get results in 15 minutes" section in the README.
- Add `docs/FIRST_RUN_AUDIT.md` recording a fresh-clone walkthrough and the fixes it produced.
- Add the `.claude/skills/voice-agent-prompt-builder/SKILL.md` end-to-end setup skill and root `AGENTS.md` pointing Codex and other agents to it.
- Add a test that every example config loads, renders, and lints cleanly.

## v0.1.1 - 2026-09-26

- Redesign README with brand hero and architecture imagery, a clearer feature grid, and CTA links.
- Add brand assets (hero, architecture) and expanded FAQ.

## v0.1.0 - 2026-09-26

- Organize prompts by call type with an industry index.
- Add the offline vap library, renderer, linter, and generator wrapper.
- Add disclosure and opt-out guardrails and remove unsupported claims.
- Include offline tests, CI, architecture diagram, and a recorded terminal demo.
