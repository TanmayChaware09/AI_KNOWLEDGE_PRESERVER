from pydantic import BaseModel
from datetime import datetime


class RawDocument(BaseModel):
    source: str
    employee_id: str
    employee_name: str
    department: str
    content: str
    timestamp: datetime
    url: str