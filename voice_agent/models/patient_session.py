from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class PatientSession(BaseModel):
    session_id: str
    patient_id: str
    appointment_id: str
    doctor_id: str
    original_transcript: Optional[str] = None
    edited_transcript: Optional[str] = None
    version: int = 1
    status: str = 'active'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
