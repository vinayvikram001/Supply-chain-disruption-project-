import streamlit as st
import requests

st.set_page_config(page_title="Supply Chain Disruption Predictor")

st.title("🚚 Supply Chain Disruption Predictor")

disruption_type = st.selectbox(
    "Disruption Type",
    [
        "cyber attack",
        "factory incident",
        "geopolitical",
        "labor strike",
        "natural disaster",
        "port congestion",
    ],
)

industry = st.text_input("Industry", "automotive")

supplier_region = st.selectbox(
    "Supplier Region",
    [
        "africa/middle east",
        "asia-pacific",
        "europe",
        "north america",
        "south america",
    ],
)

supplier_size = st.text_input("Supplier Size", "large")

response_type = st.text_input("Response Type", "alternative supplier")

disruption_severity = st.slider("Severity", 1, 10, 8)

production_impact_pct = st.slider(
    "Production Impact (%)",
    0,
    100,
    75,
)

if st.button("Predict Recovery Time"):

    payload = {
        "disruption_type": disruption_type,
        "industry": industry,
        "supplier_region": supplier_region,
        "supplier_size": supplier_size,
        "response_type": response_type,
        "disruption_severity": disruption_severity,
        "production_impact_pct": production_impact_pct,
    }

    response = requests.post(
        "http://localhost:8000/predict",
        json=payload,
    )

    if response.status_code == 200:
        data = response.json()

        st.success(
            f"Predicted Recovery Time: "
            f"{data['predicted_full_recovery_days']:.2f} days"
        )

        st.json(data)

    else:
        st.error(response.text)