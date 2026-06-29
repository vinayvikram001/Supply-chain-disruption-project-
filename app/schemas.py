from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class RiskAssessment(BaseModel):
    risk_type: str = Field(description="Type of disruption e.g. natural disaster, labor strike")
    severity: str = Field(description="Critical, High, Medium, or Low")
    affected_country: str = Field(description="Country where disruption occurred")
    confidence_score: float = Field(description="Agent confidence 0.0 to 1.0")

class AffectedSupplier(BaseModel):
    supplier_name: str
    country: str
    tier: int = Field(description="Supply chain tier 1, 2, or 3")
    parts_affected: List[str]

class AlternativeSupplier(BaseModel):
    supplier_name: str
    country: str
    parts_available: List[str]
    lead_time_days: int
    reliability_score: float

class DisruptionReport(BaseModel):
    report_id: str
    timestamp: str = Field(default_factory=lambda: str(datetime.now()))
    news_headline: str
    risk_assessment: RiskAssessment
    affected_suppliers: List[AffectedSupplier]
    alternative_suppliers: List[AlternativeSupplier]
    recovery_time_days: float
    executive_summary: str