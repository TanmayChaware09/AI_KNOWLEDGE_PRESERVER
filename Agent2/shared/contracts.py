from datetime import datetime

from pydantic import BaseModel


# ==========================================================
# AGENT 1 : RAW DOCUMENT
# ==========================================================

class RawDocument(BaseModel):

    source: str

    employee_name: str

    employee_id: str

    department: str

    timestamp: datetime

    url: str

    content: str


# ==========================================================
# AGENT 2 : KNOWLEDGE CARD
# ==========================================================

class KnowledgeCard(BaseModel):

    title: str

    summary: str

    category: str

    confidence: float

    source: str

    employee_id: str

    timestamp: datetime