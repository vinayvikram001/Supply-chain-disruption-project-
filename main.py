from app.api import app
from app.schemas import (
    AffectedSupplier,
    AlternativeSupplier,
    DisruptionReport,
    RiskAssessment,
)
from generate_report import save_report
import uvicorn
import uuid


@app.post("/report")
def generate_disruption_report(payload: dict):
    report = DisruptionReport(
        report_id=f"RPT-{str(uuid.uuid4())[:8].upper()}",
        news_headline=payload.get("headline", "Supply chain disruption detected"),
        risk_assessment=RiskAssessment(
            risk_type=payload.get("disruption_type", "natural disaster"),
            severity=payload.get("severity", "High"),
            affected_country=payload.get("country", "Unknown"),
            confidence_score=0.87,
        ),
        affected_suppliers=[
            AffectedSupplier(
                supplier_name="Taiwan Chip Corp",
                country="Taiwan",
                tier=2,
                parts_affected=["Microchips", "Circuit Boards"],
            )
        ],
        alternative_suppliers=[
            AlternativeSupplier(
                supplier_name="Korea Semiconductor",
                country="South Korea",
                parts_available=["Microchips"],
                lead_time_days=14,
                reliability_score=0.92,
            )
        ],
        recovery_time_days=payload.get("recovery_days", 30),
        executive_summary=(
            f"A {payload.get('disruption_type', 'disruption')} has been detected. "
            "Immediate action required to secure alternative suppliers."
        ),
    )

    path = save_report(report)
    return {"status": "success", "report_id": report.report_id, "saved_to": path}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
