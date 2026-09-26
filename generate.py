#!/usr/bin/env python3
"""
RizzDial Voice AI Prompt Maker (CLI)

Generates a complete, editable voice AI sales prompt in the canonical
12 section RizzDial structure, with the sales psychology engine baked in by name
(Time Contract, SPIN, Loss Aversion, Voss labeling, Takeaway, Assumptive Bridge,
Silence Bomb, emotional matching, one question at a time).

This is the prompt engineering method behind RizzDial, James Hill's commercial
AI calling platform for agencies and GoHighLevel users.
Framework: framework/00-RIZZDIAL-SECTION-STRUCTURE.md.

Website:  https://aiguyofficial.com
Platform: https://rizzdial.com

Usage:
  python3 generate.py                          Interactive mode
  python3 generate.py --vertical medspa        Build a ready made vertical prompt
  python3 generate.py --vertical hvac --out prompts/generated-examples/hvac.md
  python3 generate.py --non-interactive --company "Acme" --industry "roofing" \\
      --agent "Sam" --objective "book a roof inspection"

No third party dependencies. Python 3.11 or newer.
Notation: ~"..." spoken lines, the right arrow for actions, {{...}} for CRM variables.
"""

import argparse
import sys

SITE = "https://aiguyofficial.com"
PLATFORM = "https://rizzdial.com"
ARROW = "→"  # right arrow, the RizzDial action notation (not a dash)

# Industry discovery questions, lifted from MODULE-industry-discovery-questions.
VERTICALS = {
    "medspa": {
        "industry": "medical spa",
        "company": "Glow Aesthetics Medspa",
        "agent": "Mia",
        "offer": "a free consultation",
        "target": "people who want to look and feel confident",
        "outcome": "real, natural looking results from expert injectors",
        "differentiator": "a medical team that actually listens",
        "transfer": "a patient coordinator",
        "discovery": [
            "Have you had a treatment like this before, or would this be your first?",
            "What are you hoping to improve most?",
            "Any big event or date you are working toward?",
            "What has held you back from booking before now?",
        ],
        "loss_math": "What would you like to understand before deciding whether to book?",
        "faq": [
            ("How much does it cost?", "Great question. It depends on what you actually need, which is exactly what the free consult is for."),
            ("Does it hurt?", "The provider can explain the procedure and discuss your concerns."),
            ("Is this a real person?", "I am the AI assistant for the medspa, here to get you booked with the team."),
        ],
        "hipaa": False,
    },
    "hvac": {
        "industry": "HVAC and home services",
        "company": "Summit Heating and Air",
        "agent": "Sam",
        "offer": "a free estimate",
        "target": "homeowners who want a system that just works",
        "outcome": "comfort without the surprise breakdowns",
        "differentiator": "upfront pricing and techs who show up on time",
        "transfer": "the on call dispatcher",
        "discovery": [
            "Is this for a repair, or a system that is just getting old?",
            "How long has it been acting up?",
            "Any idea the last time it was serviced?",
            "Is it the whole house, or just one room that is off?",
        ],
        "loss_math": "The technician can assess the system and explain repair options.",
        "faq": [
            ("How much will it cost?", "The tech gives you an exact quote on site after a quick look, and the visit itself is a good first step."),
            ("How soon can you come?", "Let me check current availability with the team."),
            ("Is this a real person?", "I am the AI assistant for the company, here to get a technician scheduled for you."),
        ],
        "hipaa": False,
    },
    "healthcare": {
        "industry": "healthcare clinic",
        "company": "Lakeside Family Clinic",
        "agent": "Avery",
        "offer": "an appointment",
        "target": "patients who want to be seen and heard",
        "outcome": "care from a provider who takes the time",
        "differentiator": "short wait times and a caring team",
        "transfer": "the front desk team",
        "discovery": [
            "Is this a new concern, or something you have been managing for a while?",
            "Are you currently seeing anyone for it?",
            "How soon are you hoping to be seen?",
            "Is this covered by insurance, or self pay?",
        ],
        "loss_math": "The clinical team can help you decide the appropriate next step.",
        "faq": [
            ("What will it cost?", "Our billing team handles coverage details. I can have them follow up, or get the visit booked first."),
            ("Can you give me advice on my symptoms?", "I am not able to give medical guidance, the provider covers all of that at the visit."),
            ("Is this a real person?", "I am the clinic AI assistant, here to help you get scheduled."),
        ],
        "hipaa": True,
    },
    "insurance": {
        "industry": "insurance",
        "company": "Guardian Insurance Partners",
        "agent": "Casey",
        "offer": "a free coverage review",
        "target": "people who want the right coverage without overpaying",
        "outcome": "the right protection at a fair price",
        "differentiator": "an advisor who shops it for you",
        "transfer": "a licensed insurance advisor",
        "discovery": [
            "Do you have coverage right now, or shopping fresh?",
            "When does your current policy renew?",
            "What made you start looking?",
            "Anything your current policy is missing?",
        ],
        "loss_math": "An advisor can explain coverage options and any gaps in your current policy.",
        "faq": [
            ("What is the rate?", "The advisor gives you real quotes on the review. I cannot quote a binding rate, that would not be honest."),
            ("How long does the review take?", "About fifteen minutes, and you walk away knowing exactly where you stand."),
            ("Is this a real person?", "I am the AI assistant for the agency, here to book your review."),
        ],
        "hipaa": False,
    },
    "solar": {
        "industry": "solar",
        "company": "BrightPath Solar",
        "agent": "Riley",
        "offer": "a free savings estimate",
        "target": "homeowners tired of rising power bills",
        "outcome": "predictable energy costs and long term savings",
        "differentiator": "honest estimates with no high pressure",
        "transfer": "a solar advisor",
        "discovery": [
            "Do you own the home, or rent?",
        ],
        "loss_math": "The advisor can explain costs and eligibility using verified information.",
        "faq": [
            ("How much will I save?", "The advisor runs your real numbers on the estimate. I will not promise a figure I cannot back up."),
            ("Do I qualify?", "If you own the home, you are likely a fit. The estimate confirms it."),
            ("Is this a real person?", "I am the AI assistant for the company, here to set up your estimate."),
        ],
        "hipaa": False,
    },
    "real-estate": {
        "industry": "real estate",
        "company": "Coastline Realty Group",
        "agent": "Jordan",
        "offer": "a quick call with an agent",
        "target": "buyers and sellers who want a pro in their corner",
        "outcome": "the right move at the right time",
        "differentiator": "agents who know the local market cold",
        "transfer": "a licensed agent",
        "discovery": [
            "Are you looking to buy, sell, or both?",
            "What area are you focused on?",
            "What is your timeline to make a move?",
            "Have you been pre approved yet, or still early?",
        ],
        "loss_math": "The agent can discuss current listings and your timeline.",
        "faq": [
            ("What are your fees?", "The agent covers all of that on the call, and there is no cost to talk."),
            ("Are you an agent?", "I am the AI assistant for the group, here to connect you with a licensed agent."),
            ("Is this a real person?", "I am the team AI assistant, here to set up your call."),
        ],
        "hipaa": False,
    },
    "b2b-saas": {
        "industry": "B2B software",
        "company": "your platform",
        "agent": "Sam",
        "offer": "a short demo",
        "target": "teams stuck with tools that fight them",
        "outcome": "hours back every week and cleaner data",
        "differentiator": "it actually fits how your team already works",
        "transfer": "an account executive",
        "discovery": [
            "What are you using for this right now?",
            "Where does the current setup fall short?",
            "How many people on the team would touch this?",
            "What would solving this unlock for you?",
        ],
        "loss_math": "Every week on the old setup is hours your team will not get back, and the switch is easier than living with it.",
        "faq": [
            ("What does it cost?", "Pricing depends on your team size, which the demo scopes. I will not throw out a number that does not fit you."),
            ("How long is the demo?", "About twenty minutes, tailored to your stack, not a generic walkthrough."),
            ("Is this a real person?", "I am the company AI assistant, here to book your demo."),
        ],
        "hipaa": False,
    },
    "marketing-agency": {
        "industry": "marketing agency",
        "company": "your agency",
        "agent": "Casey",
        "offer": "a strategy call",
        "target": "business owners who want more booked calls",
        "outcome": "a pipeline that fills itself",
        "differentiator": "done for you systems, not just advice",
        "transfer": "a strategist",
        "discovery": [
            "What is your biggest bottleneck right now, leads or fulfillment?",
            "What are you spending on ads a month, ballpark?",
            "How are you handling follow up today?",
            "If you doubled booked calls, could you handle the volume?",
        ],
        "loss_math": "Leads you are not following up with fast are revenue walking out the door, and speed to lead is the cheapest win there is.",
        "faq": [
            ("How much do you charge?", "It depends on scope, which is exactly what the strategy call is for."),
            ("Do you guarantee results?", "The strategist gives you honest expectations on the call. I will not promise numbers I cannot back."),
            ("Is this a real person?", "I am the agency AI assistant, here to book your strategy call."),
        ],
        "hipaa": False,
    },
}

DEFAULT = {
    "industry": "general",
    "company": "Your Company",
    "agent": "Alex",
    "offer": "a quick call",
    "target": "your ideal customer",
    "outcome": "the result they want",
    "differentiator": "doing it right the first time",
    "transfer": "a team member",
    "discovery": [
        "What made you reach out today?",
        "How long has that been a problem?",
        "What is it costing you right now?",
        "If we fixed that, what would it mean for you?",
    ],
    "loss_math": "Every week you wait is another week the problem keeps costing you.",
    "faq": [
        ("How much does it cost?", "It depends on your situation, which is exactly why we book the call."),
        ("Is this a real person?", "I am the company AI assistant, here to get you booked with the team."),
    ],
    "hipaa": False,
}


def assemble(s):
    """Build the full 12 section RizzDial prompt with psychology baked in."""
    c = dict(DEFAULT)
    c.update(s)
    company = c["company"]
    agent = c["agent"]
    objective = c.get("objective") or ("book " + c["offer"])
    A = ARROW

    crit = [
        "HANG UP immediately if the first audio is voicemail, an answering machine, or an IVR menu. Do not talk into the mailbox. Do not leave a message.",
        "Hang-up phrases: your call has been forwarded, leave a message after the beep, the person you are trying to reach, you've reached the voicemail, press 1.",
        "Talking into voicemail is not a successful call. Real success is a booked appointment or a live transfer.",
        "iPhone screening (name and reason only, then silence): state your name, wait 30 seconds. If it becomes a mailbox, hang up.",
        "NEVER invent prices or make promises outside the script. If you do not know, say a specialist will follow up.",
        "ONE question at a time. Ask, then stop and wait for the answer. Never stack questions.",
        "Never interrogate before a micro-yes. If they are hot and a closer is available, transfer. Do not over-qualify.",
        "MATCH the caller energy (Emotional Intelligence). If they are rushed, get to the point. If chatty, warm up first.",
        "ALWAYS confirm the appointment time twice before ending.",
        "Speak numbers and times the way a person says them, for example two thirty in the afternoon.",
        "Honor any do not call or stop request immediately: record DNC status, stop persuasion, suppress future calls through the calling system, and end politely.",
        "At the start of the call, say plainly that you are an AI assistant. Never claim to be a human.",
    ]
    if c["hipaa"]:
        crit.append("NEVER give medical advice. Collect only what is needed to schedule. If it sounds like an emergency, tell them to call local emergency services or go to the nearest ER, then end.")

    # Build the Script section with named psychology hooks
    d = c["discovery"]
    script = []
    script.append('~"Hi, is this {{contact.first_name}}?"')
    script.append("  [WAIT. Handle the iPhone screening pause: if silence, re-greet warmly once.]")
    script.append('~"Hey {{contact.first_name}}, this is ' + agent + " at " + company + ". You reached out about " + c["offer"] + ', perfect timing. Do you have seventeen seconds?"')
    script.append("  [Time Contract: the odd number feels precise and honest, not salesy.]")
    script.append("IF yes " + A)
    script.append('  ~"Awesome. Mind if I ask you one quick thing?"')
    script.append("  [Permission Close: a small yes that lowers resistance to the next.]")
    script.append('  ~"' + d[0] + '"')
    script.append("  [SPIN Situation. WAIT. Mirror their words back before the next question.]")
    if len(d) > 1:
        script.append('  ~"' + d[1] + '"')
        script.append("  [SPIN Problem. WAIT.]")
    if len(d) > 2:
        script.append('  ~"' + d[2] + '"')
        script.append("  [SPIN Implication. WAIT.]")
    if len(d) > 3:
        script.append('  ~"' + d[3] + '"')
        script.append("  [SPIN Need-payoff. WAIT.]")
    script.append('~"It sounds like this has been weighing on you for a bit."')
    script.append("  [Chris Voss Labeling: name the emotion to defuse it and build trust.]")
    script.append('~"' + c["loss_math"] + '"')
    script.append("  [Loss Aversion: make the cost of doing nothing concrete.]")
    script.append('~"Here is what I would suggest, based on what you just told me..."')
    script.append("  [Pitch tied directly to their answers, never generic.]")
    script.append('~"Honestly, this might not even be a fit for you, and that is okay."')
    script.append("  [Takeaway: removing the offer triggers desire.]")
    script.append('~"Tell you what, let us grab a quick time. {{slot_one}} or {{slot_two}}?"')
    script.append("  [Assumptive Bridge: replace the yes/no with an easy either/or.]")
    script.append('~"Before I lock it in, anything I did not cover that is on your mind?"')
    script.append("  [Silence Bomb: ask, then say NOTHING. Let the silence do the work.]")
    script.append(A + " {{ghl_calendar_availability_}}")
    script.append(A + " {{book_appointment_GHL_}}")
    script.append('~"Perfect, you are all set for {{appointment_time}}. That is {{appointment_time}}, correct?"')
    script.append("  [Confirm twice. Then a warm close.]")
    script.append('~"You will get a text confirmation. Talk soon, {{contact.first_name}}."')

    objections = [
        ('"I am not interested"', '~"Totally fair, most folks say that before they hear how fast this actually works. Can I take seventeen seconds?"'),
        ('"How did you get my info?"', '~"You reached out about ' + c["offer"] + ' just now, that is the only reason I am calling."'),
        ('"I am busy right now"', '~"I hear you, seventeen seconds and I will let you go. Fair?"  [Time Contract again]'),
        ('"Just send me an email or text"', '~"Happy to send something over. While I have you, one quick question so I send the right thing..."'),
        ('"How much is it?"', '~"Great question, and an honest answer is it depends on your situation, which is exactly what the ' + c["offer"].replace("a ", "").replace("an ", "") + ' is for."'),
    ]

    P = []
    P.append("# RizzDial Voice AI Prompt: " + company + " (" + c["industry"] + ")")
    P.append("")
    P.append("Built on the canonical 12 section prompt structure with the sales psychology engine baked in.")
    P.append("This is the prompt engineering method behind RizzDial, a commercial AI calling platform for agencies and GoHighLevel users.")
    P.append("Free resources and templates at " + SITE + ". RizzDial is a commercial platform at " + PLATFORM + ".")
    P.append("")
    P.append("Notation: ~\"...\" is spoken out loud, " + A + " is a system action, {{...}} is a CRM variable.")
    P.append("")
    P.append("---")
    P.append("")
    P.append("## 1. Project Instructions")
    P.append("```")
    P.append("You are " + agent + ", the voice AI assistant for " + company + ".")
    P.append("Your job is to " + objective + ".")
    P.append("You are speaking with {{contact.first_name}}.")
    P.append("Use conversational techniques on purpose, but never sound like a script.")
    P.append("```")
    P.append("")
    P.append("## 2. Greetings")
    P.append("```")
    P.append('~"Hi, is this {{contact.first_name}}?"')
    P.append("  [Handle the iPhone screening pause. If silence, WAIT 2 seconds, then a warm re-greet.]")
    P.append('~"Hello? Can you hear me okay? It is just ' + agent + " from " + company + '."')
    P.append('~"Quick disclosure: I am an AI assistant, not a person. I can still get you taken care of."')
    P.append("  [AI disclosure: state it plainly, once, early. Never deny being AI if asked again.]")
    P.append("```")
    P.append("")
    P.append("## 3. Call Flow")
    P.append("```")
    P.append("1. Confirm identity (handle screening pause)")
    P.append("2. Time Contract opener (seventeen seconds)")
    P.append("3. Permission to continue (micro-yes)")
    P.append("4. SPIN discovery (one question at a time)")
    P.append("5. Label the emotion, then Loss Aversion math")
    P.append("6. Pitch tied to their answers")
    P.append("7. Takeaway, then Assumptive Bridge to booking")
    P.append("8. Silence Bomb, then book and confirm twice")
    P.append("9. Warm close")
    P.append("```")
    P.append("")
    P.append("## 4. Character")
    P.append("```")
    P.append("Warm, confident, sharp. Speaks in short sentences. One question at a time.")
    P.append("Matches the caller energy and pace. Sounds like a skilled closer, who")
    P.append("happens to respect your time. Never robotic, never pushy, never reads like a script.")
    P.append("```")
    P.append("")
    P.append("## 5. Transfer Call")
    P.append("```")
    P.append("IF the caller is hot and " + c["transfer"] + " is available " + A)
    P.append('  ~"Honestly, you should talk to ' + c["transfer"] + ' right now, let me connect you."')
    P.append("  " + A + " {{transfer_call_}}")
    P.append("```")
    P.append("")
    P.append("## 6. Critical Instructions")
    P.append("```")
    for line in crit:
        P.append(line)
    P.append("```")
    P.append("")
    P.append("## 7. Custom Field References")
    P.append("```")
    P.append("{{contact.first_name}}, {{contact.last_name}}, {{contact.email}}, {{contact.phone}}")
    P.append("{{appointment_time}}, {{slot_one}}, {{slot_two}}, {{location.calendar_name}}")
    P.append("```")
    P.append("")
    P.append("## 8. What Your Company Does")
    P.append("```")
    P.append(company + " helps " + c["target"] + " get " + c["outcome"] + ".")
    P.append("Known for " + c["differentiator"] + ".")
    P.append("```")
    P.append("")
    P.append("## 9. Script")
    P.append("```")
    for line in script:
        P.append(line)
    P.append("```")
    P.append("")
    P.append("## 10. Objection Handling")
    P.append("```")
    for o, r in objections:
        P.append(o + " " + A)
        P.append("  " + r)
    P.append("```")
    P.append("")
    P.append("## 11. Booking/Calendar")
    P.append("```")
    P.append(A + " {{ghl_calendar_availability_}}")
    P.append('  ~"I have {{slot_one}}, or {{slot_two}}. Which works better?"')
    P.append(A + " {{book_appointment_GHL_}}")
    P.append('  ~"You are booked for {{appointment_time}}. Confirm: that is correct, yes?"')
    P.append("  [Always confirm twice. Never double book. Swap the function names for your calendar stack.]")
    P.append("```")
    P.append("")
    P.append("## 12. FAQ")
    P.append("```")
    for q, a in c["faq"]:
        P.append("Q: " + q)
        P.append('A: ~"' + a + '"')
    P.append("```")
    P.append("")
    P.append("---")
    P.append("From the voice-agent-prompts library by James Hill (The AI Guy), MIT licensed. " + SITE + " | " + PLATFORM)
    P.append("")
    return "\n".join(P)


def ask(prompt, default):
    raw = input(prompt + " [" + str(default) + "]: ").strip() if default else input(prompt + ": ").strip()
    return raw if raw else default


def interactive():
    print("")
    print("RizzDial Voice AI Prompt Maker by James Hill (The AI Guy)")
    print("Outputs the real 12 section structure with the psychology engine baked in.")
    print(SITE + "  |  " + PLATFORM)
    print("")
    vk = ask("Vertical (" + ", ".join(VERTICALS.keys()) + ", or custom)", "custom")
    s = dict(VERTICALS.get(vk, {}))
    s["company"] = ask("Company name", s.get("company", DEFAULT["company"]))
    s["industry"] = ask("Industry", s.get("industry", DEFAULT["industry"]))
    s["agent"] = ask("Agent name", s.get("agent", DEFAULT["agent"]))
    s["offer"] = ask("Offer (the reason to act now)", s.get("offer", DEFAULT["offer"]))
    s["objective"] = ask("Primary objective", "book " + s.get("offer", DEFAULT["offer"]))
    s["transfer"] = ask("Transfer target", s.get("transfer", DEFAULT["transfer"]))
    return s


def settings_from_args(args):
    if args.vertical:
        key = args.vertical.lower()
        if key not in VERTICALS:
            print("Unknown vertical: " + key, file=sys.stderr)
            print("Available: " + ", ".join(VERTICALS.keys()), file=sys.stderr)
            sys.exit(2)
        s = dict(VERTICALS[key])
        for field in ("company", "industry", "agent", "offer", "objective", "transfer"):
            value = getattr(args, field)
            if value is not None:
                s[field] = value
        if args.hipaa:
            s["hipaa"] = True
        return s
    s = {}
    if args.company:
        s["company"] = args.company
    if args.industry:
        s["industry"] = args.industry
    if args.agent:
        s["agent"] = args.agent
    if args.offer:
        s["offer"] = args.offer
    if args.objective:
        s["objective"] = args.objective
    if args.transfer:
        s["transfer"] = args.transfer
    if args.hipaa:
        s["hipaa"] = True
    return s


def main():
    p = argparse.ArgumentParser(description="RizzDial Voice AI Prompt Maker: 12 section structure with sales psychology baked in. By James Hill (The AI Guy).")
    p.add_argument("--vertical", help="Ready made vertical: " + ", ".join(VERTICALS.keys()))
    p.add_argument("--non-interactive", action="store_true")
    p.add_argument("--out", help="Output file (default your-rizzdial-prompt.md)")
    p.add_argument("--company")
    p.add_argument("--industry")
    p.add_argument("--agent")
    p.add_argument("--offer")
    p.add_argument("--objective")
    p.add_argument("--transfer")
    p.add_argument("--hipaa", action="store_true")
    p.add_argument("--print", dest="to_stdout", action="store_true")
    args = p.parse_args()

    if args.vertical or args.non_interactive:
        s = settings_from_args(args)
    else:
        s = interactive()

    prompt = assemble(s)

    if args.to_stdout:
        print(prompt)
        return
    out = args.out or "your-rizzdial-prompt.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write(prompt)
    print("Saved your RizzDial voice AI prompt to: " + out)
    print("Run prompts like this at scale on RizzDial. " + PLATFORM)


if __name__ == "__main__":
    main()
