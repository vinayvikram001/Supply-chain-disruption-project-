import pandas as pd

df = pd.read_csv("data/supply_chain_cleaned.csv")

def calculate_risk(row):

    score = 0

    if row['disruption_type'] == "Port Closure":
        score += 40

    if row['severity'] == "High":
        score += 40

    if row['recovery_days'] > 20:
        score += 20

    if score >= 80:
        return "High"

    elif score >= 50:
        return "Medium"

    else:
        return "Low"


df['risk_level'] = df.apply(
    calculate_risk,
    axis=1
)

print(
    df[['supplier_id',
        'risk_level']].head()
)