# Supply-chain-disruption-project-
Logistics &amp; Supply Chain - Autonomous Disruption Monitoring Agent,Global supply chains are highly fragile. Port strikes, extreme weather, or geopolitical conflicts can disrupt production, making it crucial to quickly identify alternative suppliers across all supply chain tiers.
supplier K="vikram"
a=100
b=100
c=a+b
print c
# risk_agent.py

def classify_risk(article):
    article = article.lower()

    if "earthquake" in article:
        return {
            "risk_type": "Natural Disaster",
            "severity": "Critical"
        }

    elif "strike" in article:
        return {
            "risk_type": "Labor Strike",
            "severity": "High"
        }

    elif "war" in article or "conflict" in article:
        return {
            "risk_type": "Geopolitical Conflict",
            "severity": "Critical"
        }

    else:
        return {
            "risk_type": "Safe",
            "severity": "Low"
        }


# Sample news article
news_article = """
Taiwan earthquake disrupts semiconductor factories and causes delays
in microchip production.
"""

# Analyze article
result = classify_risk(news_article)

# Print output
print("Supply Chain Risk Analysis")
print("--------------------------")
print("Risk Type :", result["risk_type"])
print("Severity  :", result["severity"])
# network_agent.py

suppliers = [
    {"name": "Taiwan Chip Corp", "country": "Taiwan"},
    {"name": "Japan Silicon Ltd", "country": "Japan"},
    {"name": "India Assembly Pvt Ltd", "country": "India"},
    {"name": "Taipei Electronics", "country": "Taiwan"}
]

risk_country = "Taiwan"

affected_suppliers = []

for supplier in suppliers:
    if supplier["country"] == risk_country:
        affected_suppliers.append(supplier["name"])

print("Affected Suppliers")
print("------------------")

for supplier in affected_suppliers:
    print(supplier)
# disruption_monitor.py

# Mock supplier database
suppliers = [
    {
        "name": "Taiwan Chip Corp",
        "country": "Taiwan",
        "part": "Microchips"
    },
    {
        "name": "Taipei Electronics",
        "country": "Taiwan",
        "part": "Circuit Boards"
    },
    {
        "name": "Japan Chip Ltd",
        "country": "Japan",
        "part": "Microchips"
    },
    {
        "name": "Korea Semiconductor",
        "country": "South Korea",
        "part": "Microchips"
    }
]


def classify_risk(article):
    article = article.lower()

    if "earthquake" in article:
        return "Natural Disaster", "Critical", "Taiwan"

    elif "strike" in article:
        return "Labor Strike", "High", "Shanghai"

    elif "war" in article:
        return "Geopolitical Conflict", "Critical", "Unknown"

    return "Safe", "Low", "Unknown"


def find_affected_suppliers(country):
    affected = []

    for supplier in suppliers:
        if supplier["country"].lower() == country.lower():
            affected.append(supplier)

    return affected


def suggest_alternatives(affected_suppliers):
    alternatives = []

    affected_parts = []

    for supplier in affected_suppliers:
        affected_parts.append(supplier["part"])

    for supplier in suppliers:

        if supplier["country"] != "Taiwan":

            if supplier["part"] in affected_parts:
                alternatives.append(supplier)

    return alternatives



    risk_type, severity, country = classify_risk(article)

    affected_suppliers = find_affected_suppliers(country)

    alternatives = suggest_alternatives(affected_suppliers)

    print("\n========== DISRUPTION REPORT ==========\n")

    print("News Event:")
    print(article)

    print("\nRisk Analysis")
    print("--------------------")
    print("Risk Type :", risk_type)
    print("Severity  :", severity)
    print("Location  :", country)

    print("\nAffected Suppliers")
    print("--------------------")

    if len(affected_suppliers) == 0:
        print("No affected suppliers found")

    else:
        for supplier in affected_suppliers:
            print(
                f"- {supplier['name']} ({supplier['part']})"
            )

    print("\nAlternative Suppliers")
    print("--------------------")

    if len(alternatives) == 0:
        print("No alternatives found")

    else:
        for supplier in alternatives:
            print(
                f"- {supplier['name']} ({supplier['country']})"
            )

    print("\nRecommended Action")
    print("--------------------")

    if severity == "Critical":
        print("Switch sourcing immediately.")
        print("Increase safety stock.")
        print("Notify procurement team.")

    elif severity == "High":
        print("Monitor situation daily.")
        print("Prepare backup suppliers.")

    else:
        print("No action required.")

    print("\n=======================================\n")
    # report_engine.py

import json
from datetime import datetime


class DisruptionReport:

    def __init__(
        self,
        event,
        risk_type,
        severity,
        location,
        affected_suppliers,
        alternatives
    ):

        self.event = event
        self.risk_type = risk_type
        self.severity = severity
        self.location = location
        self.affected_suppliers = affected_suppliers
        self.alternatives = alternatives
        self.timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def generate_json(self):

        report = {
            "timestamp": self.timestamp,
            "event": self.event,
            "risk_type": self.risk_type,
            "severity": self.severity,
            "location": self.location,
            "affected_suppliers": self.affected_suppliers,
            "alternative_suppliers": self.alternatives
        }

        return report

    def save_report(self, filename):

        report = self.generate_json()

        with open(filename, "w") as file:
            json.dump(
                report,
                file,
                indent=4
            )

        print(f"\nReport saved: {filename}")


class RiskScorer:

    def calculate_score(self, severity):

        scores = {
            "Low": 25,
            "Medium": 50,
            "High": 75,
            "Critical": 100
        }

        return scores.get(severity, 0)


class AlertManager:

    def create_alert(self, severity):

        if severity == "Critical":
            return (
                "URGENT: Immediate action required."
            )

        elif severity == "High":
            return (
                "WARNING: Monitor situation closely."
            )

        elif severity == "Medium":
            return (
                "NOTICE: Potential disruption detected."
            )

        return (
            "SAFE: No significant disruption."
        )


class ReportHistory:

    def __init__(self):
        self.history = []

    def add_report(self, report):

        self.history.append(report)

    def show_reports(self):

        print("\n===== REPORT HISTORY =====")

        for report in self.history:

            print(
                f"{report['event']} | "
                f"{report['severity']} | "
                f"{report['timestamp']}"
            )


event = (
    "Taiwan earthquake disrupts "
    "semiconductor production"
)

affected_suppliers = [
    "Taiwan Chip Corp",
    "Taipei Electronics"
]

alternative_suppliers = [
    "Japan Chip Ltd",
    "Korea Semiconductor"
]

report = DisruptionReport(
    event=event,
    risk_type="Natural Disaster",
    severity="Critical",
    location="Taiwan",
    affected_suppliers=affected_suppliers,
    alternatives=alternative_suppliers
)

report_json = report.generate_json()

scorer = RiskScorer()

risk_score = scorer.calculate_score(
    report_json["severity"]
)

alert_manager = AlertManager()

alert_message = alert_manager.create_alert(
    report_json["severity"]
)

print("\n========== DISRUPTION REPORT ==========\n")

print("Event:")
print(report_json["event"])

print("\nLocation:")
print(report_json["location"])

print("\nRisk Type:")
print(report_json["risk_type"])

print("\nSeverity:")
print(report_json["severity"])

print("\nRisk Score:")
print(risk_score)

print("\nAlert:")
print(alert_message)

print("\nAffected Suppliers:")

for supplier in report_json[
    "affected_suppliers"
]:
    print(f"- {supplier}")

print("\nAlternative Suppliers:")

for supplier in report_json[
    "alternative_suppliers"
]:
    print(f"- {supplier}")

report.save_report(
    "disruption_report.json"
)

history = ReportHistory()

history.add_report(
    report_json
)

history.show_reports()
