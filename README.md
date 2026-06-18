# Supply-chain-disruption-project-
Logistics &amp; Supply Chain - Autonomous Disruption Monitoring Agent,Global supply chains are highly fragile. Port strikes, extreme weather, or geopolitical conflicts can disrupt production, making it crucial to quickly identify alternative suppliers across all supply chain tiers.
import json
from datetime import datetime


# -----------------------------
# NEWS DATA
# -----------------------------

news_article = """
Taiwan earthquake disrupts semiconductor factories
and delays microchip production.
"""


# -----------------------------
# SUPPLIER DATABASE
# -----------------------------

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
    },
    {
        "name": "India Silicon Works",
        "country": "India",
        "part": "Silicon"
    }
]


# -----------------------------
# RISK AGENT
# -----------------------------

def classify_risk(article):

    article = article.lower()

    if "earthquake" in article:
        return {
            "risk_type": "Natural Disaster",
            "severity": "Critical",
            "country": "Taiwan"
        }

    elif "strike" in article:
        return {
            "risk_type": "Labor Strike",
            "severity": "High",
            "country": "China"
        }

    elif "war" in article:
        return {
            "risk_type": "Geopolitical Conflict",
            "severity": "Critical",
            "country": "Unknown"
        }

    return {
        "risk_type": "Safe",
        "severity": "Low",
        "country": "Unknown"
    }


# -----------------------------
# NETWORK AGENT
# -----------------------------

def find_affected_suppliers(country):

    affected = []

    for supplier in suppliers:

        if supplier["country"].lower() == country.lower():
            affected.append(supplier)

    return affected


# -----------------------------
# SOURCING AGENT
# -----------------------------

def find_alternatives(affected_suppliers):

    alternatives = []

    affected_parts = []

    for supplier in affected_suppliers:
        affected_parts.append(supplier["part"])

    for supplier in suppliers:

        if supplier["country"] != "Taiwan":

            if supplier["part"] in affected_parts:
                alternatives.append(supplier)

    return alternatives


# -----------------------------
# REPORT ENGINE
# -----------------------------

def generate_report(article):

    risk = classify_risk(article)

    affected = find_affected_suppliers(
        risk["country"]
    )

    alternatives = find_alternatives(
        affected
    )

    report = {
        "timestamp": str(datetime.now()),
        "event": article.strip(),
        "risk_type": risk["risk_type"],
        "severity": risk["severity"],
        "location": risk["country"],
        "affected_suppliers": [],
        "alternative_suppliers": []
    }

    for supplier in affected:
        report["affected_suppliers"].append(
            supplier["name"]
        )

    for supplier in alternatives:
        report["alternative_suppliers"].append(
            supplier["name"]
        )

    return report


# -----------------------------
# EXECUTION
# -----------------------------

report = generate_report(news_article)

print("\n========== SUPPLY CHAIN REPORT ==========\n")

print("Risk Type:")
print(report["risk_type"])

print("\nSeverity:")
print(report["severity"])

print("\nLocation:")
print(report["location"])

print("\nAffected Suppliers:")

for supplier in report["affected_suppliers"]:
    print("-", supplier)

print("\nAlternative Suppliers:")

for supplier in report["alternative_suppliers"]:
    print("-", supplier)

print("\nSaving report...\n")

with open(
    "disruption_report.json",
    "w"
) as file:

    json.dump(
        report,
        file,
        indent=4
    )

print("Report saved successfully!")

print("\n=========================================\n")
