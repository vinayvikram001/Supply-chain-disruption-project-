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
