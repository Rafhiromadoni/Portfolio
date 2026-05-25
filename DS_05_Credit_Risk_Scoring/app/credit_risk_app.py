import streamlit as st
import pandas as pd
import joblib

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="Credit Risk Scoring App",
    page_icon="💳",
    layout="wide"
)

# =========================
# Load Model
# =========================
MODEL_PATH = "model/credit_risk_model.pkl"

@st.cache_resource
def load_model():
    model = joblib.load(MODEL_PATH)
    return model

model = load_model()

# =========================
# App Title
# =========================
st.title("💳 Credit Risk Scoring App")
st.write(
    "This app predicts the probability of loan default and classifies applicants "
    "into Low Risk, Medium Risk, or High Risk segments."
)

st.divider()

# =========================
# Input Form
# =========================
st.subheader("Applicant Information")

col1, col2, col3 = st.columns(3)

with col1:
    person_age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30
    )

    person_income = st.number_input(
        "Annual Income",
        min_value=0,
        value=60000,
        step=1000
    )

    person_home_ownership = st.selectbox(
        "Home Ownership",
        ["RENT", "OWN", "MORTGAGE", "OTHER"]
    )

    person_emp_length = st.number_input(
        "Employment Length (Years)",
        min_value=0.0,
        max_value=50.0,
        value=5.0,
        step=0.5
    )

with col2:
    loan_intent = st.selectbox(
        "Loan Intent",
        [
            "PERSONAL",
            "EDUCATION",
            "MEDICAL",
            "VENTURE",
            "HOMEIMPROVEMENT",
            "DEBTCONSOLIDATION"
        ]
    )

    loan_grade = st.selectbox(
        "Loan Grade",
        ["A", "B", "C", "D", "E", "F", "G"]
    )

    loan_amnt = st.number_input(
        "Loan Amount",
        min_value=0,
        value=10000,
        step=500
    )

    loan_int_rate = st.number_input(
        "Loan Interest Rate (%)",
        min_value=0.0,
        max_value=50.0,
        value=10.0,
        step=0.1
    )

with col3:
    cb_person_default_on_file = st.selectbox(
        "Previous Default on File",
        ["N", "Y"]
    )

    cb_person_cred_hist_length = st.number_input(
        "Credit History Length (Years)",
        min_value=0,
        max_value=50,
        value=5
    )

    if person_income > 0:
        loan_percent_income = loan_amnt / person_income
    else:
        loan_percent_income = 0

    st.metric(
        "Loan Percent Income",
        f"{loan_percent_income:.2%}"
    )

st.divider()

# =========================
# Prediction DataFrame
# =========================
input_data = pd.DataFrame({
    "person_age": [person_age],
    "person_income": [person_income],
    "person_home_ownership": [person_home_ownership],
    "person_emp_length": [person_emp_length],
    "loan_intent": [loan_intent],
    "loan_grade": [loan_grade],
    "loan_amnt": [loan_amnt],
    "loan_int_rate": [loan_int_rate],
    "loan_percent_income": [loan_percent_income],
    "cb_person_default_on_file": [cb_person_default_on_file],
    "cb_person_cred_hist_length": [cb_person_cred_hist_length]
})

# =========================
# Prediction
# =========================
if st.button("Predict Credit Risk"):
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    if probability < 0.30:
        risk_segment = "Low Risk"
        risk_color = "green"
        recommendation = "Applicant is relatively safe. Loan approval can be considered with standard review."
    elif probability < 0.60:
        risk_segment = "Medium Risk"
        risk_color = "orange"
        recommendation = "Applicant requires additional review before loan approval."
    else:
        risk_segment = "High Risk"
        risk_color = "red"
        recommendation = "Applicant has high default risk. Stricter review or rejection should be considered."

    st.subheader("Prediction Result")

    col_result1, col_result2, col_result3 = st.columns(3)

    with col_result1:
        st.metric(
            "Predicted Status",
            "Default" if prediction == 1 else "Non Default"
        )

    with col_result2:
        st.metric(
            "Default Probability",
            f"{probability:.2%}"
        )

    with col_result3:
        st.markdown(
            f"<h3 style='color:{risk_color};'>{risk_segment}</h3>",
            unsafe_allow_html=True
        )

    st.info(recommendation)

    st.subheader("Input Summary")
    st.dataframe(input_data)