# clackai-pdf-tool

Extract structured data from PDFs using pdfplumber + Anthropic Claude.

## Install

```bash
pip install -r requirements.txt
```

Set your API key:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Usage

```bash
# Extract structured data from a PDF
python -m pdf_tool extract invoice.pdf

# Raw text only (no AI, no API key needed)
python -m pdf_tool extract invoice.pdf --text-only

# Custom extraction instruction
python -m pdf_tool ask report.pdf "Extract all financial metrics as JSON"
```

## Output

JSON with extracted fields — invoices get `vendor`, `line_items`, `total`; reports get `title`, `sections`, `key_metrics`.

## Project Structure

```
pdf_tool/
├── __init__.py
├── __main__.py    # python -m pdf_tool support
├── parser.py      # pdfplumber text/table extraction
├── ai.py          # Anthropic structured extraction
└── cli.py         # click CLI
tests/
└── test_parser.py # parser unit tests
```
