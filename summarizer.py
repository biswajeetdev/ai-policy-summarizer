"""
Core summarization logic — provider-agnostic, OpenAI SDK-compatible.
"""
from __future__ import annotations

import re
from typing import Optional

from openai import OpenAI

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_MODEL = "llama-3.3-70b-versatile"
OPENAI_MODEL = "gpt-4o-mini"


def make_client(api_key: str, provider: str = "groq") -> OpenAI:
    if provider == "openai":
        return OpenAI(api_key=api_key)
    return OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)


SUMMARY_PROMPT = """\
You are a policy analyst who specialises in translating complex institutional \
documents into plain language. Given the policy text below, produce a structured \
analysis in the following exact format (use these exact headings):

## Plain-Language Summary
2–4 sentence overview a non-expert can understand immediately.

## Key Points
- Bullet list of the 5–8 most important facts, rules, or obligations.

## Who This Affects
- Bullet list of the specific roles, teams, or individuals this policy applies to.

## Required Actions
- Concrete steps that readers must take (or "None identified" if purely informational).

## Important Dates & Deadlines
- Any dates, deadlines, or review cycles mentioned (or "None specified").

## Plain-Language Glossary
- Define any jargon or technical terms used in the document (3–6 terms max).

Be concise and precise. Do not add commentary or caveats beyond the format above.
"""


def summarise(text: str, client: OpenAI, provider: str = "groq") -> str:
    model = OPENAI_MODEL if provider == "openai" else GROQ_MODEL
    # Truncate to ~12k words to stay within context limits for large docs
    words = text.split()
    if len(words) > 12_000:
        text = " ".join(words[:12_000]) + "\n\n[Document truncated for length]"

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SUMMARY_PROMPT},
            {"role": "user", "content": f"Policy document:\n\n{text}"},
        ],
        temperature=0.1,
    )
    return resp.choices[0].message.content


def compare(texts: dict[str, str], client: OpenAI, provider: str = "groq") -> str:
    """Compare two or more policy documents and highlight differences."""
    model = OPENAI_MODEL if provider == "openai" else GROQ_MODEL
    docs_block = "\n\n---\n\n".join(
        f"[Document: {name}]\n{text[:4000]}" for name, text in texts.items()
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a policy analyst. Compare the provided documents and produce "
                    "a structured comparison covering: key similarities, key differences, "
                    "conflicts or contradictions, and which document is more restrictive "
                    "on each major point. Use markdown tables where helpful."
                ),
            },
            {"role": "user", "content": docs_block},
        ],
        temperature=0.1,
    )
    return resp.choices[0].message.content
