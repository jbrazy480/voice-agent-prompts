# Build-a-Bot - Dev Spec v1

> **Goal:** A client calls the Build-a-Bot intake agent. 15 minutes later, a new sectioned prompt is auto-populated into a fresh RizzDial agent, ready to deploy. No ChatGPT, no manual prompt writing.

> **CRM:** GoHighLevel (GHL). Clients map the GHL custom fields they want the AI to reference.

---

## 1. Architecture Overview

```
[Client] --calls--> [Build-a-Bot Intake Agent (RizzDial)]
                            |
                            | (conversational slot-filling)
                            v
                    [GHL Custom Fields]  <-- source of truth during build
                            |
                            | (on call end, webhook)
                            v
            [Prompt Assembly Service]  <-- deterministic find-and-replace
                            |
                            | (12 sections filled)
                            v
              [RizzDial Agent API]  <-- creates/updates sectioned prompt
                            |
                            v
               [New Agent ready to test via "Talk With Agent"]
```

---

## 2. Sectioned Prompt Structure (from RizzDial UI)

Every agent prompt in RizzDial is broken into 12 sections. The Build-a-Bot must produce **one output per section**. These are the exact sections to target:

| # | Section Name | Content Type |
|---|---|---|
| 1 | Project Instructions / Request | Paragraph - mission, who they call, objectives |
| 2 | Greetings | 1-2 lines - opener |
| 3 | Call Flow | Ordered step list |
| 4 | Character | Agent persona + rules |
| 5 | Transfer Call | Transfer logic (DO NOT EDIT block from templates) |
| 6 | Critical Instructions / Guardrails | Hard rules + guardrails |
| 7 | Custom Field References | List of GHL `{{variables}}` the agent uses |
| 8 | What Your Company Does | Elevator pitch + follow-up |
| 9 | Script | Full scripted dialogue with emoji-tagged steps |
| 10 | Objection Handling | Q/A pairs |
| 11 | Booking Flow | Scheduling task logic (DO NOT EDIT block) |
| 12 | FAQ / Knowledge Base | Q/A pairs |

**Available GHL custom fields (already wired in RizzDial):**
`{{first_name}}, {{last_name}}, {{phone_number}}, {{company_name}}, {{address}}, {{city}}, {{state}}, {{postal_code}}, {{industry}}, {{website}}, {{email}}, {{highest_level_of_contact}}, {{company_domain}}, {{company_linkedin_url}}, {{offer_details}}, {{current_dateTime}}, {{join_meeting_pin}}`

---

## 3. The Slot Schema (single source of truth)

This is the JSON the Build-a-Bot must collect. Every slot maps to one or more sections. The intake agent's job = fill this schema via conversation.

```json
{
  "business": {
    "business_name": "string (required)",
    "industry": "string (required)",
    "website": "string",
    "location_city_state": "string",
    "timezone": "string (required, e.g. America/Chicago)",
    "business_hours": "string (required, e.g. Mon-Fri 9am-6pm CT)",
    "business_days": "string"
  },
  "agent_persona": {
    "agent_name": "string (required)",
    "voice_gender": "male|female",
    "ai_disclosure_answer": "string (required - how to answer 'Are you AI?')",
    "tone": "warm|direct|professional|casual"
  },
  "offer": {
    "product_service": "string (required)",
    "pain_point": "string (required)",
    "desired_result": "string (required)",
    "elevator_pitch": "string (required, 15-20 sec)",
    "differentiator": "string (required - why choose you over competitors)",
    "form_reason": "string (why they filled out the form)"
  },
  "qualification": {
    "qualifying_question_1": "string (required)",
    "qualifying_question_2": "string (required)",
    "qualifying_question_3": "string (required)",
    "lead_capture_fields": "string[] (what to capture in CRM)"
  },
  "routing": {
    "use_case": "speed_to_lead_transfer | speed_to_lead_booking | both | no_show | nurture | reengagement | reminder | welcome | database_reactivation",
    "industry_rep_title": "string (e.g. licensed agent, strategist)",
    "transfer_number": "string",
    "calendar_id": "string (GHL calendar)"
  },
  "objections": [
    {"question": "string", "response": "string"}
  ],
  "faq": [
    {"question": "string", "response": "string"}
  ],
  "ghl_field_mapping": {
    "description": "array of GHL custom field keys the client wants the agent to reference",
    "fields": "string[]"
  }
}
```

**Required vs optional:** fields marked `(required)` block agent publish. Optional fields get sensible defaults from the vertical template pack.

---

## 4. Intake Agent Behavior (the Build-a-Bot itself)

The Build-a-Bot is a RizzDial voice agent built with **our own templates**. Its job:

**Opening**
> "Hey, this is your RizzDial Build-a-Bot. I'm going to ask you about 15 questions and by the end you'll have a fully trained AI voice agent ready to deploy. It takes about 15 minutes. Ready to start?"

**Interview rules:**
- Walk the slot schema in order: Business → Persona → Offer → Qualification → Routing → Objections → FAQ
- **One question at a time** (same golden rule as our templates)
- Confirm back after each section: "So your business is X, you're located in Y, you help people with Z - got it right?"
- If slot empty/vague → re-ask with an example
- If client says "I don't know" → offer a smart default from the vertical pack
- Use examples from similar businesses: "Most medspas we work with capture name, email, which service they're interested in. Want to use those?"

**Auto-extract before call (v2):**
- Scrape `website` → pre-fill elevator_pitch, services, differentiator
- Pull GHL sub-account → pre-fill business_name, hours, calendar_id
- The call becomes **confirmation**, not data entry

**End of call:**
> "Perfect. I'm building your agent now. In about 60 seconds it'll show up in your RizzDial dashboard. Click 'Talk With Agent' to test it, and if anything's off, just tell it what to fix."

---

## 5. Data Storage During Intake

All slot answers write to GHL custom fields on the **client's contact record** (the business owner) in real time as the intake agent captures them. Use a naming convention:

```
bab_business_name
bab_agent_name
bab_pain_point
bab_product_service
bab_qualifying_q1
bab_qualifying_q2
bab_qualifying_q3
bab_elevator_pitch
bab_differentiator
bab_use_case
bab_objections_json
bab_faq_json
bab_ghl_field_mapping_json
... etc
```

**Why GHL fields and not a DB table?** Zero new infra. GHL is already the source of truth. Webhooks and workflows can react to field updates natively.

---

## 6. Prompt Assembly Service (the deterministic core)

**Input:** slot schema JSON (pulled from GHL custom fields at end of intake call)
**Output:** 12 section strings, one per sectioned prompt field

**Algorithm:** find-and-replace. Not LLM. Deterministic.

### Template files needed
Dev team takes the 10 existing templates in this folder and converts GREEN variables to mustache slots. Example - `01-speed-to-lead.template.json`:

```json
{
  "project_instructions": "Your purpose is simple: Call leads that filled out a lead inquiry form... You work for {{business_name}} helping people with {{pain_point}}...",
  "greetings": "~\"Hi, is this {{first_name}}?\"",
  "call_flow": "Order: Introduction → Quick Qualification → Information Capture → Transfer or Appointment\n\nGolden Rules:\n- Keep tone professional but warm - {{industry}} vibe\n...",
  "character": "Your name is {{agent_name}}. You are a {{industry}} specialist...",
  "transfer_call": "[DO NOT EDIT BLOCK - pasted verbatim from template]",
  "critical_instructions": "...",
  "custom_field_references": "{{ghl_field_mapping}}",
  "what_your_company_does": "→ ~\"{{elevator_pitch}}\"\nAlt: → ~\"{{differentiator}}. Does that make sense?\"",
  "script": "🟢 GREETING\n~\"Hi, is this {{first_name}}?\"\n\n~\"Hi {{first_name}}, this is {{agent_name}} calling from {{business_name}}. I had just a second to get back to you about {{form_reason}}...\"\n\n🟠 QUALIFYING QUESTIONS\n~\"{{qualifying_question_1}}\"\n~\"Perfect! {{qualifying_question_2}}\"\n~\"{{qualifying_question_3}}\"\n...",
  "objection_handling": "{{objections_rendered}}",
  "booking_flow": "[DO NOT EDIT BLOCK - pasted verbatim]",
  "faq_knowledge_base": "OFFICE HOURS: {{business_hours}}\n\n{{faq_rendered}}"
}
```

### Assembly steps
1. Pick template file based on `routing.use_case`
2. For each of the 12 section strings: run mustache replace with slot values
3. For `objections` and `faq` arrays: render each Q/A as `Q: {question}\n→ {response}\n\n`
4. For `ghl_field_mapping`: render as a comma-separated list of `{{field}}` tokens
5. Return 12 finished strings

**No LLM in this step.** Deterministic = debuggable + free + fast.

---

## 7. RizzDial Agent API Integration

**Endpoint needed (dev team to confirm exists or build):**
- `POST /api/agents/create` - create a new agent with sectioned prompt
- `PATCH /api/agents/{agent_id}/sections` - update individual sections
- Payload shape: `{ agent_name, folder_id, ghl_location_id, timezone, sections: { project_instructions, greetings, call_flow, character, transfer_call, critical_instructions, custom_field_references, what_your_company_does, script, objection_handling, booking_flow, faq_knowledge_base } }`

**If API doesn't exist yet:** this is the blocker. Build it first. Everything else depends on programmatic agent creation.

---

## 8. End-to-End Flow

1. Client buys RizzDial → GHL contact created
2. Workflow auto-calls them from the Build-a-Bot agent (`bab_status = pending`)
3. Build-a-Bot runs interview → writes answers to `bab_*` GHL fields one by one
4. On call end: webhook fires → `POST /build-a-bot/assemble` with `contact_id`
5. Assembly service reads all `bab_*` fields from GHL → runs find-and-replace → gets 12 section strings
6. Assembly service calls RizzDial Agent API → creates new agent in client's account
7. Webhook responds back → GHL workflow sends client an SMS: *"Your agent is ready! Click here to test it: [link to RizzDial agent page]"*
8. Client clicks "Talk With Agent" → tests it live
9. (v2) Correction loop: supervisor agent listens, owner says "fix this," relevant section gets patched

---

## 9. Build Order for Dev Team

**Week 1 - Foundation**
- [ ] Confirm or build RizzDial Agent Creation API (`POST /agents`, sectioned prompt payload)
- [ ] Create `bab_*` custom fields in GHL (script or manual)
- [ ] Convert Template 01 (Speed-to-Lead Live Transfer) to `01-speed-to-lead.template.json` with mustache slots
- [ ] Build Prompt Assembly Service (Node or Python, single endpoint, deterministic)
- [ ] Write the Build-a-Bot intake agent prompt (uses our own sectioned prompt structure, slot-filling via tool calls that write to GHL fields)

**Week 2 - Wiring**
- [ ] GHL workflow: on new client → trigger Build-a-Bot call
- [ ] Webhook on intake call end → assembly service → RizzDial API
- [ ] SMS notification back to client with agent link
- [ ] End-to-end test with a real client

**Week 3 - Second use case**
- [ ] Convert Template 02 (Speed-to-Lead Booking) + add inbound use case
- [ ] Add use case selection to the intake flow ("Do you want to transfer live, book appointments, or both?")

**Week 4 - v2**
- [ ] Website auto-scrape pre-fill
- [ ] Vertical template packs (medspa first)
- [ ] Live correction loop via "Talk With Agent"

---

## 10. Acceptance Criteria (v1)

- [ ] A non-technical business owner can call the Build-a-Bot, have a 15-minute conversation, and hang up with a fully populated sectioned prompt visible in their RizzDial dashboard
- [ ] All 12 sections are filled
- [ ] All mustache slots are replaced (no literal `{{business_name}}` text in final output)
- [ ] The resulting agent passes a test call with correct name, company, qualifying questions, and transfer behavior
- [ ] Total time from first ring to deployed agent: **under 20 minutes**
- [ ] Zero human touchpoints required between intake call end and client testing their agent

---

## 11. Open Questions for Dev Team

1. Does RizzDial expose an agent creation API today? If not, that's the first thing to build.
2. Can RizzDial agents be triggered to call a GHL contact via API, or does the Build-a-Bot need to be initiated manually by the client (inbound to a RizzDial number)?
3. Where should the Assembly Service live - existing RizzDial backend, separate Node service on Railway, or Cloudflare Worker?
4. Who owns the Build-a-Bot intake agent's ongoing maintenance - is it a template inside RizzDial that we edit like any other agent, or is it hard-coded?

---

## 12. Files in this Folder (for reference)
- `README.md` - overall system + intake checklist
- `01-speed-to-lead-live-transfer.md` through `10-database-reactivation.md` - source templates (GREEN = variables, RED = do not edit)
- `BUILD-A-BOT-DEV-SPEC.md` - this file

**Next file to produce:** `01-speed-to-lead.template.json` - the first template with mustache slots, ready for the Assembly Service to consume. Say the word and I'll build it.
