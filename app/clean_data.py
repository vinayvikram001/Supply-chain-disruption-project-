import json
import pandas as pd
import numpy as np
from pathlib import Path
import os

# Get the directory where this script is located
script_dir = Path(__file__).parent
project_root = script_dir.parent
csv_path = script_dir / "database" / "database" / "supply_chain_disruption_recovery.csv"
supplier_json_path = project_root / "data" / "suppliers.json"

# Load raw data
df = pd.read_csv(csv_path)

print("=" * 60)
print("DATASET CLEANING PIPELINE")
print("=" * 60)

# Initial stats
print(f"\n[1] Initial Dataset: {df.shape[0]} rows, {df.shape[1]} columns")

# Check for duplicates
duplicates = df.duplicated().sum()
df = df.drop_duplicates()
print(f"[2] Removed duplicates: {duplicates} rows")

# Load optional supplier metadata JSON
supplier_metadata = None
if supplier_json_path.exists():
    with open(supplier_json_path, 'r', encoding='utf-8') as f:
        supplier_payload = json.load(f)

    supplier_records = supplier_payload.get('suppliers', [])
    if supplier_records:
        supplier_metadata = pd.DataFrame(supplier_records)

        # Normalize supplier metadata fields for downstream use
        if 'tier' in supplier_metadata.columns:
            supplier_metadata['tier'] = pd.to_numeric(supplier_metadata['tier'], errors='coerce')
        if 'location' in supplier_metadata.columns:
            supplier_metadata['location'] = supplier_metadata['location'].astype(str).str.strip().str.lower()
        if 'risk_level' in supplier_metadata.columns:
            supplier_metadata['risk_level'] = supplier_metadata['risk_level'].astype(str).str.strip().str.lower()
        if 'parts_supplied' in supplier_metadata.columns:
            supplier_metadata['parts_supplied'] = supplier_metadata['parts_supplied'].apply(
                lambda value: value if isinstance(value, list) else []
            )
        if 'supplies_to' in supplier_metadata.columns:
            supplier_metadata['supplies_to'] = supplier_metadata['supplies_to'].apply(
                lambda value: value if isinstance(value, list) else []
            )

        print(f"\n[3] Loaded supplier metadata from: {supplier_json_path}")
        print(f"    - Supplier profiles loaded: {len(supplier_metadata)}")
        print(f"    - Risk levels: {supplier_metadata['risk_level'].value_counts().to_dict() if 'risk_level' in supplier_metadata.columns else 'n/a'}")

# Data validation and cleaning
print("\n[4] Data Validation:")

# Check for inconsistent values
print(f"   - Disruption Types: {df['disruption_type'].nunique()} unique values")
print(f"     {df['disruption_type'].unique()}")

print(f"   - Industries: {df['industry'].nunique()} unique values")
print(f"   - Supplier Regions: {df['supplier_region'].nunique()} unique values")
print(f"   - Supplier Sizes: {df['supplier_size'].nunique()} unique values")
print(f"     {df['supplier_size'].unique()}")

print(f"   - Response Types: {df['response_type'].nunique()} unique values")
print(f"     {df['response_type'].unique()}")

# Standardize categorical values to lowercase
df['disruption_type'] = df['disruption_type'].str.lower().str.strip()
df['industry'] = df['industry'].str.lower().str.strip()
df['supplier_region'] = df['supplier_region'].str.lower().str.strip()
df['supplier_size'] = df['supplier_size'].str.lower().str.strip()
df['response_type'] = df['response_type'].str.lower().str.strip()

print("\n[5] Standardized categorical columns to lowercase")

# Optional supplier metadata summary for data inspection
if supplier_metadata is not None and not supplier_metadata.empty:
    print("\n[6] Supplier metadata preview:")
    preview_cols = [col for col in ['id', 'name', 'tier', 'location', 'risk_level'] if col in supplier_metadata.columns]
    print(supplier_metadata[preview_cols].head(10).to_string(index=False))

    print("\n[7] Relevant supplier context for this dataset:")
    print("    - Only tier/location/risk_level are relevant to the current CSV schema")
    print("    - Fields such as parts_supplied and supplies_to are not directly usable")

# Check for outliers/invalid ranges
print("\n[8] Range Validation:")
print(f"   - Disruption Severity: {df['disruption_severity'].min()} to {df['disruption_severity'].max()}")
print(f"   - Production Impact %: {df['production_impact_pct'].min()} to {df['production_impact_pct'].max()}")
print(f"   - Revenue Loss USD: ${df['revenue_loss_usd'].min():,.0f} to ${df['revenue_loss_usd'].max():,.0f}")
print(f"   - Response Time Days: {df['response_time_days'].min()} to {df['response_time_days'].max()}")
print(f"   - Partial Recovery Days: {df['partial_recovery_days'].min()} to {df['partial_recovery_days'].max()}")
print(f"   - Full Recovery Days: {df['full_recovery_days'].min()} to {df['full_recovery_days'].max()}")

# Ensure recovery days are logical (partial <= full)
invalid_recovery = (df['partial_recovery_days'] > df['full_recovery_days']).sum()
if invalid_recovery > 0:
    print(f"   WARNING: {invalid_recovery} rows with partial_recovery > full_recovery")
    # Fix if needed
    mask = df['partial_recovery_days'] > df['full_recovery_days']
    df.loc[mask, ['partial_recovery_days', 'full_recovery_days']] = \
        df.loc[mask, ['full_recovery_days', 'partial_recovery_days']].values

# Data types
print("\n[9] Final Data Types:")
print(df.dtypes)

# Summary statistics
print("\n[10] Summary Statistics:")
print(df.describe())

# Correlation for numeric columns
print("\n[11] Numeric Correlations with Revenue Loss:")
numeric_cols = df.select_dtypes(include=[np.number]).columns
correlations = df[numeric_cols].corr()['revenue_loss_usd'].sort_values(ascending=False)
print(correlations)

# Create output directory if needed
output_dir = project_root / "data"
output_dir.mkdir(exist_ok=True)

# Save cleaned data
output_file = output_dir / "supply_chain_cleaned.csv"
df.to_csv(output_file, index=False)
print(f"\n[12] Cleaned dataset saved: {output_file}")
print(f"    Final shape: {df.shape[0]} rows, {df.shape[1]} columns")

print("\n" + "=" * 60)
print("CLEANING COMPLETE")
print("=" * 60)
