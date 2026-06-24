from sqlalchemy.orm import sessionmaker

from db.models import (
    engine,
    AnalysisResult
)

# --------------------------------------------------
# Session
# --------------------------------------------------

SessionLocal = sessionmaker(bind=engine)

# --------------------------------------------------
# Save Analysis
# --------------------------------------------------

def save_analysis(
    document_id,
    requirement,
    issue,
    suggestion,
    confidence
):

    db = SessionLocal()

    record = AnalysisResult(

        document_id=document_id,

        requirement=requirement,

        issue=issue,

        suggestion=suggestion,

        confidence=confidence

    )

    db.add(record)

    db.commit()

    db.close()

# --------------------------------------------------
# Get Results
# --------------------------------------------------

def get_results(document_id):

    db = SessionLocal()

    results = db.query(
        AnalysisResult
    ).filter(

        AnalysisResult.document_id == document_id

    ).all()

    db.close()

    return results