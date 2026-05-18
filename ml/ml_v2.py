import mysql.connector
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score, f1_score
import joblib
import warnings
warnings.filterwarnings('ignore')

# ── Chargement direct depuis les CSV originaux ──────────────
diabetes = pd.read_csv("C:/Users/youne/OneDrive/Desktop/datasets/diabetes.csv")
heart = pd.read_csv("C:/Users/youne/OneDrive/Desktop/datasets/heart.csv")
heart = heart.drop_duplicates()  # ← ajoute cette ligne
print("Après suppression doublons:", heart.shape)
print("Diabetes shape:", diabetes.shape)
print("Heart shape:", heart.shape)

# ══════════════════════════════════════════════════════════
# MODELE 1 — DIABETES
# ══════════════════════════════════════════════════════════
print("\n" + "="*60)
print("MODELE 1 — DIABETES")
print("="*60)

# Remplacement des 0 par médiane (valeurs impossibles médicalement)
cols_zero = ['Glucose','BloodPressure','SkinThickness','Insulin','BMI']
for col in cols_zero:
    diabetes[col] = diabetes[col].replace(0, np.nan)
    diabetes[col] = diabetes[col].fillna(diabetes[col].median())

X_diab = diabetes[['Pregnancies','Glucose','BloodPressure',
                    'SkinThickness','Insulin','BMI',
                    'DiabetesPedigreeFunction','Age']]
y_diab = diabetes['Outcome']

X_train, X_test, y_train, y_test = train_test_split(
    X_diab, y_diab, test_size=0.2, random_state=42, stratify=y_diab
)

scaler1 = StandardScaler()
X_train_sc = scaler1.fit_transform(X_train)
X_test_sc  = scaler1.transform(X_test)

models_diab = {
    "Random Forest":     RandomForestClassifier(n_estimators=200, random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=200, random_state=42),
    "MLP":               MLPClassifier(hidden_layer_sizes=(128,64,32), max_iter=1000, random_state=42),
    "SVM":               SVC(probability=True, C=10, gamma='scale', random_state=42),
}

best_diab_auc = 0
best_diab_model = None

for name, model in models_diab.items():
    model.fit(X_train_sc, y_train)
    y_prob = model.predict_proba(X_test_sc)[:, 1]
    y_pred = model.predict(X_test_sc)
    auc = roc_auc_score(y_test, y_prob)
    f1  = f1_score(y_test, y_pred)
    acc = model.score(X_test_sc, y_test)
    print(f"{name:25} Accuracy:{acc:.4f}  AUC:{auc:.4f}  F1:{f1:.4f}")
    if auc > best_diab_auc:
        best_diab_auc = auc
        best_diab_model = (name, model)

print(f"\n Meilleur Diabetes : {best_diab_model[0]} (AUC={best_diab_auc:.4f})")

# ══════════════════════════════════════════════════════════
# MODELE 2 — HEART DISEASE
# ══════════════════════════════════════════════════════════
print("\n" + "="*60)
print("MODELE 2 — HEART DISEASE")
print("="*60)

heart = heart.dropna()

X_heart = heart[['age','sex','cp','trestbps','chol',
                  'fbs','restecg','thalach','exang',
                  'oldpeak','slope','ca','thal']]
y_heart = heart['target']

X_train, X_test, y_train, y_test = train_test_split(
    X_heart, y_heart, test_size=0.2, random_state=42, stratify=y_heart
)

scaler2 = StandardScaler()
X_train_sc = scaler2.fit_transform(X_train)
X_test_sc  = scaler2.transform(X_test)

models_heart = {
    "Random Forest":     RandomForestClassifier(n_estimators=200, random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=200, random_state=42),
    "MLP":               MLPClassifier(hidden_layer_sizes=(128,64,32), max_iter=1000, random_state=42),
    "SVM":               SVC(probability=True, C=10, gamma='scale', random_state=42),
}

best_heart_auc = 0
best_heart_model = None

for name, model in models_heart.items():
    model.fit(X_train_sc, y_train)
    y_prob = model.predict_proba(X_test_sc)[:, 1]
    y_pred = model.predict(X_test_sc)
    auc = roc_auc_score(y_test, y_prob)
    f1  = f1_score(y_test, y_pred)
    acc = model.score(X_test_sc, y_test)
    print(f"{name:25} Accuracy:{acc:.4f}  AUC:{auc:.4f}  F1:{f1:.4f}")
    if auc > best_heart_auc:
        best_heart_auc = auc
        best_heart_model = (name, model)

print(f"\n Meilleur Heart : {best_heart_model[0]} (AUC={best_heart_auc:.4f})")

# ── Sauvegarde des meilleurs modèles ────────────────────────
joblib.dump(best_diab_model[1],  "model_diabetes.pkl")
joblib.dump(best_heart_model[1], "model_heart.pkl")
joblib.dump(scaler1, "scaler_diabetes.pkl")
joblib.dump(scaler2, "scaler_heart.pkl")

print("\n" + "="*60)
print("RESUME FINAL")
print("="*60)
print(f"Diabetes  → Meilleur modèle : {best_diab_model[0]}  AUC : {best_diab_auc:.4f}")
print(f"Heart     → Meilleur modèle : {best_heart_model[0]}  AUC : {best_heart_auc:.4f}")
print("\nModèles sauvegardés : model_diabetes.pkl, model_heart.pkl")