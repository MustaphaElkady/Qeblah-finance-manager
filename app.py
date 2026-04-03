import streamlit as st
import pandas as pd
from datetime import date
from database import SessionLocal
from models import create_tables
from services import get_dashboard_metrics, get_monthly_summary, get_package_profitability

st.set_page_config(page_title="Media Finance System", layout="wide")

create_tables()
session = SessionLocal()

st.title("Media Company Finance Dashboard")

# ===== Dashboard Metrics =====
metrics = get_dashboard_metrics(session)

row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
row1_col1.metric("Clients", metrics["total_clients"])
row1_col2.metric("All Contracts", metrics["total_contracts"])
row1_col3.metric("Active Contracts", metrics["active_contracts"])
row1_col4.metric("Total Agreed", f'{metrics["total_agreed"]:.2f}')

row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
row2_col1.metric("Total Payments", f'{metrics["total_payments"]:.2f}')
row2_col2.metric("Total Remaining", f'{metrics["total_remaining"]:.2f}')
row2_col3.metric("Total Expenses", f'{metrics["total_expenses"]:.2f}')
row2_col4.metric("Total Profit", f'{metrics["total_profit"]:.2f}')

st.divider()

# ===== Monthly Filter =====
st.subheader("Monthly Summary")

today = date.today()

filter_col1, filter_col2 = st.columns(2)
selected_year = filter_col1.number_input("Year", min_value=2020, max_value=2100, value=today.year, step=1)
selected_month = filter_col2.selectbox(
    "Month",
    options=list(range(1, 13)),
    index=today.month - 1
)

summary = get_monthly_summary(session, selected_year, selected_month)

m1, m2, m3 = st.columns(3)
m1.metric("Monthly Income", f'{summary["month_income"]:.2f}')
m2.metric("Monthly Expenses", f'{summary["month_expenses"]:.2f}')
m3.metric("Monthly Profit", f'{summary["month_profit"]:.2f}')

st.divider()

# ===== Quick Contracts Summary =====
st.subheader("Contracts Quick Summary")

data = get_package_profitability(session)

if data:
    df = pd.DataFrame(data)

    quick_view = df[[
        "contract_id",
        "client_name",
        "package_name",
        "agreed_price",
        "total_paid",
        "remaining",
        "total_expenses",
        "profit",
        "status"
    ]]

    quick_view = quick_view.rename(columns={
        "contract_id": "Contract ID",
        "client_name": "Client",
        "package_name": "Package",
        "agreed_price": "Agreed Price",
        "total_paid": "Total Paid",
        "remaining": "Remaining",
        "total_expenses": "Expenses",
        "profit": "Profit",
        "status": "Status"
    })

    st.dataframe(quick_view, use_container_width=True)
else:
    st.info("No dashboard data yet")