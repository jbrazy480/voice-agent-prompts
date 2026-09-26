# Field-tested library

Production-shaped 12-section prompts, generalized from real call patterns for live transfer and appointment conversations. Client names, clinic names, doctor names, cities-as-brands, and phone numbers were stripped. Generic verticals only: medspa, medical practice, dental.

These files do not replace [templates/](../../templates/) (keep those as they are). They also do not replace the generated examples in [generated-examples/](../generated-examples/). Use this folder when you want a short, transfer-when-hot pattern that held up in real use.

MIT. Same license as the rest of this repo. See [LICENSE](../../LICENSE).

Full writeup: [WHY-THEY-WORK.md](WHY-THEY-WORK.md).

---

## When to use each

| File | Call type | Use when | Pattern |
|---|---|---|---|
| [01-inbound-medspa-transfer.md](01-inbound-medspa-transfer.md) | inbound | Inbound medspa. Human already called. Transfer to scheduling when hot. Two-slot if they want a time. | Transfer-when-hot |
| [02-outbound-medspa-two-slot.md](02-outbound-medspa-two-slot.md) | outbound-optin | Outbound medspa specials. Confirm name. One-line offer. Two named slots. Transfer if they want a person. | Two-slot offer |
| [03-inbound-medical-social.md](03-inbound-medical-social.md) | inbound | Inbound medical / telemed from social ads. HIPAA-aware. Transfer to front desk when hot. | Social inbound |
| [04-outbound-medical-reactivation.md](../reactivation/04-outbound-medical-reactivation.md) | reactivation | Outbound medical check-in or social follow-up. Confirm name. Do not interrogate. Two slots or transfer. | Reactivation |
| [05-inbound-dental.md](05-inbound-dental.md) | inbound | Inbound dental front desk. Emergency vs consult fork. Transfer emergencies immediately. Two-slot the rest. | Emergency fork |
| [06-outbound-dental-reactivation.md](../reactivation/06-outbound-dental-reactivation.md) | reactivation | Outbound dental recall / database reactivation. Confirm name. Two slots. Never talk into a machine. | Database recall |

Every file uses all 12 sections in order. Notation: `~"..."` spoken, right arrow for actions, `{{...}}` CRM. Booking uses `{{ghl_calendar_availability_}}` then `{{book_appointment_GHL_}}` (optional integration, swap-able).

---

## House rules for this folder

- All 12 sections, this order: Project Instructions, Greetings, Call Flow, Character, Transfer Call, Critical Instructions, Custom Field References, What Your Company Does, Script, Objection Handling, Booking and Calendar, FAQ.
- Named psychology baked in: Time Contract, Permission Close, SPIN, Loss Aversion, Chris Voss labeling, the Takeaway, Assumptive Bridge, Silence Bomb, emotional matching, one question at a time.
- No em dashes or en dashes.
- No real customer names, phone numbers, clinic names, doctor names, or production company names.
- No fabricated performance numbers. Describe what worked qualitatively; do not invent call counts, transfer rates, or percentages.
- No machine-detection / voicemail talk tracks here. That is a separate template (`modules/MODULE-amd-and-connection.md`).
- Every outbound and reactivation file includes a truthful AI disclosure line and a do-not-call / opt-out handling line.
