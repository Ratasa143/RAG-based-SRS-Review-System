from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime
)

from sqlalchemy.orm import declarative_base
from datetime import datetime

# --------------------------------------------------
# SQLite Database
# --------------------------------------------------

DATABASE_URL = "sqlite:///srs_review.db"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

# --------------------------------------------------
# Analysis Result Table
# --------------------------------------------------

class AnalysisResult(Base):

    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(String)

    requirement = Column(String)

    issue = Column(String)

    suggestion = Column(String)

    confidence = Column(String)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )

# --------------------------------------------------
# Create Tables
# --------------------------------------------------

Base.metadata.create_all(bind=engine)