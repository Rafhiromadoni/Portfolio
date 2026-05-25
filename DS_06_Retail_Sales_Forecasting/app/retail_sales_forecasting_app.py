from pathlib import Path
import streamlit as st
import pandas as pd
import joblib

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Retail Sales Forecasting App",
    page_icon="📈",
    layout="wide"
)

# =========================
# PATH
# =========================
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "model" / "retail_sales_forecasting_model.pkl"

# =========================
# LOAD MODEL
# =========================
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

# =========================
# STYLE
# =========================
st.markdown("""
<style>
    .block-container {
        max-width: 1180px;
        padding-top: 1.2rem;
        padding-bottom: 1rem;
    }

    .hero {
        background: linear-gradient(135deg, #EFA17D, #D87555);
        color: white;
        padding: 22px 26px;
        border-radius: 18px;
        margin-bottom: 18px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    }

    .hero-title {
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .hero-subtitle {
        font-size: 15px;
        opacity: 0.95;
    }

    .card {
        background: white;
        border: 1px solid #f1f1f1;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    .metric-label {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 30px;
        font-weight: 800;
        color: #111827;
    }

    .result-low {
        background: #EAF8EE;
        color: #166534;
        padding: 14px 16px;
        border-radius: 14px;
        border-left: 6px solid #22C55E;
        font-weight: 700;
    }

    .result-medium {
        background: #FFF7E8;
        color: #92400E;
        padding: 14px 16px;
        border-radius: 14px;
        border-left: 6px solid #F59E0B;
        font-weight: 700;
    }

    .result-high {
        background: #FDECEC;
        color: #991B1B;
        padding: 14px 16px;
        border-radius: 14px;
        border-left: 6px solid #EF4444;
        font-weight: 700;
    }

    div[data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<div class="hero">
    <div class="hero-title">📈 Retail Sales Forecasting App</div>
    <div class="hero-subtitle">
        Predict weekly sales demand using store, department, holiday, economic, promotion,
        and historical sales features.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR: SIMPLE ONLY
# =========================
st.sidebar.title("Forecast Control")
st.sidebar.info(
    "Isi input pada tab utama, lalu klik tombol prediksi di bawah."
)

predict_btn = st.sidebar.button(
    "🚀 Predict Weekly Sales",
    use_container_width=True
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Model:** Random Forest")
st.sidebar.markdown("**Use case:** Inventory demand planning")
st.sidebar.markdown("**Output:** Weekly sales forecast")

# =========================
# INPUT TABS
# =========================
tab_input1, tab_input2, tab_input3, tab_result = st.tabs([
    "🏬 Store & Date",
    "🌡️ Economy & Promotion",
    "📊 Historical Sales",
    "✅ Result"
])

with tab_input1:
    st.subheader("Store and Calendar Information")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        store = st.number_input("Store", min_value=1, max_value=45, value=2, step=1)
        dept = st.number_input("Department", min_value=1, max_value=99, value=1, step=1)

    with col2:
        store_type = st.selectbox("Store Type", ["A", "B", "C"], index=0)
        size = st.number_input("Store Size", min_value=1, value=150000, step=1000)

    with col3:
        year = st.number_input("Year", min_value=2010, max_value=2030, value=2012, step=1)
        month = st.number_input("Month", min_value=1, max_value=12, value=6, step=1)

    with col4:
        week = st.number_input("Week", min_value=1, max_value=53, value=25, step=1)
        is_holiday = st.selectbox("Is Holiday", [False, True], index=0)

    quarter = (month - 1) // 3 + 1

    st.caption(f"Auto-calculated Quarter: **Q{quarter}**")

with tab_input2:
    st.subheader("Economic and Promotion Features")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Economic Factors")
        temperature = st.number_input("Temperature", value=50.0, step=0.1)
        fuel_price = st.number_input("Fuel Price", value=3.0, step=0.01)
        cpi = st.number_input("CPI", value=220.0, step=0.01)
        unemployment = st.number_input("Unemployment", value=7.0, step=0.01)

    with col2:
        st.markdown("#### MarkDown Promotion")
        markdown1 = st.number_input("MarkDown1", value=0.0, step=100.0)
        markdown2 = st.number_input("MarkDown2", value=0.0, step=100.0)
        markdown3 = st.number_input("MarkDown3", value=0.0, step=100.0)
        markdown4 = st.number_input("MarkDown4", value=0.0, step=100.0)
        markdown5 = st.number_input("MarkDown5", value=0.0, step=100.0)

with tab_input3:
    st.subheader("Historical Sales Features")

    col1, col2 = st.columns(2)

    with col1:
        sales_lag_1 = st.number_input("Sales Lag 1 Week", value=16000.0, step=100.0)
        sales_lag_2 = st.number_input("Sales Lag 2 Weeks", value=16500.0, step=100.0)
        sales_lag_4 = st.number_input("Sales Lag 4 Weeks", value=15500.0, step=100.0)

    with col2:
        rolling_mean_4 = st.number_input("Rolling Mean 4 Weeks", value=16000.0, step=100.0)
        rolling_mean_8 = st.number_input("Rolling Mean 8 Weeks", value=15800.0, step=100.0)

    st.info(
        "Historical features help the model learn recent demand patterns. "
        "Use previous weekly sales values for more realistic prediction."
    )

# =========================
# INPUT DATA
# =========================
input_data = pd.DataFrame([{
    "Store": store,
    "Dept": dept,
    "IsHoliday": is_holiday,
    "Temperature": temperature,
    "Fuel_Price": fuel_price,
    "MarkDown1": markdown1,
    "MarkDown2": markdown2,
    "MarkDown3": markdown3,
    "MarkDown4": markdown4,
    "MarkDown5": markdown5,
    "CPI": cpi,
    "Unemployment": unemployment,
    "Type": store_type,
    "Size": size,
    "year": year,
    "month": month,
    "week": week,
    "quarter": quarter,
    "sales_lag_1": sales_lag_1,
    "sales_lag_2": sales_lag_2,
    "sales_lag_4": sales_lag_4,
    "rolling_mean_4": rolling_mean_4,
    "rolling_mean_8": rolling_mean_8
}])

# =========================
# RESULT TAB
# =========================
with tab_result:
    st.subheader("Forecast Result")

    if predict_btn:
        prediction = model.predict(input_data)[0]

        if prediction >= 30000:
            demand_level = "High Demand"
            status_class = "result-high"
            recommendation = "High demand forecast. Prepare higher inventory level and stronger replenishment planning."
        elif prediction >= 15000:
            demand_level = "Moderate Demand"
            status_class = "result-medium"
            recommendation = "Moderate demand forecast. Maintain normal inventory level and monitor weekly sales movement."
        else:
            demand_level = "Low Demand"
            status_class = "result-low"
            recommendation = "Low demand forecast. Avoid overstock and maintain efficient inventory control."

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="metric-label">Predicted Weekly Sales</div>
                <div class="metric-value">${prediction:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="card">
                <div class="metric-label">Demand Level</div>
                <div class="metric-value">{demand_level}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="card">
                <div class="metric-label">Holiday Status</div>
                <div class="metric-value">{"Holiday" if is_holiday else "Non-Holiday"}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"<div class='{status_class}'>{recommendation}</div>", unsafe_allow_html=True)

        if is_holiday:
            st.warning("Holiday week detected. Consider additional inventory buffer.")
        else:
            st.success("Non-holiday week. Standard inventory planning can be applied.")

        st.markdown("### Sales Comparison")

        comparison_df = pd.DataFrame({
            "Feature": [
                "Sales Lag 1",
                "Sales Lag 2",
                "Sales Lag 4",
                "Rolling Mean 4",
                "Rolling Mean 8",
                "Predicted Sales"
            ],
            "Value": [
                sales_lag_1,
                sales_lag_2,
                sales_lag_4,
                rolling_mean_4,
                rolling_mean_8,
                prediction
            ]
        })

        st.bar_chart(comparison_df.set_index("Feature"))

        with st.expander("View Input Summary"):
            st.dataframe(input_data, use_container_width=True)

    else:
        st.info("Klik tombol **Predict Weekly Sales** di sidebar untuk melihat hasil prediksi.")
        st.markdown("### Current Input Summary")
        st.dataframe(input_data, use_container_width=True)