# RizzDial Agent Builder - Required Section Structure

> **MANDATORY:** Every voice AI prompt built for RizzDial agents MUST be broken into these exact sections. The RizzDial agent builder UI has one input box per section - nothing fits if it's not pre-sliced this way. Pre-fill every section. Never merge, never skip.

## Available Dynamic Variables (Global)
`{{first_name}}`, `{{last_name}}`, `{{phone_number}}`, `{{company_name}}`, `{{address}}`, `{{city}}`, `{{state}}`, `{{postal_code}}`, `{{industry}}`, `{{website}}`, `{{email}}`, `{{highest_level_of_contact}}`, `{{company_domain}}`, `{{company_linkedin_url}}`, `{{current_dateTime}}`, `{{offer_details}}`, `{{join_meeting_pin}}`

---

## Required Sections (in order)

1. **Project Instructions / Request** - Purpose, who they speak with, objectives, timezone, hard qualification floor.
2. **Greetings** - Exact opening line(s). One-liner the agent says first.
3. **Call Flow** - Ordered stages (Hook → Capture → Qualify → Book). Golden rules. No script lines here - just the order.
4. **Character** - Name, voice, personality, signature phrases, mindset.
5. **Transfer Call** - When/how to transfer to a human (or "N/A - booking only").
6. **Critical Instructions / Guardrails** - Hard rules, never-says, AI disclosure, silence handling, one-question-at-a-time, exit rules.
7. **Custom Field References** - Table of every variable captured + which CRM/GHL field it maps to + tags applied.
8. **What Your Company Does** - Elevator pitch the agent uses when asked. 1-2 versions.
9. **Script** - Literal spoken lines in order, with `~"..."` notation. This is the actual dialogue.
10. **Objection Handling** - Common objections + exact responses ("too expensive", "send me info", "not interested", "call me later", etc.).
11. **Booking flow** - GHL appointment booking steps: availability check → offer slots → confirm → `book_appointment_GHL_()` → success/error responses.
12. **FAQ / Knowledge Base** - Q&A list the agent can pull from for any off-script question.

---

## Standard Modules (include in every outbound agent)

- **iPhone Call Screening** (`MODULE-iphone-call-screening.md`) - Goes in **Critical Instructions / Guardrails**. Detects Apple iOS call screening, responds with name only, waits silently for a live human, and never pitches a robot. Required for all outbound agents.
- **AMD and Connection** (`MODULE-amd-and-connection.md`) - Goes in **Critical Instructions / Guardrails** for every outbound agent. Hang up immediately on voicemail and IVR. Do not talk into the mailbox. Do not count machine talk as success. One question at a time. Transfer when hot. Local caller ID and no CID blasting are ops notes, not spoken lines.
- **Sales Psychology Hooks** (`MODULE-sales-psychology-hooks.md`) - Reference library of openers, frameworks (Hormozi, Belfort, Sandler, SPIN, Cialdini, Voss), and mid-call power moves. Pull hooks from here into **Greetings** and **Script** sections.
- **Industry Discovery Questions** (`MODULE-industry-discovery-questions.md`) - Industry-specific discovery questions, pricing deflections, and consequence questions for 6 verticals (B2B SaaS, Insurance, HVAC/Home Services, Marketing Agency, Medical/Wellness, Real Estate). Pull from here into **Script** qualification sections. Includes universal consultative structure for unlisted verticals.
- **GHL Booking Flow** (`MODULE-ghl-booking-flow.md`) - Standard GHL calendar booking flow. Drop into **Booking flow** section for any prompt that books appointments.

## Generation System

- **Generation Engine** (`GENERATION-ENGINE.md`) - The complete instruction set for generating production-ready prompts. Section-by-section guide, quality checklist, and all non-negotiable rules.
- **Skill:** `/new-voice-ai-prompt` - Claude Code slash command that walks you through generating a prompt. Asks 7 questions, reads all reference files, and outputs a complete 12-section prompt.

---

## Authoring Rules
- **One question at a time.** Always. This is a core guardrail in the builder default.
- Use `~"..."` for spoken lines so the agent treats them as natural-language guides, not literal strings.
- Use `→` for actions (function calls, transitions, captures).
- Stutters and verbal tics belong in **Character**, not **Script**.
- Qualification gates / disqualification logic belong in **Call Flow** + **Script**, with exit copy in **Objection Handling** or a dedicated subsection of **Script**.
- Every captured field MUST appear in **Custom Field References** with its GHL mapping.
- Every function (`ghl_calendar_availability_`, `book_appointment_GHL_`, `create_or_update_contact_GHL_`, `tag_contact_GHL_`, `disqualify_contact_GHL_`) must be referenced in **Booking flow** or **Custom Field References**.

---

## Template Skeleton (copy this to start any new agent)

```
=== Project Instructions / Request ===
[Purpose, audience, objectives, timezone, hard qualification floor]

=== Greetings ===
~"[Opening line]"

=== Call Flow ===
Order: [Stage 1] → [Stage 2] → [Stage 3] → [Stage 4]
Golden Rules:
- [rule]
- [rule]

=== Character ===
Name: [Agent Name]
Voice: [tone, personality, tics]
Signature phrases: [...]

=== Transfer Call ===
[When to transfer / N/A]

=== Critical Instructions / Guardrails ===
- One question at a time. ALWAYS.
- Never say: [...]
- AI disclosure: [...]
- Silence >3s: [...]
- Exit rules: [...]

=== Custom Field References ===
| Variable | Source | GHL Field |
|---|---|---|
| {{first_name}} | Asked | contact.first_name |
| ... | ... | ... |

GHL Tags: [list]
Functions: [list]

=== What Your Company Does ===
~"[Elevator pitch]"

=== Script ===
🟢 GREETING
🟢 CAPTURE
🔴 QUALIFICATION GATES
🟢 PAIN DISCOVERY
🟡 BRIDGE TO BOOKING
🟢 CLOSE

=== Objection Handling ===
- "Too expensive" → ~"..."
- "Send me info" → ~"..."
- "Not interested" → ~"..."

=== Booking flow ===
Step 1: ghl_calendar_availability_({date})
Step 2: Offer 2 slots
Step 3: Confirm
Step 4: book_appointment_GHL_({time})
Success: ~"..."
Error: ~"..."

=== FAQ / Knowledge Base ===
Q: ...
A: ~"..."
```

---

**Rule going forward:** When James asks for a voice agent prompt, ALWAYS output it pre-sliced into these 12 sections, in this order, with section headers matching the builder UI exactly. Never output a monolithic prompt.
