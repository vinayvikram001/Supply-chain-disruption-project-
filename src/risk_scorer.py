def calculate_risk(row):

    score = 0

    if row["disruption_severity"] >= 8:
        score += 40

    if row["production_impact_pct"] >= 60:
        score += 40

    if row["full_recovery_days"] >= 20:
        score += 20

    if score >= 80:
        return "High"

    elif score >= 50:
        return "Medium"

    return "Low"