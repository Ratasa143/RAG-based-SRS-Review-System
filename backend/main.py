from fastapi import FastAPI, UploadFile, File
import shutil
import uuid
import json

from core.parser import extract_text
from core.chunker import split_requirements
from rag_pipeline import retrieve_knowledge
from core.llm import analyze_requirement

from db.crud import save_analysis, get_results

# --------------------------------------------------
# FastAPI App
# --------------------------------------------------

app = FastAPI()

# --------------------------------------------------
# Home Endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "SRS Review System Backend Running"
    }

# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

# --------------------------------------------------
# Analyze PDF
# --------------------------------------------------

@app.post("/analyze")
async def analyze_pdf(file: UploadFile = File(...)):

    # ----------------------------
    # Save uploaded PDF
    # ----------------------------

    upload_path = f"sample_docs/{file.filename}"

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ----------------------------
    # Extract Text
    # ----------------------------

    text = extract_text(upload_path)

    # ----------------------------
    # Split into Requirements
    # ----------------------------

    requirements = split_requirements(text)

    # ----------------------------
    # Generate Document ID
    # ----------------------------

    document_id = str(uuid.uuid4())

    final_results = []

    # ----------------------------
    # Analyze First 3 Requirements
    # ----------------------------

    for req in requirements[:3]:

        # ----------------------------
        # Retrieve Knowledge
        # ----------------------------

        retrieved = retrieve_knowledge(req["text"])

        knowledge = ""

        for doc in retrieved["documents"][0]:
            knowledge += doc + "\n"

        # ----------------------------
        # Analyze using LLM
        # ----------------------------

        analysis = analyze_requirement(
            req["text"],
            knowledge
        )

        # ----------------------------
        # Convert JSON safely
        # ----------------------------

        try:

            analysis_data = json.loads(analysis)

        except Exception:

            analysis_data = {

                "issue": "Unable to parse LLM response",

                "suggestion": analysis,

                "confidence": "Low"

            }

        # ----------------------------
        # Save into SQLite
        # ----------------------------

        save_analysis(

            document_id=document_id,

            requirement=req["text"],

            issue=analysis_data["issue"],

            suggestion=analysis_data["suggestion"],

            confidence=analysis_data["confidence"]

        )

        # ----------------------------
        # Store for API Response
        # ----------------------------

        final_results.append({

            "id": req["id"],

            "requirement": req["text"],

            "analysis": analysis_data

        })

    # ----------------------------
    # Return Response
    # ----------------------------

    return {

        "document_id": document_id,

        "total_requirements": len(requirements),

        "analysed_requirements": len(final_results),

        "results": final_results

    }

# --------------------------------------------------
# Get Previous Analysis Results
# --------------------------------------------------

@app.get("/results/{document_id}")
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