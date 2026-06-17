import pandas as pd
from pathlib import Path

# Get the directory where this script is located
script_dir = Path(__file__).parent
csv_path = script_dir / "database" / "database" / "supply_chain_disruption_recovery.csv"

df = pd.read_csv(csv_path)

print(df.head())