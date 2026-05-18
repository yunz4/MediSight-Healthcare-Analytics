import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# ── Chargement des modèles ──────────────────────────────────
model_diabetes  = joblib.load(r"C:\Users\youne\model_diabetes.pkl")
model_heart     = joblib.load(r"C:\Users\youne\model_heart.pkl")
scaler_diabetes = joblib.load(r"C:\Users\youne\scaler_diabetes.pkl")
scaler_heart    = joblib.load(r"C:\Users\youne\scaler_heart.pkl")

app = FastAPI(
    title="MediSight API",
    description="API de prédiction du risque maladie — Diabète & Maladies Cardiaques",
    version="1.0.0"
)

# ── Schémas des requêtes ────────────────────────────────────
class DiabetesInput(BaseModel):
    pregnancies: float
    glucose: float
    blood_pressure: float
    skin_thickness: float
    insulin: float
    bmi: float
    diabetes_pedigree: float
    age: int

class HeartInput(BaseModel):
    age: int
    sex: int              # 1=homme, 0=femme
    cp: int               # type douleur thoracique (0-3)
    trestbps: float       # pression artérielle
    chol: float           # cholestérol
    fbs: int              # glycémie à jeun > 120 mg/dl (1=oui)
    restecg: int          # résultats ECG (0-2)
    thalach: float        # fréquence cardiaque max
    exang: int            # angine à l'effort (1=oui)
    oldpeak: float        # dépression ST
    slope: int            # pente segment ST (0-2)
    ca: int               # nb vaisseaux colorés (0-4)
    thal: int             # thal (0-3)

# ── Endpoints ───────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "message": "Bienvenue sur MediSight API",
        "version": "1.0.0",
        "endpoints": {
            "predict_diabetes": "/predict/diabetes",
            "predict_heart": "/predict/heart",
            "docs": "/docs"
        }
    }

@app.post("/predict/diabetes")
def predict_diabetes(data: DiabetesInput):
    features = np.array([[
        data.pregnancies, data.glucose, data.blood_pressure,
        data.skin_thickness, data.insulin, data.bmi,
        data.diabetes_pedigree, data.age
    ]])

    features_scaled = scaler_diabetes.transform(features)
    prediction      = model_diabetes.predict(features_scaled)[0]
    probability     = model_diabetes.predict_proba(features_scaled)[0][1]

    return {
        "disease": "Diabetes",
        "prediction": int(prediction),
        "result": "POSITIF — Risque de diabète détecté" if prediction == 1 else "NEGATIF — Pas de risque détecté",
        "probability": round(float(probability) * 100, 2),
        "model": "Gradient Boosting",
        "auc_model": 0.8259
    }

@app.post("/predict/heart")
def predict_heart(data: HeartInput):
    features = np.array([[
        data.age, data.sex, data.cp, data.trestbps, data.chol,
        data.fbs, data.restecg, data.thalach, data.exang,
        data.oldpeak, data.slope, data.ca, data.thal
    ]])

    features_scaled = scaler_heart.transform(features)
    prediction      = model_heart.predict(features_scaled)[0]
    probability     = model_heart.predict_proba(features_scaled)[0][1]

    return {
        "disease": "Heart Disease",
        "prediction": int(prediction),
        "result": "POSITIF — Risque cardiaque détecté" if prediction == 1 else "NEGATIF — Pas de risque détecté",
        "probability": round(float(probability) * 100, 2),
        "model": "Random Forest",
        "auc_model": 0.8680
    }

@app.get("/health")
def health():
    return {"status": "OK", "models_loaded": ["Diabetes (Gradient Boosting)", "Heart Disease (Random Forest)"]}