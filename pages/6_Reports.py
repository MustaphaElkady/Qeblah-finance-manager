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

    # ===== Filters =====
    st.subheader("Filters")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    client_options = ["All"] + sorted(df["client_name"].dropna().unique().tolist())
    package_options = ["All"] + sorted(df["package_name"].dropna().unique().tolist())
    status_options = ["All"] + sorted(df["status"].dropna().unique().tolist())

    selected_client = filter_col1.selectbox("Client", client_options)
    selected_package = filter_col2.selectbox("Package", package_options)
    selected_status = filter_col3.selectbox("Status", status_options)

    filtered_df = df.copy()

    if selected_client != "All":
        filtered_df = filtered_df[filtered_df["client_name"] == selected_client]

    if selected_package != "All":
        filtered_df = filtered_df[filtered_df["package_name"] == selected_package]

    if selected_status != "All":
        filtered_df = filtered_df[filtered_df["status"] == selected_status]

    st.divider()

    # ===== Report Table =====
    st.subheader("Package / Contract Profitability")

    display_df = filtered_df[[
        "contract_id",
        "client_name",
        "package_name",
        "agreed_price",
        "total_paid",
        "remaining",
        "total_expenses",
        "profit",
        "status"
    ]].rename(columns={
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

    if not display_df.empty:
        st.dataframe(display_df, use_container_width=True)

        st.subheader("Summary")
        st.write("Total Agreed Price:", filtered_df["agreed_price"].sum())
        st.write("Total Paid:", filtered_df["total_paid"].sum())
        st.write("Total Remaining:", filtered_df["remaining"].sum())
        st.write("Total Expenses:", filtered_df["total_expenses"].sum())
        st.write("Total Profit:", filtered_df["profit"].sum())
    else:
        st.info("No results found for the selected filters.")
else:
    st.info("No report data yet")