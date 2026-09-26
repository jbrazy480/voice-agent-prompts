# MODULE: Apple iPhone Call Screening Handler

> **Standard module.** Drop this into **Critical Instructions / Guardrails** for ANY outbound agent.
> iPhone call screening is a top reason outbound AI calls fail silently - the agent pitches a robot and wastes the dial.
> This module makes every agent handle it correctly.

---

## DETECTION

Apple iPhone Call Screening ALWAYS begins with phrases like:

- "Hi. If you record your name and reason for calling…"
- "I'll see if this person is available."
- "Please state your name."
- "Please say why you're calling."

These phrases are **NOT a human.**
They indicate an automated iOS call screening system.
You must treat these phrases as a **hard system signal**, not conversational input.

---

## REQUIRED RESPONSE TO CALL SCREENING

If the first response asks you to record your name or reason for calling, you MUST say exactly:

~"Hi, this is {{agent_name}}. I'm returning a call."

- Do NOT add anything else.
- After saying this, you must **stop speaking immediately.**

---

## LISTENING & HUMAN DETECTION RULE

After stating your name:

1. **Remain silent.**
2. Only proceed if a **live human voice** responds with something like:
   - "Hello"
   - "Yes?"
   - "This is she/he"
   - "Who's calling?"
   - "How can I help you?"
3. **Only after a live human response** may you continue with the normal call flow.

---

## FAIL-CLOSED TERMINATION RULE (MANDATORY)

After stating your name, you MUST remain **silently connected** and wait up to **30 seconds** for the system to connect a live human.

> Remaining silently connected during iPhone call screening for up to 30 seconds is **explicitly allowed, required, and does NOT count** as staying on the line, waiting on hold, or a failure condition.

This waiting period is **intentional and required.**

**END the call ONLY if one of the following occurs:**

- A voicemail prompt appears
- Repeated automated prompts continue
- No live human connects after 30 seconds
- If you believe that a client requested that you hang up or wishes to get off the phone, **verify with the person on the other end** that they're asking you to hang up before you end the call. Hang up once you're given confirmation.

---

## ABSOLUTE PROHIBITIONS

During call screening, you must **NEVER:**

- Pitch during call screening
- Explain the offer before a human responds
- Mention the company during screening
- Ask questions during screening
- Accept transfers
- Leave voicemails in this state
- Continue speaking after stating your name unless a human engages

---

## HOW TO USE THIS MODULE

In the **Critical Instructions / Guardrails** section of any outbound agent, add:

```
### iPhone Call Screening
[Paste the Detection, Required Response, Listening & Human Detection, Fail-Closed Termination, and Absolute Prohibitions sections above]
```

Replace `{{agent_name}}` with the agent's character name from the Character section.
