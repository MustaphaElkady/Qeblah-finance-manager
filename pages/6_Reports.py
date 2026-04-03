import streamlit as st
import pandas as pd
from database import SessionLocal
from models import create_tables
from services import get_package_profitability

st.set_page_config(page_title="Reports", layout="wide")
create_tables()
session = SessionLocal()

st.title("Reports")

data = get_package_profitability(session)

if data:
    df = pd.DataFrame(data)

    st.subheader("Package / Contract Profitability")
    st.dataframe(df, use_container_width=True)

    st.subheader("Summary")
    st.write("Total Paid:", df["total_paid"].sum())
    st.write("Total Expenses:", df["total_expenses"].sum())
    st.write("Total Profit:", df["profit"].sum())
else:
    st.info("No report data yet")