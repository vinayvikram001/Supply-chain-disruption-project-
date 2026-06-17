import pandas as pd
import networkx as nx

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

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
def blast_radius(graph, supplier):

    affected = list(
        nx.descendants(graph, supplier)
    )

    return affected
supplier = "SUP011"

affected = blast_radius(G, supplier)

print("\nDisruption Source:", supplier)

print("Affected Suppliers:")

for node in affected:

    print(node)
print("\nBackup Suppliers:")

for node in affected:

    backup = df[
        df['supplier_id'] == node
    ]['backup_supplier'].values

    if len(backup) > 0:

        print(
            node,
            "→",
            backup[0]
        )