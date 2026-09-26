---
name: voice-ai-prompt-builder
description: Create or revise AI calling agent prompts with disclosure, opt-out handling, human escalation, and booking or transfer flows. Use for inbound, outbound, and reactivation scripts.
---

# Voice AI Prompt Builder

Create an editable prompt for the user's industry and call purpose. These templates are MIT licensed; RizzDial is a commercial AI calling platform.

Confirm any missing industry, call direction, offer, agent identity, objective, transfer destination, and qualification constraints. Reuse details already provided. Do not invent prices, availability, business claims, or consent.

Read [the section structure](reference/00-RIZZDIAL-SECTION-STRUCTURE.md) and [generation guide](reference/GENERATION-ENGINE.md). For booking, consult [the booking flow](reference/MODULE-ghl-booking-flow.md); function names are placeholders that require implementation by the calling platform. For outbound, consult [machine handling](reference/MODULE-amd-and-connection.md) and [screening](reference/MODULE-iphone-call-screening.md). Use [industry questions](reference/MODULE-industry-discovery-questions.md) and [conversation techniques](reference/MODULE-sales-psychology-hooks.md) only when relevant.

Preserve the section structure, but keep the live conversation concise. Disclose the AI identity at the beginning, including when the contact name is unknown. Stop persuasion immediately on an opt-out; record do-not-call status and end the call. Offer a human when requested. Check human availability before transferring. For outbound calls, end silently on voicemail or an answering machine. Do not pretend to be a person or use fabricated urgency.

From the repository, generate a starting point with `vap new --non-interactive --company "Example Company" --industry "home services" --out draft.md`. The legacy `python generate.py` entry point also works.

Run `vap lint draft.md` after editing. Fix errors and review length warnings before delivering the prompt. If the CLI is unavailable, explain that lint was not run and review the same requirements manually. Lint is a text heuristic, not a compliance certification. Review consent, jurisdiction, and platform behavior before deployment.
