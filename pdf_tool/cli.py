from __future__ import annotations

import json
import sys
from pathlib import Path

import click

from .ai import extract_structured
from .parser import extract


@click.group()
def cli():
    """clackai-pdf-tool: Extract structured data from PDFs."""


@cli.command()
@click.argument("pdf_path", type=click.Path(exists=True))
@click.option("--max-pages", default=50, help="Max pages to process.")
@click.option("--text-only", is_flag=True, help="Print raw text, skip AI.")
def extract_cmd(pdf_path: str, max_pages: int, text_only: bool):
    """Extract structured data from a PDF."""
    try:
        content = extract(pdf_path, max_pages=max_pages)
    except (FileNotFoundError, ValueError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    if text_only:
        click.echo(content.text)
        if content.tables:
            click.echo(f"\n--- {len(content.tables)} table(s) found ---")
            for i, tbl in enumerate(content.tables, 1):
                click.echo(f"\nTable {i}:")
                for row in tbl:
                    click.echo(" | ".join(row))
        return

    click.echo("Extracting with AI...", err=True)
    try:
        result = extract_structured(content)
    except RuntimeError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    click.echo(json.dumps(result, indent=2, ensure_ascii=False))


@cli.command()
@click.argument("pdf_path", type=click.Path(exists=True))
@click.argument("instruction")
@click.option("--max-pages", default=50, help="Max pages to process.")
def ask(pdf_path: str, instruction: str, max_pages: int):
    """Extract data from a PDF with a custom instruction."""
    try:
        content = extract(pdf_path, max_pages=max_pages)
    except (FileNotFoundError, ValueError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    try:
        result = extract_structured(content, instruction=instruction)
    except RuntimeError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    click.echo(json.dumps(result, indent=2, ensure_ascii=False))


# Aliases for `python -m pdf_tool`
extract_cmd.name = "extract"
ask.name = "ask"


if __name__ == "__main__":
    cli()
