# RizzDial Master AI Agent Prompt Templates

Source: "Copy of AI Agent Templates (1).pdf" - official RizzDial voice agent templates for app.Rizzdial.com.

## Purpose
Reference library for building high-converting voice AI agents. Use these as the skeleton for every new client build. Upload finished prompts into the agent on app.Rizzdial.com.

## Template Library
1. [01 - Speed to Lead - Live Transfer Only](01-speed-to-lead-live-transfer.md)
2. [02 - Speed to Lead - Appointment Booking Only](02-speed-to-lead-booking.md)
3. [03 - Speed to Lead - Booking + Live Transfer](03-speed-to-lead-both.md)
4. [04 - No-Show Recovery](04-no-show-recovery.md)
5. [05 - 360 Nurture](05-360-nurture.md)
6. [06 - Annual Re-engagement](06-annual-reengagement.md)
7. [07 - 2 Hour Appointment Reminder](07-appointment-reminder-2hr.md)
8. [08 - Post-Sale Welcome Call](08-post-sale-welcome.md)
9. [09 - Appointment No-Show (v2)](09-appointment-no-show-v2.md)
10. [10 - Database Reactivation](10-database-reactivation.md)
11. [11 - Webinar / Event Invite](11-webinar-invite.md)
12. [12 - Inbound Receptionist Booking](12-inbound-receptionist-booking.md)
13. [13 - Short Outbound Closer](13-short-outbound-closer.md)
14. [14 - Transfer When Hot](14-transfer-when-hot.md)

12 through 14 are the live-call set. Inbound books in under 2 minutes. Outbound is name, one why, one qualifier, two slots. Transfer-when-hot treats a yes as a conversion. All outbound templates hang up on voicemail (see `modules/MODULE-amd-and-connection.md`).

## Editing Rules (from source doc)
- **GREEN sections** = variables to customize per business (BUSINESS NAME, AGENT NAME, PAIN POINT, PRODUCT/SERVICE, TIME ZONE, elevator pitch, qualifying questions, etc.)
- **RED sections** = DO NOT EDIT - proven transfer/booking/scheduling logic
- Keep calls under **90 seconds** on speed-to-lead
- Every template follows: Greeting → Reintroduction → Qualification/Interest → Transfer or Book → Exit

## Intake Checklist - Variables to Collect Per Client
Before building any prompt, get these from the client:

**Business**
- BUSINESS NAME
- Elevator pitch (15-20 sec)
- Why clients choose them over competitors
- Website
- Location
- Office hours + time zone
- Business days/hours for transfer windows

**Agent Persona**
- AGENT NAME
- How to answer "Are you AI?" (truthful disclosure vs. deflection - depends on compliance)

**Offer & Pain**
- PRODUCT / SERVICE
- PAIN POINT
- DESIRED RESULT
- What form they filled out / why
- Annual offer details (for re-engagement)

**Qualification**
- 3 qualifying questions
- Lead capture fields (beyond name/phone)

**Routing**
- INDUSTRY REP title (who the transfer goes to)
- Transfer number
- Calendar for booking

**Objections & FAQ**
- Industry-specific objections + responses
- Common FAQs

## Build Workflow (use this every time)
1. Pick the right template for the use case (speed-to-lead, DR, no-show, etc.)
2. Copy the template
3. Fill in every GREEN variable from the intake checklist
4. Leave all RED sections untouched
5. Add industry-specific objections to the objection block
6. Paste into the agent on app.Rizzdial.com
7. Test with a live call before deploying to traffic

## System Notes
- These prompts are optimized for GHL integration (calendar functions: `check_cal_avail`, `book_appointment`, `ghl_calendar_availability_`, `book_appointment_GHL_`)
- CRM variables use `{{first_name}}`, `{{current_dateTime}}`, `{{name}}`, `{{phone}}`, `{{appointment_date_and_time}}`
- Always check `{{current_dateTime}}` before transferring or booking
