from fastapi import APIRouter, UploadFile, File
import shutil
import uuid
import json

from core.parser import extract_text
from core.chunker import split_requirements
from rag_pipeline import retrieve_knowledge
from core.llm import analyze_requirement

from db.crud import save_analysis, get_results

router = APIRouter()


@router.post("/analyze")
async def analyze_pdf(file: UploadFile = File(...)):

    upload_path = f"sample_docs/{file.filename}"

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(upload_path)

    requirements = split_requirements(text)

    document_id = str(uuid.uuid4())

    final_results = []

    for req in requirements[:3]:

        retrieved = retrieve_knowledge(req["text"])

        knowledge = ""

        for doc in retrieved["documents"][0]:
            knowledge += doc + "\n"

        analysis = analyze_requirement(
            req["text"],
            knowledge
        )

        try:
            analysis_data = json.loads(analysis)

        except Exception:

            analysis_data = {
                "issue": "Unable to parse LLM response",
                "suggestion": analysis,
                "confidence": "Low"
            }

        save_analysis(
            document_id=document_id,
            requirement=req["text"],
            issue=analysis_data["issue"],
            suggestion=analysis_data["suggestion"],
            confidence=analysis_data["confidence"]
        )

        final_results.append({
            "id": req["id"],
            "requirement": req["text"],
            "analysis": analysis_data
        })

    return {
        "document_id": document_id,
        "total_requirements": len(requirements),
        "analysed_requirements": len(final_results),
        "results": final_results
    }


@router.get("/results/{document_id}")
def get_analysis_results(document_id: str):

    results = get_results(document_id)

    final_results = []

    for row in results:

        final_results.append({
            "document_id": row.document_id,
            "requirement": row.requirement,
            "issue": row.issue,
            "suggestion": row.suggestion,
            "confidence": row.confidence,
            "timestamp": row.timestamp
        })

    return final_results