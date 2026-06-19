from fastapi import FastAPI
from src.network_builder import build_graph
from src.network_builder import (
    build_graph,
    blast_radius,
     get_backup_suppliers
)
import pandas as pd
from src.risk_scorer import calculate_risk

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Supply Chain API Running"
    }

@app.get("/network-summary")
def network_summary():

    G, df = build_graph()

    return {
        "suppliers": G.number_of_nodes(),
        "connections": G.number_of_edges()
    }
@app.get("/blast-radius/{supplier_id}")
def supplier_blast_radius(supplier_id: str):

    G, df = build_graph()

    affected = blast_radius(
        G,
        supplier_id
    )

    return {
        "supplier": supplier_id,
        "affected_suppliers": affected,
        "count": len(affected)
    }
@app.get("/suppliers")
def suppliers():

    G, df = build_graph()

    return {
        "suppliers": list(G.nodes())
    }
@app.get("/backup-suppliers/{supplier_id}")
def backup_suppliers(supplier_id: str):

    G, df = build_graph()

    affected = blast_radius(
        G,
        supplier_id
    )

    backups = get_backup_suppliers(
        df,
        affected
    )

    return {
        "supplier": supplier_id,
        "affected_suppliers": affected,
        "backup_recommendations": backups
    }
@app.get("/risk-summary")
def risk_summary():

    df = pd.read_csv("data/supply_chain_cleaned.csv")

    df["risk_level"] = df.apply(
        calculate_risk,
        axis=1
    )

    counts = df["risk_level"].value_counts().to_dict()

    return counts
@app.get("/risk/{disruption_id}")
def get_risk(disruption_id: str):

    df = pd.read_csv("data/supply_chain_cleaned.csv")

    row = df[
        df["disruption_id"] == disruption_id
    ]

    if row.empty:
        return {
            "error": "Disruption not found"
        }

    row = row.iloc[0]

    risk = calculate_risk(row)

    return {
    "disruption_id": str(disruption_id),
    "risk_level": str(risk),
    "disruption_severity": int(row["disruption_severity"]),
    "production_impact_pct": float(row["production_impact_pct"]),
    "full_recovery_days": float(row["full_recovery_days"])
}