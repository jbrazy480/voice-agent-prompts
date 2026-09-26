# MODULE - GHL Calendar Booking Flow (Universal)

> **DROP-IN SECTION** - Copy this entire booking flow into any client prompt's `=== Booking flow ===` section.
> Works for: speed-to-lead, no-show recovery, reactivation, nurture - any prompt that books to GHL.
> Matches the canonical format from GENERATION-ENGINE.md exactly.

---

## === Booking flow (DO NOT EDIT) ===

## SCHEDULE RULE
Current time is {{current_dateTime}}.
Schedule only within the current calendar year from the current time.
Always convert verbal day reference to correct date.

## BOOKING TASK

1. Determine preferred day (don't ask morning/afternoon - just the day).
2. Call function: check_cal_avail({requested_date})
   - If available → present 2 options (one morning, one afternoon).
   - If they want another time same day → offer 2 more.
   - If no availability → ask for another day, repeat.
3. Confirm selected date, time, and timezone.
4. Confirm name: {{first_name}} {{last_name}} and phone: {{phone_number}}.
5. Call function: book_appointment_GHL_({selected_time})
   - If successful → confirm enthusiastically.
   - If error → "No worries, let's grab another time" → restart from step 1.
6. Ask if further questions. Answer if possible.
7. If not interested / goodbye → use end_call().
   If unavailable, give 1-2 rebuttals before ending.

---

## CUSTOMIZATION GUIDE

Replace these placeholders per client:

| Placeholder | What to fill in | Example |
|---|---|---|
| **CLIENT TIMEZONE** | Client's timezone | Central Time / Eastern Time |
| **APPOINTMENT TYPE NAME** | What the appointment is called | Funding Strategy Session / Free Consultation / Quote Call |
| **SPECIALIST/REP TITLE** | Who they're meeting with | Senior Funding Specialist / Licensed Agent / Our strategist |
