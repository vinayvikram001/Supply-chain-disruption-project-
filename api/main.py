from fastapi import FastAPI
from src.network_builder import build_graph
from src.network_builder import (
    build_graph,
    blast_radius,
     get_backup_suppliers
)

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