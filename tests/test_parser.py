from pathlib import Path

import pytest

from pdf_tool.parser import PDFContent, extract


class TestPDFContent:
    def test_to_dict_empty(self):
        pc = PDFContent(text="", tables=[], page_count=0)
        d = pc.to_dict()
        assert d == {"text": "", "tables": [], "page_count": 0}

    def test_to_dict_with_data(self):
        table = [["Name", "Age"], ["Alice", "30"]]
        pc = PDFContent(text="Hello", tables=[table], page_count=1)
        d = pc.to_dict()
        assert d["text"] == "Hello"
        assert d["tables"] == [[["Name", "Age"], ["Alice", "30"]]]
        assert d["page_count"] == 1


class TestExtract:
    def test_file_not_found(self, tmp_path: Path):
        with pytest.raises(FileNotFoundError):
            extract(tmp_path / "nonexistent.pdf")

    def test_not_a_pdf(self, tmp_path: Path):
        f = tmp_path / "test.txt"
        f.write_text("hello")
        with pytest.raises(ValueError, match="Not a PDF"):
            extract(f)
