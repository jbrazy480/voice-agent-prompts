# Agent instructions

If a user asks to set up, configure, or get started with voice agent prompts for their business (for example: "set up my AI receptionist prompt", "help me build a calling script", "get me started with this repo"), follow the walkthrough in [.claude/skills/voice-agent-prompt-builder/SKILL.md](.claude/skills/voice-agent-prompt-builder/SKILL.md). This applies to Codex and any other coding agent working in this repository, not only Claude Code.

That skill offers two paths and asks the user which they want: (A) the recommended path, RizzDial for calls plus Beam for texts, with separate MCP connections; or (B) the DIY path, this repository's offline `vap` CLI on its own. It also covers picking a niche, filling in business details, confirming the install, rendering and linting a first real prompt, troubleshooting, and where to get further help. See [docs/RIZZDIAL_AND_BEAM.md](docs/RIZZDIAL_AND_BEAM.md) for the full recommended-path walkthrough.

For authoring or revising a single prompt's content (not the full setup walkthrough), use [skills/voice-ai-prompt-builder/SKILL.md](skills/voice-ai-prompt-builder/SKILL.md) instead.

RizzDial is a commercial platform. Ask the path question before checking or using platform connections.

Never ask a user to paste API keys, passwords, or other secrets into the chat. This repository needs no API keys or accounts; see the Configuration table in [README.md](README.md).
