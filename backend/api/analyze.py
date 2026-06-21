from fastapi import APIRouter

router = APIRouter()

@router.post("/analyze/{doc_id}")
async def analyze_document(doc_id: str):
    return {"status": "stub", "doc_id": doc_id}