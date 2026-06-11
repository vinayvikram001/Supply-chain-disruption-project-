import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("SUPPLY CHAIN DISRUPTION - MODEL PREDICTION")
print("=" * 70)

# ============================================================================
# LOAD MODEL & ARTIFACTS
# ============================================================================
script_dir = Path(__file__).parent
models_dir = script_dir / "models"

print(f"\n[1] Loading Model & Artifacts from: {models_dir}")

# Load all saved artifacts
model = joblib.load(models_dir / "random_forest_model.pkl")
scaler = joblib.load(models_dir / "scaler.pkl")
label_encoders = joblib.load(models_dir / "label_encoders.pkl")

with open(models_dir / "feature_names.txt", 'r') as f:
    feature_names = [line.strip() for line in f.readlines()]

print(f"    ✓ Model loaded")
print(f"    ✓ Scaler loaded")
print(f"    ✓ Label encoders loaded ({len(label_encoders)} categorical features)")
print(f"    ✓ Feature names loaded ({len(feature_names)} features)")

# ============================================================================
# EXAMPLE PREDICTIONS
# ============================================================================
print(f"\n[2] Example Predictions:")

# Create sample scenarios
example_data = pd.DataFrame({
    'disruption_type': ['natural_disaster', 'supplier_bankruptcy', 'labor_strike'],
    'industry': ['automotive', 'electronics', 'food_beverage'],
    'supplier_region': ['asia', 'north_america', 'europe'],
    'supplier_size': ['large', 'small', 'medium'],
    'response_type': ['alternative_supplier', 'demand_adjustment', 'inventory_buffer'],
    'disruption_severity': [8, 6, 5],
    'production_impact_pct': [75, 45, 30]
})

print(f"\n    Scenario Data:")
print(example_data.to_string(index=False))

# Encode the example data
example_encoded = example_data.copy()
for col in label_encoders.keys():
    if col in example_encoded.columns:
        example_encoded[col] = label_encoders[col].transform(
            example_encoded[col].astype(str)
        )

# Make predictions
predictions = model.predict(example_encoded)

print(f"\n    Predictions:")
print("    " + "-" * 70)
for idx, (scenario_idx, pred) in enumerate(enumerate(predictions)):
    print(f"\n    Scenario {scenario_idx + 1}:")
    for col in example_data.columns:
        print(f"      {col}: {example_data.iloc[scenario_idx][col]}")
    print(f"      → Predicted Full Recovery: {pred:.1f} days")
    print("    " + "-" * 70)

# ============================================================================
# BATCH PREDICTION FROM CLEANED DATA
# ============================================================================
print(f"\n[3] Batch Predictions on Test Set:")

project_root = script_dir.parent
data_path = project_root / "data" / "supply_chain_cleaned.csv"

df = pd.read_csv(data_path)

# Use first 10 rows for demonstration
sample_df = df.iloc[:10].copy()
X_sample = sample_df.drop(
    columns=['full_recovery_days', 'partial_recovery_days', 
             'response_time_days', 'revenue_loss_usd']
)

# Encode
X_sample_encoded = X_sample.copy()
for col in label_encoders.keys():
    if col in X_sample_encoded.columns:
        X_sample_encoded[col] = label_encoders[col].transform(
            X_sample_encoded[col].astype(str)
        )

# Predict
batch_predictions = model.predict(X_sample_encoded)
actual_values = sample_df['full_recovery_days'].values

print(f"\n    Sample Predictions vs Actual:")
print("    " + "-" * 70)
print(f"    {'Index':<8} {'Actual Days':<15} {'Predicted Days':<15} {'Error':<15}")
print("    " + "-" * 70)

errors = []
for idx, (actual, pred) in enumerate(zip(actual_values, batch_predictions)):
    error = abs(actual - pred)
    errors.append(error)
    print(f"    {idx:<8} {actual:<15.1f} {pred:<15.1f} {error:<15.1f}")

print("    " + "-" * 70)
print(f"    Average Prediction Error: {np.mean(errors):.2f} days")
print(f"    Min Error: {np.min(errors):.2f} days")
print(f"    Max Error: {np.max(errors):.2f} days")

print("\n" + "=" * 70)
print("PREDICTION COMPLETE")
print("=" * 70)
