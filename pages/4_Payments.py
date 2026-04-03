import streamlit as st
import pandas as pd
from datetime import date
from database import SessionLocal
from models import Payment, create_tables
from services import get_all_contracts

st.set_page_config(page_title="Payments", layout="wide")
create_tables()
session = SessionLocal()

st.title("Payments")

contracts = get_all_contracts(session)

if not contracts:
    st.warning("Please add contracts first.")
else:
    with st.form("add_payment_form"):
        contract_map = {
            f"#{c.id} | {c.client.name} | {c.package.package_name}": c.id
            for c in contracts
        }

        contract_lookup = {c.id: c for c in contracts}

        contract_label = st.selectbox("Contract", list(contract_map.keys()))
        payment_date = st.date_input("Payment Date", value=date.today())
        amount = st.number_input("Amount", min_value=0.0, step=100.0)
        payment_method = st.selectbox("Payment Method", ["Cash", "Bank Transfer", "Instapay", "Other"])
        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Add Payment")

        if submitted:
            if amount <= 0:
                st.error("Amount must be greater than 0.")
            else:
                payment = Payment(
                    contract_id=contract_map[contract_label],
                    payment_date=payment_date,
                    amount=amount,
                    payment_method=payment_method,
                    notes=notes
                )
                session.add(payment)
                session.commit()
                st.success("Payment added successfully")

    all_payments = session.query(Payment).all()

    if all_payments:
        rows = []
        for p in all_payments:
            contract = contract_lookup.get(p.contract_id)
            rows.append({
                "ID": p.id,
                "Contract ID": p.contract_id,
                "Client": contract.client.name if contract else "",
                "Package": contract.package.package_name if contract else "",
                "Payment Date": p.payment_date,
                "Amount": p.amount,
                "Method": p.payment_method,
                "Notes": p.notes
            })

        df = pd.DataFrame(rows)
        st.dataframe(df, width="stretch")
    else:
        st.info("No payments yet")