from fastapi import APIRouter, UploadFile, File
import shutil
import uuid
import json

from core.parser import extract_text
from core.chunker import split_requirements
from rag_pipeline import retrieve_knowledge
from core.llm import analyze_requirement
from core.completeness_checker import check_completeness
from core.improvement_generator import generate_improvement

from db.crud import save_analysis, get_results

router = APIRouter()


@router.post("/analyze")
async def analyze_pdf(file: UploadFile = File(...)):

    # -----------------------------
    # Save Uploaded PDF
    # -----------------------------
    upload_path = f"sample_docs/{file.filename}"

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # -----------------------------
    # Extract text
    # -----------------------------
    text = extract_text(upload_path)

    # -----------------------------
    # Split into requirements
    # -----------------------------
    requirements = split_requirements(text)

    # Unique document ID
    document_id = str(uuid.uuid4())

    final_results = []

    # -----------------------------
    # Analyze first 3 requirements
    # -----------------------------
    for req in requirements[:3]:

        print("=" * 60)
        print("Requirement:")
        print(req["text"])
        print("=" * 60)

        # -----------------------------------
        # STEP 1 : Completeness Checker
        # -----------------------------------
        completeness = check_completeness(req["text"])

        print("Completeness Result:")
        print(completeness)
        print("=" * 60)

        # -----------------------------------
        # STEP 2 : Retrieve Knowledge
        # -----------------------------------
        retrieved = retrieve_knowledge(req["text"])

        knowledge = ""

        for doc in retrieved["documents"][0]:
            knowledge += doc + "\n"

        # -----------------------------------
        # STEP 3 : Ambiguity Analysis
        # -----------------------------------
        analysis = analyze_requirement(
            req["text"],
            knowledge
        )

        # -----------------------------------
        # Convert JSON string into dictionary
        # -----------------------------------
        try:

            analysis_data = json.loads(analysis)

        except Exception:

            analysis_data = {
                "issue": "Unable to parse LLM response",
                "suggestion": analysis,
                "confidence": "Low"
            }

        # -----------------------------------
        # STEP 4 : Generate Improved Requirement
        # -----------------------------------
        improvement = generate_improvement(
            requirement=req["text"],
            completeness=completeness,
            ambiguity=analysis_data,
            knowledge=knowledge
        )

        print("Improved Requirement:")
        print(improvement)
        print("=" * 60)

        # -----------------------------------
        # Save into SQLite
        # -----------------------------------
        save_analysis(
            document_id=document_id,
            requirement=req["text"],
            issue=analysis_data["issue"],
            suggestion=analysis_data["suggestion"],
            confidence=analysis_data["confidence"]
        )

        # -----------------------------------
        # Final API Response
        # -----------------------------------
        final_results.append({

            "id": req["id"],

            "requirement": req["text"],

            "completeness": completeness,

            "analysis": analysis_data,

            "improvement": improvement

        })

    return {

        "document_id": document_id,

        "total_requirements": len(requirements),

        "analysed_requirements": len(final_results),

        "results": final_results

    }


# =====================================================
# GET Previous Analysis Results
# =====================================================

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