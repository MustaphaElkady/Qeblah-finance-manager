import streamlit as st
import pandas as pd
from datetime import date
from database import SessionLocal
from models import Client, Package, Contract, create_tables
from services import get_all_contracts

st.set_page_config(page_title="Contracts", layout="wide")
create_tables()
session = SessionLocal()

st.title("Contracts")

clients = session.query(Client).all()
packages = session.query(Package).all()

if not clients or not packages:
    st.warning("Please add clients and packages first.")
else:
    with st.form("add_contract_form"):
        client_map = {f"{c.name} - {c.company_name or ''}": c.id for c in clients}
        package_map = {p.package_name: p.id for p in packages}

        client_label = st.selectbox("Client", list(client_map.keys()))
        package_label = st.selectbox("Package", list(package_map.keys()))
        start_date = st.date_input("Start Date", value=date.today())
        end_date = st.date_input("End Date", value=date.today())
        agreed_price = st.number_input("Agreed Price", min_value=0.0, step=100.0)
        status = st.selectbox("Status", ["Active", "Completed", "Cancelled"])

        submitted = st.form_submit_button("Add Contract")

        if submitted:
            if end_date < start_date:
                st.error("End Date cannot be earlier than Start Date.")
            elif agreed_price <= 0:
                st.error("Agreed Price must be greater than 0.")
            else:
                contract = Contract(
                    client_id=client_map[client_label],
                    package_id=package_map[package_label],
                    start_date=start_date,
                    end_date=end_date,
                    agreed_price=agreed_price,
                    status=status
                )
                session.add(contract)
                session.commit()
                st.success("Contract added successfully")

contracts = get_all_contracts(session)

if contracts:
    df = pd.DataFrame([
        {
            "Contract ID": c.id,
            "Client": c.client.name,
            "Package": c.package.package_name,
            "Start Date": c.start_date,
            "End Date": c.end_date,
            "Agreed Price": c.agreed_price,
            "Status": c.status
        }
        for c in contracts
    ])
    st.dataframe(df, use_container_width=True)
else:
    st.info("No contracts yet")