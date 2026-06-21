import fitz  # PyMuPDF
import docx
import re
import uuid

def parse_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def parse_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs)

def parse_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_requirements(raw_text: str) -> list[dict]:
    """
    Splits raw text into individual requirement-like sentences.
    Looks for lines containing 'shall', 'must', 'will', or numbered req IDs.
    """
    lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
    requirements = []

    for line in lines:
        # Keep lines that look like requirements
        if re.search(r"\b(shall|must|should|will)\b", line, re.IGNORECASE) or \
           re.match(r"^(REQ|FR|NFR)[-_]?\d+", line, re.IGNORECASE):
            requirements.append({
                "id": str(uuid.uuid4())[:8],
                "text": line
            })

    return requirements

def parse_document(file_path: str, file_type: str) -> list[dict]:
    if file_type == "pdf":
        raw_text = parse_pdf(file_path)
    elif file_type == "docx":
        raw_text = parse_docx(file_path)
    elif file_type == "txt":
        raw_text = parse_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    return extract_requirements(raw_text)