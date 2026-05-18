import streamlit as st
import requests
import json

st.set_page_config(
    page_title="MediSight — Prédiction Médicale",
    page_icon="🏥",
    layout="wide"
)

# ── Style CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f0f4f8; }
    .stButton>button {
        background-color: #2E75B6;
        color: white;
        border-radius: 8px;
        padding: 10px 30px;
        font-size: 16px;
        width: 100%;
    }
    .result-positive {
        background-color: #FADBD8;
        border-left: 5px solid #E74C3C;
        padding: 20px;
        border-radius: 8px;
        font-size: 18px;
    }
    .result-negative {
        background-color: #D5F5E3;
        border-left: 5px solid #27AE60;
        padding: 20px;
        border-radius: 8px;
        font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────
st.markdown("<h1 style='text-align:center; color:#1F4E79;'>🏥 MediSight</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:#555;'>Plateforme de Prédiction du Risque Maladie</h4>", unsafe_allow_html=True)
st.markdown("---")

# ── Sélection maladie ───────────────────────────────────────
disease = st.radio(
    "Choisissez le type de prédiction :",
    ["🩸 Diabète", "❤️ Maladie Cardiaque"],
    horizontal=True
)

st.markdown("---")

# ══════════════════════════════════════════════════════════
# FORMULAIRE DIABÈTE
# ══════════════════════════════════════════════════════════
if disease == "🩸 Diabète":
    st.subheader("🩸 Formulaire — Prédiction du Diabète")
    st.caption("Modèle : Gradient Boosting | AUC = 0.8259")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Âge", min_value=1, max_value=120, value=35)
        glucose = st.number_input("Glucose (mg/dL)", min_value=0.0, max_value=300.0, value=120.0)
        bmi = st.number_input("IMC (BMI)", min_value=0.0, max_value=70.0, value=28.0)

    with col2:
        pregnancies = st.number_input("Nombre de grossesses", min_value=0, max_value=20, value=1)
        blood_pressure = st.number_input("Pression artérielle (mm Hg)", min_value=0.0, max_value=200.0, value=70.0)
        insulin = st.number_input("Insuline (mu U/ml)", min_value=0.0, max_value=900.0, value=80.0)

    with col3:
        skin_thickness = st.number_input("Épaisseur peau (mm)", min_value=0.0, max_value=100.0, value=20.0)
        diabetes_pedigree = st.number_input("Fonction pedigree diabète", min_value=0.0, max_value=3.0, value=0.5, step=0.01)

    st.markdown("---")

    if st.button("🔍 Analyser le risque de diabète"):
        payload = {
            "pregnancies": pregnancies,
            "glucose": glucose,
            "blood_pressure": blood_pressure,
            "skin_thickness": skin_thickness,
            "insulin": insulin,
            "bmi": bmi,
            "diabetes_pedigree": diabetes_pedigree,
            "age": age
        }

        try:
            response = requests.post("http://127.0.0.1:8000/predict/diabetes", json=payload)
            result = response.json()

            st.markdown("### Résultat de l'analyse")

            if result["prediction"] == 1:
                st.markdown(f"""
                <div class='result-positive'>
                    🔴 <b>{result['result']}</b><br><br>
                    Probabilité de diabète : <b>{result['probability']}%</b>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='result-negative'>
                    🟢 <b>{result['result']}</b><br><br>
                    Probabilité de diabète : <b>{result['probability']}%</b>
                </div>
                """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            col1.metric("Probabilité", f"{result['probability']}%")
            col2.metric("Modèle utilisé", result['model'])
            col3.metric("AUC du modèle", result['auc_model'])

        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")

# ══════════════════════════════════════════════════════════
# FORMULAIRE CARDIAQUE
# ══════════════════════════════════════════════════════════
else:
    st.subheader("❤️ Formulaire — Prédiction Maladie Cardiaque")
    st.caption("Modèle : Random Forest | AUC = 0.8680")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Âge", min_value=1, max_value=120, value=55)
        trestbps = st.number_input("Pression artérielle (mm Hg)", min_value=0.0, max_value=300.0, value=130.0)
        chol = st.number_input("Cholestérol (mg/dL)", min_value=0.0, max_value=600.0, value=250.0)
        thalach = st.number_input("Fréquence cardiaque max", min_value=0.0, max_value=250.0, value=150.0)
        oldpeak = st.number_input("Dépression ST", min_value=0.0, max_value=10.0, value=1.0, step=0.1)

    with col2:
        sex = st.selectbox("Sexe", options=[1, 0], format_func=lambda x: "Homme" if x == 1 else "Femme")
        cp = st.selectbox("Type douleur thoracique", options=[0,1,2,3],
            format_func=lambda x: {0:"Asymptomatique", 1:"Angine typique", 2:"Angine atypique", 3:"Douleur non-angineuse"}[x])
        fbs = st.selectbox("Glycémie à jeun > 120 mg/dL", options=[0,1], format_func=lambda x: "Oui" if x==1 else "Non")
        restecg = st.selectbox("Résultat ECG repos", options=[0,1,2],
            format_func=lambda x: {0:"Normal", 1:"Anomalie ST-T", 2:"Hypertrophie"}[x])

    with col3:
        exang = st.selectbox("Angine à l'effort", options=[0,1], format_func=lambda x: "Oui" if x==1 else "Non")
        slope = st.selectbox("Pente segment ST", options=[0,1,2],
            format_func=lambda x: {0:"Descendante", 1:"Plate", 2:"Ascendante"}[x])
        ca = st.number_input("Nb vaisseaux colorés (0-4)", min_value=0, max_value=4, value=0)
        thal = st.selectbox("Thalassémie", options=[0,1,2,3],
            format_func=lambda x: {0:"Normal", 1:"Défaut fixe", 2:"Défaut réversible", 3:"Inconnu"}[x])

    st.markdown("---")

    if st.button("🔍 Analyser le risque cardiaque"):
        payload = {
            "age": age, "sex": sex, "cp": cp,
            "trestbps": trestbps, "chol": chol, "fbs": fbs,
            "restecg": restecg, "thalach": thalach, "exang": exang,
            "oldpeak": oldpeak, "slope": slope, "ca": ca, "thal": thal
        }

        try:
            response = requests.post("http://127.0.0.1:8000/predict/heart", json=payload)
            result = response.json()

            st.markdown("### Résultat de l'analyse")

            if result["prediction"] == 1:
                st.markdown(f"""
                <div class='result-positive'>
                    🔴 <b>{result['result']}</b><br><br>
                    Probabilité de maladie cardiaque : <b>{result['probability']}%</b>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='result-negative'>
                    🟢 <b>{result['result']}</b><br><br>
                    Probabilité de maladie cardiaque : <b>{result['probability']}%</b>
                </div>
                """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            col1.metric("Probabilité", f"{result['probability']}%")
            col2.metric("Modèle utilisé", result['model'])
            col3.metric("AUC du modèle", result['auc_model'])

        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")

# ── Footer ──────────────────────────────────────────────────
st.markdown("---")
st.markdown("<p style='text-align:center; color:#888;'>MediSight v1.0 — Powered by Gradient Boosting & Random Forest | GitHub : github.com/yunz4/MediSight-Healthcare-Analytics</p>", unsafe_allow_html=True)