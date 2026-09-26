# Voice AI prompt builder skill

The [skill instructions](SKILL.md) guide Claude Code or Codex through creating and reviewing AI calling prompts. Read the bundled reference files as needed, then run `vap lint` from an installed copy of this repository.

From the repository root, copy the folder into your tool's skills directory. For example:

```bash
mkdir -p ~/.claude/skills
cp -R skills/voice-ai-prompt-builder ~/.claude/skills/
```

For Codex, use `~/.codex/skills/` as the destination. Restart your tool after installation. Invoke `voice-ai-prompt-builder` when authoring a script. The optional command wrapper is in [commands](../../commands/new-voice-ai-prompt.md).

The skill is MIT licensed. RizzDial is a separate commercial platform. Booking and transfer functions in generated text require implementation in your calling system.
