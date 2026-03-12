from pydantic import BaseModel, ConfigDict
from typing import Optional

class SymptomEntity(BaseModel):
    entity_id: str
    session_id: str
    symptom_name: str
    severity_level: str
    duration: str
    characteristics: str

    model_config = ConfigDict(from_attributes=True)
