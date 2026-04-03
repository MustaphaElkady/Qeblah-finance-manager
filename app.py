import streamlit as st
from datetime import date
from database import SessionLocal # 001_database
from models import create_tables # 002_services
from services import get_dashboard_metrics, get_monthly_summary

st.set_page_config(page_title="Media Finance System", layout="wide")
create_tables()
session = SessionLocal()
st.title("Media Company Finance Dashboard")
metrics = get_dashboard_metrics(session)
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Clients", metrics["total_clients"])
col2.metric("Contracts", metrics["total_contracts"])
col3.metric("Total Payments", f'{metrics["total_payments"]:.2f}')
col4.metric("Total Expenses", f'{metrics["total_expenses"]:.2f}')
col5.metric("Total Profit", f'{metrics["total_profit"]:.2f}')
st.divider()
today = date.today()
summary = get_monthly_summary(session, today.year, today.month)
st.subheader("Current Month Summary")
m1, m2, m3 = st.columns(3)
m1.metric("Monthly Income", f'{summary["month_income"]:.2f}')
m2.metric("Monthly Expenses", f'{summary["month_expenses"]:.2f}')
m3.metric("Monthly Profit", f'{summary["month_profit"]:.2f}')