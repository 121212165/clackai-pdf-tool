from __future__ import annotations

import json
import os
from typing import Any

import anthropic

from .parser import PDFContent

DEFAULT_MODEL = "claude-sonnet-4-20250514"

SYSTEM_PROMPT = """\
You are a structured data extraction engine.
Given raw text and tables extracted from a PDF, return a clean JSON object
that captures the document's key information.

Rules:
- Return ONLY valid JSON, no markdown fences, no explanation.
- Use descriptive keys matching the document's domain.
- For invoices: include vendor, date, line_items, total, currency.
- For reports: include title, date, sections, key_metrics.
- For generic docs: include title, summary, key_points.
- Tables should become arrays of objects with meaningful headers.
"""


def extract_structured(
    content: PDFContent,
    instruction: str | None = None,
    *,
    model: str = DEFAULT_MODEL,
    api_key: str | None = None,
) -> dict[str, Any]:
    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Set ANTHROPIC_API_KEY env var or pass api_key parameter"
        )

    user_msg = _build_prompt(content, instruction)

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()

    return json.loads(raw)


def _build_prompt(content: PDFContent, instruction: str | None) -> str:
    parts = [f"--- EXTRACTED TEXT ({content.page_count} pages) ---\n{content.text}"]

    if content.tables:
        parts.append("\n--- EXTRACTED TABLES ---")
        for i, tbl in enumerate(content.tables, 1):
            parts.append(f"\nTable {i}:")
            for row in tbl:
                parts.append(" | ".join(row))

    if instruction:
        parts.append(f"\n--- INSTRUCTION ---\n{instruction}")
    else:
        parts.append(
            "\n--- INSTRUCTION ---\nExtract all key information as structured JSON."
        )

    return "\n".join(parts)
