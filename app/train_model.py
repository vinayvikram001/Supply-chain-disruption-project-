import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("SUPPLY CHAIN DISRUPTION - MODEL TRAINING PIPELINE")
print("=" * 70)

# ============================================================================
# 1. LOAD CLEANED DATA
# ============================================================================
script_dir = Path(__file__).parent
project_root = script_dir.parent
data_path = project_root / "data" / "supply_chain_cleaned.csv"

print(f"\n[1] Loading cleaned dataset from: {data_path}")
df = pd.read_csv(data_path)
print(f"    Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"    Columns: {list(df.columns)}")

# ============================================================================
# 2. DATA EXPLORATION
# ============================================================================
print("\n[2] Data Exploration:")
print(f"    Missing values: {df.isnull().sum().sum()}")
print(f"\n    Data types:\n{df.dtypes}")
print(f"\n    Numeric summary:\n{df.describe()}")

# ============================================================================
# 3. DEFINE TARGET AND FEATURES
# ============================================================================
# Predicting: Full recovery days based on disruption characteristics
TARGET = 'full_recovery_days'
EXCLUDE_COLS = [TARGET, 'partial_recovery_days', 'response_time_days', 'revenue_loss_usd']

print(f"\n[3] Model Configuration:")
print(f"    Target Variable: {TARGET}")
print(f"    Excluded Columns: {EXCLUDE_COLS}")

X = df.drop(columns=EXCLUDE_COLS)
y = df[TARGET]

print(f"    Features shape: {X.shape}")
print(f"    Target shape: {y.shape}")
print(f"    Target range: {y.min()} - {y.max()} days")

# ============================================================================
# 4. FEATURE ENGINEERING & ENCODING
# ============================================================================
print("\n[4] Feature Engineering:")

# Identify categorical and numeric columns
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()

print(f"    Categorical features: {categorical_cols}")
print(f"    Numeric features: {numeric_cols}")

# Store original X for later use
X_encoded = X.copy()

# Encode categorical variables
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    X_encoded[col] = le.fit_transform(X_encoded[col].astype(str))
    label_encoders[col] = le
    print(f"    Encoded '{col}': {len(le.classes_)} unique values")

# ============================================================================
# 5. TRAIN-TEST SPLIT
# ============================================================================
print("\n[5] Train-Test Split:")
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42
)

print(f"    Training set: {X_train.shape[0]} samples ({X_train.shape[0]/len(X)*100:.1f}%)")
print(f"    Test set: {X_test.shape[0]} samples ({X_test.shape[0]/len(X)*100:.1f}%)")

# ============================================================================
# 6. FEATURE SCALING
# ============================================================================
print("\n[6] Feature Scaling:")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print(f"    Applied StandardScaler to normalize features")

# ============================================================================
# 7. MODEL TRAINING
# ============================================================================
print("\n[7] Training Models:")

models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
}

results = {}

for model_name, model in models.items():
    print(f"\n    Training {model_name}...")
    
    # Use scaled data for Linear Regression, original for tree-based models
    if model_name == 'Linear Regression':
        model.fit(X_train_scaled, y_train)
        y_pred_train = model.predict(X_train_scaled)
        y_pred_test = model.predict(X_test_scaled)
    else:
        model.fit(X_train, y_train)
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
    
    # Calculate metrics
    train_mse = mean_squared_error(y_train, y_pred_train)
    test_mse = mean_squared_error(y_test, y_pred_test)
    train_mae = mean_absolute_error(y_train, y_pred_train)
    test_mae = mean_absolute_error(y_test, y_pred_test)
    train_r2 = r2_score(y_train, y_pred_train)
    test_r2 = r2_score(y_test, y_pred_test)
    
    results[model_name] = {
        'model': model,
        'train_mse': train_mse,
        'test_mse': test_mse,
        'train_mae': train_mae,
        'test_mae': test_mae,
        'train_r2': train_r2,
        'test_r2': test_r2,
        'y_pred_test': y_pred_test
    }
    
    print(f"      Train MSE: {train_mse:.2f} | Test MSE: {test_mse:.2f}")
    print(f"      Train MAE: {train_mae:.2f} | Test MAE: {test_mae:.2f}")
    print(f"      Train R²: {train_r2:.4f} | Test R²: {test_r2:.4f}")

# ============================================================================
# 8. MODEL COMPARISON & SELECTION
# ============================================================================
print("\n[8] Model Comparison:")
print("\n    Model Performance Summary:")
print("    " + "-" * 70)
print(f"    {'Model':<25} {'Test MAE':<15} {'Test R²':<15} {'Overfitting':<15}")
print("    " + "-" * 70)

best_model_name = None
best_test_r2 = -np.inf

for model_name, result in results.items():
    test_mae = result['test_mae']
    test_r2 = result['test_r2']
    train_r2 = result['train_r2']
    overfitting = train_r2 - test_r2
    
    print(f"    {model_name:<25} {test_mae:<15.4f} {test_r2:<15.4f} {overfitting:<15.4f}")
    
    if test_r2 > best_test_r2:
        best_test_r2 = test_r2
        best_model_name = model_name

print("    " + "-" * 70)
print(f"\n    ✓ Best Model: {best_model_name} (Test R² = {best_test_r2:.4f})")

best_model = results[best_model_name]['model']

# ============================================================================
# 9. FEATURE IMPORTANCE (for tree-based models)
# ============================================================================
if hasattr(best_model, 'feature_importances_'):
    print(f"\n[9] Feature Importance ({best_model_name}):")
    feature_importance = pd.DataFrame({
        'Feature': X_encoded.columns,
        'Importance': best_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print(f"    Top 10 Features:")
    for idx, row in feature_importance.head(10).iterrows():
        print(f"      {row['Feature']:<30} {row['Importance']:.4f}")
else:
    print(f"\n[9] Feature Importance: Not available for {best_model_name}")
    if 'Linear Regression' in best_model_name:
        print(f"    Coefficients:")
        coefs = pd.DataFrame({
            'Feature': X_encoded.columns,
            'Coefficient': best_model.coef_
        }).sort_values('Coefficient', ascending=False)
        for idx, row in coefs.head(10).iterrows():
            print(f"      {row['Feature']:<30} {row['Coefficient']:.4f}")

# ============================================================================
# 10. SAVE MODEL & PREPROCESSING OBJECTS
# ============================================================================
print(f"\n[10] Saving Models and Artifacts:")

models_dir = script_dir / "models"
models_dir.mkdir(exist_ok=True)

# Save best model
model_path = models_dir / f"{best_model_name.replace(' ', '_').lower()}_model.pkl"
joblib.dump(best_model, model_path)
print(f"    ✓ Saved model: {model_path}")

# Save scaler
scaler_path = models_dir / "scaler.pkl"
joblib.dump(scaler, scaler_path)
print(f"    ✓ Saved scaler: {scaler_path}")

# Save label encoders
encoders_path = models_dir / "label_encoders.pkl"
joblib.dump(label_encoders, encoders_path)
print(f"    ✓ Saved label encoders: {encoders_path}")

# Save feature names
feature_names_path = models_dir / "feature_names.txt"
with open(feature_names_path, 'w') as f:
    for col in X_encoded.columns:
        f.write(f"{col}\n")
print(f"    ✓ Saved feature names: {feature_names_path}")

# ============================================================================
# 11. VISUALIZATION & ANALYSIS
# ============================================================================
print(f"\n[11] Generating Visualizations:")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Actual vs Predicted (Best Model)
ax = axes[0, 0]
ax.scatter(y_test, results[best_model_name]['y_pred_test'], alpha=0.6, s=50)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
ax.set_xlabel('Actual Full Recovery Days')
ax.set_ylabel('Predicted Full Recovery Days')
ax.set_title(f'Actual vs Predicted - {best_model_name}')
ax.grid(True, alpha=0.3)

# Plot 2: Residuals
ax = axes[0, 1]
residuals = y_test - results[best_model_name]['y_pred_test']
ax.scatter(results[best_model_name]['y_pred_test'], residuals, alpha=0.6, s=50)
ax.axhline(y=0, color='r', linestyle='--', lw=2)
ax.set_xlabel('Predicted Values')
ax.set_ylabel('Residuals')
ax.set_title('Residual Plot')
ax.grid(True, alpha=0.3)

# Plot 3: Model Comparison
ax = axes[1, 0]
model_names = list(results.keys())
test_r2_scores = [results[m]['test_r2'] for m in model_names]
colors = ['green' if m == best_model_name else 'lightblue' for m in model_names]
ax.bar(model_names, test_r2_scores, color=colors)
ax.set_ylabel('Test R² Score')
ax.set_title('Model Comparison')
ax.set_ylim([0, 1])
for i, v in enumerate(test_r2_scores):
    ax.text(i, v + 0.02, f'{v:.3f}', ha='center', va='bottom')

# Plot 4: Error Distribution
ax = axes[1, 1]
ax.hist(residuals, bins=20, edgecolor='black', alpha=0.7)
ax.set_xlabel('Prediction Error (days)')
ax.set_ylabel('Frequency')
ax.set_title('Distribution of Prediction Errors')
ax.grid(True, alpha=0.3)

plt.tight_layout()
viz_path = models_dir / "training_analysis.png"
plt.savefig(viz_path, dpi=300, bbox_inches='tight')
print(f"    ✓ Saved visualization: {viz_path}")

# ============================================================================
# 12. SUMMARY REPORT
# ============================================================================
print("\n" + "=" * 70)
print("TRAINING COMPLETE - SUMMARY REPORT")
print("=" * 70)
print(f"""
Dataset: {df.shape[0]} samples, {df.shape[1]} features
Training Set: {X_train.shape[0]} samples
Test Set: {X_test.shape[0]} samples

Target Variable: {TARGET} (range: {y.min()}-{y.max()} days)

Best Model: {best_model_name}
  - Test R² Score: {results[best_model_name]['test_r2']:.4f}
  - Test MAE: {results[best_model_name]['test_mae']:.2f} days
  - Test RMSE: {np.sqrt(results[best_model_name]['test_mse']):.2f} days

Artifacts Saved to: {models_dir}
  - Model: {best_model_name.replace(' ', '_').lower()}_model.pkl
  - Scaler: scaler.pkl
  - Label Encoders: label_encoders.pkl
  - Feature Names: feature_names.txt
  - Analysis Plot: training_analysis.png

Next Steps:
  1. Use 'evaluate_model.py' to test on new data
  2. Use 'predict_recovery.py' for predictions on specific cases
  3. Monitor model performance over time
""")
print("=" * 70)
