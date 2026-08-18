from datetime import datetime

from pydantic import BaseModel


# ==========================================================
# Knowledge Agent Output
# Privacy Agent Input
# ==========================================================

class KnowledgeCard(BaseModel):

    title: str

    summary: str

    category: str

    confidence: float

    source: str

    employee_id: str

    timestamp: datetime


# ==========================================================
# Privacy Agent Output
# Storage Agent Input
# ==========================================================

class SafeKnowledgeCard(BaseModel):

    title: str

    summary: str

    category: str

    confidence: float

    source: str

    timestamp: datetime


# ==========================================================
# Storage Agent Output
# ==========================================================
class StoredKnowledge(BaseModel):

    postgres_id: int
    vector_id: str
    stored: bool