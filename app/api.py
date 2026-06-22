from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Supply Chain Disruption API",
    description="API for predicting recovery outcomes from disruption inputs.",
    version="1.0.0",
)

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"

model = None
label_encoders = None
feature_names = []


def find_model_file():
    preferred_names = [
        "random_forest_model.pkl",
        "gradient_boosting_model.pkl",
        "linear_regression_model.pkl",
    ]

    for name in preferred_names:
        candidate = MODELS_DIR / name
        if candidate.exists():
            return candidate

    model_files = sorted(MODELS_DIR.glob("*_model.pkl"))
    if model_files:
        return model_files[0]

    return None


def load_artifacts():
    global model, label_encoders, feature_names

    if not MODELS_DIR.exists():
        return False

    model_path = find_model_file()

    required_files = [
        model_path,
        MODELS_DIR / "scaler.pkl",
        MODELS_DIR / "label_encoders.pkl",
        MODELS_DIR / "feature_names.txt",
    ]

    if not all(file is not None and file.exists() for file in required_files):
        return False

    model = joblib.load(required_files[0])
    joblib.load(required_files[1])  # scaler loaded if needed later
    label_encoders = joblib.load(required_files[2])

    with open(required_files[3], "r", encoding="utf-8") as f:
        feature_names = [line.strip() for line in f.readlines()]

    return True


load_artifacts()


class PredictionInput(BaseModel):
    disruption_type: str
    industry: str
    supplier_region: str
    supplier_size: str
    response_type: str
    disruption_severity: float
    production_impact_pct: float


@app.get("/")
def root():
    return {
        "message": "Supply Chain Disruption Prediction API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None and label_encoders is not None,
        "models_dir_exists": MODELS_DIR.exists(),
    }


@app.post("/predict")
def predict(payload: PredictionInput):
    if model is None or label_encoders is None or not feature_names:
        raise HTTPException(
            status_code=503,
            detail=(
                "Model artifacts are not available yet. "
                "Run the training pipeline first to generate the model files."
            ),
        )

    input_df = pd.DataFrame([payload.model_dump()])

    for col in label_encoders:
        if col in input_df.columns:
            input_df[col] = label_encoders[col].transform(
                input_df[col].astype(str)
            )

    input_df = input_df.reindex(columns=feature_names, fill_value=0)

    prediction = float(model.predict(input_df)[0])

    return {
        "predicted_full_recovery_days": round(prediction, 2),
        "input": payload.model_dump(),
    }