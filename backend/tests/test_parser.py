import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.parser import parse_document

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "sample_docs")

def test_parse_txt():
    reqs = parse_document(os.path.join(SAMPLE_DIR, "sample1.txt"), "txt")
    assert len(reqs) >= 2
    assert all("text" in r and "id" in r for r in reqs)

def test_parse_pdf():
    reqs = parse_document(os.path.join(SAMPLE_DIR, "sample2.pdf"), "pdf")
    assert len(reqs) >= 1

def test_parse_docx():
    reqs = parse_document(os.path.join(SAMPLE_DIR, "sample3.docx"), "docx")
    assert len(reqs) >= 1

def test_unsupported_type():
    import pytest
    with pytest.raises(ValueError):
        parse_document("fake.xyz", "xyz")