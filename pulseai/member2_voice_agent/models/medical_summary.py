from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class MedicalSummaryModel(BaseModel):
    summary_id: str
    session_id: str
    summary_text: str
    summary_format: str
    key_findings: str # Stored as JSON string in DB
    generated_at: Optional[datetime] = None
    sent_to_doctor_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
