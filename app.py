import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="NaijaBank Analytics", page_icon="🏦", layout="wide")

st.markdown("""
<style>
    .header-title { font-size: 2.8rem; font-weight: 900; color: #00d4aa; text-align: center; }
    .sub-title { text-align: center; color: #aaa; font-size: 1.1rem; margin-bottom: 2rem; }
    .metric-card { background: #1e2130; border-radius: 12px; padding: 20px; text-align: center; margin: 5px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATABASE CONNECTION
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    conn = sqlite3.connect("naijabank.db")
    customers = pd.read_sql("SELECT * FROM customers", conn)
    transactions = pd.read_sql("SELECT * FROM transactions", conn)
    summary = pd.read_sql("SELECT * FROM customer_summary", conn)
    conn.close()
    return customers, transactions, summary


customers, transactions, summary = load_data()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown('<p class="header-title">🏦 NaijaBank Analytics</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">SQL-Powered Nigerian Banking Intelligence Dashboard</p>', unsafe_allow_html=True)
st.markdown("---")

# ─────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────
st.sidebar.markdown("## 🏦 NaijaBank Analytics")
st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")
selected_bank = st.sidebar.multiselect("Bank", customers["bank"].unique().tolist(), default=customers["bank"].unique().tolist())
selected_state = st.sidebar.multiselect("State", customers["state"].unique().tolist(), default=customers["state"].unique().tolist())
selected_gender = st.sidebar.multiselect("Gender", ["Male", "Female"], default=["Male", "Female"])
st.sidebar.markdown("---")
st.sidebar.markdown("**Built by:** Okparaji Wisdom 🇳🇬")

# Apply filters
filtered_customers = customers[
    (customers["bank"].isin(selected_bank)) &
    (customers["state"].isin(selected_state)) &
    (customers["gender"].isin(selected_gender))
]
filtered_ids = filtered_customers["customer_id"].tolist()
filtered_txns = transactions[transactions["customer_id"].isin(filtered_ids)]

# ─────────────────────────────────────────────
# KPI METRICS
# ─────────────────────────────────────────────
st.markdown("### 📊 Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Customers", f"{len(filtered_customers):,}")
col2.metric("Active Customers", f"{filtered_customers['is_active'].sum():,}")
col3.metric("Total Transactions", f"{len(filtered_txns):,}")
col4.metric("Total Volume", f"₦{filtered_txns['amount'].sum():,.0f}")
col5.metric("Fraud Cases", f"{filtered_txns['is_fraud'].sum():,}")

st.markdown("---")

# ─────────────────────────────────────────────
# ROW 1: CUSTOMERS BY STATE & BANK
# ─────────────────────────────────────────────
st.markdown("### 👥 Customer Distribution")
col1, col2 = st.columns(2)

with col1:
    state_counts = filtered_customers.groupby("state").size().reset_index(name="customers")
    fig = px.bar(state_counts.sort_values("customers", ascending=True),
                 x="customers", y="state", orientation="h",
                 title="Customers by State", color="customers",
                 color_continuous_scale=["#636e72", "#00d4aa"])
    fig.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
                      font_color="white", height=350, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    bank_counts = filtered_customers.groupby("bank").size().reset_index(name="customers")
    fig = px.pie(bank_counts, values="customers", names="bank",
                 title="Market Share by Bank",
                 color_discrete_sequence=px.colors.sequential.Teal)
    fig.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
                      font_color="white", height=350)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────
# ROW 2: TRANSACTION ANALYSIS
# ─────────────────────────────────────────────
st.markdown("### 💰 Transaction Analysis")
col1, col2 = st.columns(2)

with col1:
    txn_type_vol = filtered_txns.groupby("transaction_type")["amount"].sum().reset_index()
    txn_type_vol.columns = ["Type", "Volume"]
    fig = px.bar(txn_type_vol.sort_values("Volume", ascending=True),
                 x="Volume", y="Type", orientation="h",
                 title="Transaction Volume by Type", color="Volume",
                 color_continuous_scale=["#636e72", "#00d4aa"])
    fig.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
                      font_color="white", height=350, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    monthly = filtered_txns.groupby("month_num").agg(
        total_volume=("amount", "sum"),
        total_count=("transaction_id", "count")
    ).reset_index()
    monthly = monthly.sort_values("month_num")
    fig = px.line(monthly, x="month_num", y="total_volume",
                  title="Monthly Transaction Volume (2024)",
                  markers=True, line_shape="spline")
    fig.update_traces(line_color="#00d4aa", fill="tozeroy", fillcolor="rgba(0,212,170,0.1)")
    fig.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
                      font_color="white", height=350,
                      xaxis_title="Month", yaxis_title="Volume (₦)")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────
# ROW 3: DEMOGRAPHICS & ACCOUNT TYPES
# ─────────────────────────────────────────────
st.markdown("### 🧑‍🤝‍🧑 Customer Demographics")
col1, col2, col3 = st.columns(3)

with col1:
    gender_counts = filtered_customers.groupby("gender").size().reset_index(name="count")
    fig = px.pie(gender_counts, values="count", names="gender",
                 title="Gender Distribution",
                 color_discrete_map={"Male": "#00d4aa", "Female": "#6c5ce7"})
    fig.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
                      font_color="white", height=300)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    age_bins = pd.cut(filtered_customers["age"],
                      bins=[18, 25, 35, 45, 55, 65],
                      labels=["18-25", "26-35", "36-45", "46-55", "56-65"])
    age_counts = age_bins.value_counts().reset_index()
    age_counts.columns = ["Age Group", "Count"]
    fig = px.bar(age_counts, x="Age Group", y="Count",
                 title="Age Distribution", color="Count",
                 color_continuous_scale=["#636e72", "#00d4aa"])
    fig.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
                      font_color="white", height=300, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col3:
    acct_counts = filtered_customers.groupby("account_type").size().reset_index(name="count")
    fig = px.pie(acct_counts, values="count", names="account_type",
                 title="Account Types",
                 color_discrete_sequence=["#00d4aa", "#6c5ce7", "#e17055"])
    fig.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
                      font_color="white", height=300)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────
# ROW 4: FRAUD ANALYSIS
# ─────────────────────────────────────────────
st.markdown("### 🚨 Fraud Analysis")
col1, col2 = st.columns(2)

with col1:
    fraud_by_type = filtered_txns.groupby("transaction_type")["is_fraud"].sum().reset_index()
    fraud_by_type.columns = ["Type", "Fraud Count"]
    fig = px.bar(fraud_by_type.sort_values("Fraud Count", ascending=False),
                 x="Type", y="Fraud Count",
                 title="Fraud Cases by Transaction Type",
                 color="Fraud Count",
                 color_continuous_scale=["#fdcb6e", "#d63031"])
    fig.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
                      font_color="white", height=300, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fraud_by_state = filtered_txns.merge(
        filtered_customers[["customer_id", "state"]], on="customer_id"
    ).groupby("state")["is_fraud"].sum().reset_index()
    fraud_by_state.columns = ["State", "Fraud Count"]
    fig = px.bar(fraud_by_state.sort_values("Fraud Count", ascending=False),
                 x="State", y="Fraud Count",
                 title="Fraud Cases by State",
                 color="Fraud Count",
                 color_continuous_scale=["#fdcb6e", "#d63031"])
    fig.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
                      font_color="white", height=300, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────
# ROW 5: TOP CUSTOMERS TABLE
# ─────────────────────────────────────────────
st.markdown("### 🏆 Top 10 Customers by Transaction Volume")
top_customers = summary.nlargest(10, "total_volume")[
    ["full_name", "bank", "account_type", "total_transactions", "total_volume", "fraud_count"]]
top_customers["total_volume"] = top_customers["total_volume"].apply(lambda x: f"₦{x:,.0f}")
st.dataframe(top_customers, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────
# RAW DATA EXPLORER
# ─────────────────────────────────────────────
with st.expander("🔍 Explore Raw Transaction Data"):
    st.dataframe(filtered_txns.head(100), use_container_width=True)
    csv = filtered_txns.to_csv(index=False)
    st.download_button("📥 Download Transactions CSV", csv,
                       file_name="naijabank_transactions.csv", mime="text/csv")

st.markdown("---")
st.markdown("<p style='text-align:center; color:#aaa'>NaijaBank Analytics | Built by Okparaji Wisdom 🇳🇬 | SQL Analytics Portfolio Project</p>", unsafe_allow_html=True)