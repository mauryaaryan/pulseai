from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class RiskAnalysisModel(BaseModel):
    analysis_id: str
    session_id: str
    symptom_severity_score: int
    urgency_score: int
    comorbidity_score: int
    duration_trend_score: int
    total_risk_score: int
    risk_level: str
    risk_reasoning: str
    analysis_timestamp: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
