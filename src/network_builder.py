import pandas as pd
import networkx as nx

def build_graph():

    df = pd.read_csv("data/supplier_network.csv")

    G = nx.DiGraph()

    for _, row in df.iterrows():

        supplier = row['supplier_id']

        G.add_node(
            supplier,
            name=row['supplier_name'],
            tier=row['tier'],
            region=row['region'],
            industry=row['industry']
        )

        dependency = row['depends_on']

        if pd.notna(dependency):
            G.add_edge(dependency, supplier)

    return G, df


def blast_radius(graph, supplier):

    return list(
        nx.descendants(graph, supplier)
    )


def get_backup_suppliers(df, affected):

    backups = {}

    for node in affected:

        backup = df[
            df['supplier_id'] == node
        ]['backup_supplier'].values

        if len(backup) > 0:
            backups[node] = backup[0]

    return backups