import os
import shutil
from fastapi import APIRouter, UploadFile, HTTPException
from core.parser import parse_document

router = APIRouter()
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_TYPES = {"pdf", "docx", "txt"}

@router.post("/upload")
async def upload_file(file: UploadFile):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_TYPES:
        raise HTTPException(400, f"Unsupported file type: {ext}")

    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        requirements = parse_document(save_path, ext)
    except Exception as e:
        raise HTTPException(500, f"Parsing failed: {str(e)}")

    return {
        "filename": file.filename,
        "requirement_count": len(requirements),
        "requirements": requirements
    }