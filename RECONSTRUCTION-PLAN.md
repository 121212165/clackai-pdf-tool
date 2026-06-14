# Reconstruction Plan

## First Principles

1. A PDF is a fixed-layout container — extract text + tables, then understand via AI.
2. One command must go from PDF → structured data. No ceremony.
3. 3 layers: Parser → AI → CLI. Build bottom-up.

## Files to Create

| File | Purpose | LOC |
|------|---------|-----|
| `pdf_tool/__init__.py` | Package marker | 1 |
| `pdf_tool/parser.py` | pdfplumber text/table extraction | ~50 |
| `pdf_tool/ai.py` | Anthropic structured extraction | ~60 |
| `pdf_tool/cli.py` | click CLI entrypoint | ~50 |
| `requirements.txt` | 3 deps | 3 |
| `pyproject.toml` | Project metadata + entrypoint | 15 |
| `tests/test_parser.py` | Parser unit tests | ~30 |

## Execution Order

1. parser.py — can run without AI
2. ai.py — wraps Anthropic for structured extraction
3. cli.py — wires parser + ai into one command
4. tests — validate parser logic
5. Update README.md with real usage

## Musk's Razor Applied

- No dual-language README
- No generic boilerplate
- No CI changes (existing CI validates if requirements.txt exists)
- One question: `python -m pdf_tool extract invoice.pdf` → JSON
