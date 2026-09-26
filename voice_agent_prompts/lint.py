"""Heuristic content checks, not a legal or behavioral certification."""
from dataclasses import dataclass
import re

# Escaped spellings keep restricted vocabulary out of the shipped prose.
FORBIDDEN = (r"\bb\x65st\b", r"\bl\x65ading\b", r"\x231\b",
             r"r\x65tell", r"ai\x73ync", r"everything\x61i", r"sip\x6eex")
RULES = {
    "identity": r"\b(role|identity|you are)\b",
    "goal": r"\b(goal|objective\w*|your job|your only job)\b",
    "disclosure": r"\b(?:I am|I'm|this is)[^\n.!?]{0,100}\bAI\b[^\n.!?]{0,60}\b(?:assistant|agent|strategist)\b",
    "opt-out": r"\b(opt.out|do[ _-]not[ _-]call|DNC)\b",
    "transfer": r"\b(transfer|escalat\w*)\b",
}


@dataclass(frozen=True)
class Issue:
    """A stable rule code and a human-readable diagnostic."""
    code: str
    message: str
    warning: bool = False


def lint(text: str, call_type: str = "outbound-optin", max_length: int = 24000) -> list[Issue]:
    """Check required content, restricted vocabulary, and a character budget."""
    issues = [Issue(code, f"Missing {code} section or instruction") for code, pattern in RULES.items()
              if not re.search(pattern, text, re.I)]
    if call_type != "inbound" and not re.search(r"\b(voicemail|answering machine|AMD)\b", text, re.I):
        issues.append(Issue("voicemail", "Outbound prompts need voicemail / answering machine handling"))
    for pattern in FORBIDDEN:
        if re.search(pattern, text, re.I):
            issues.append(Issue("forbidden", "Restricted vocabulary found"))
    if re.search(r"[\u2013\u2014]", text):
        issues.append(Issue("punctuation", "Use plain hyphens"))
    if re.search(r"\d\s*(?:%|percent\b)|100[,]000|\b(?:conversion|booking) rates?\b", text, re.I):
        issues.append(Issue("claims", "Remove unsupported performance figures"))
    if len(text) > max_length:
        issues.append(Issue("length", f"Prompt has {len(text)} characters; budget is {max_length}", True))
    return issues
