from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pdfplumber


@dataclass
class PDFContent:
    text: str
    tables: list[list[list[str]]] = field(default_factory=list)
    page_count: int = 0

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "tables": self.tables,
            "page_count": self.page_count,
        }


def extract(path: str | Path, max_pages: int = 50) -> PDFContent:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")
    if not path.suffix.lower() == ".pdf":
        raise ValueError(f"Not a PDF: {path}")

    text_parts: list[str] = []
    tables: list[list[list[str]]] = []

    with pdfplumber.open(path) as pdf:
        page_count = min(len(pdf.pages), max_pages)
        for i in range(page_count):
            page = pdf.pages[i]
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
            page_tables = page.extract_tables()
            for tbl in page_tables:
                cleaned = [
                    [cell if cell is not None else "" for cell in row]
                    for row in tbl
                ]
                tables.append(cleaned)

    return PDFContent(
        text="\n\n".join(text_parts),
        tables=tables,
        page_count=page_count,
    )
