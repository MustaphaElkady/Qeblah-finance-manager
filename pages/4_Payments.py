import streamlit as st
import pandas as pd
from datetime import date
from database import SessionLocal
from models import Payment, create_tables
from services import get_all_contracts
from auth import login_required, show_logout

st.set_page_config(page_title="Payments", layout="wide")
login_required()
show_logout()

create_tables()
session = SessionLocal()

st.title("Payments")

tab1, tab2 = st.tabs(["Add Payment", "Edit Payment"])

contracts = get_all_contracts(session)
contract_map = {
    f"{c.id} - {c.client.name} - {c.package.package_name}": c.id
    for c in contracts
}
contract_lookup = {c.id: c for c in contracts}

# ================= Add =================
with tab1:
    if not contracts:
        st.warning("Please add contracts first.")
    else:
        with st.form("add_payment_form"):
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
                    st.rerun()

# ================= Edit =================
with tab2:
    all_payments = session.query(Payment).all()

    if all_payments and contracts:
        payment_map = {
            f"{p.id} - Contract {p.contract_id} - {contract_lookup[p.contract_id].client.name if p.contract_id in contract_lookup else ''}": p.id
            for p in all_payments
        }

        selected_payment_label = st.selectbox("Select Payment to Edit", list(payment_map.keys()))
        selected_payment_id = payment_map[selected_payment_label]

        payment_obj = session.query(Payment).filter(Payment.id == selected_payment_id).first()

        contract_labels = list(contract_map.keys())
        current_contract_label = next((label for label, cid in contract_map.items() if cid == payment_obj.contract_id), contract_labels[0])

        payment_methods = ["Cash", "Bank Transfer", "Instapay", "Other"]
        current_method_index = payment_methods.index(payment_obj.payment_method) if payment_obj.payment_method in payment_methods else 0

        with st.form("edit_payment_form"):
            edit_contract_label = st.selectbox(
                "Contract",
                contract_labels,
                index=contract_labels.index(current_contract_label)
            )
            edit_payment_date = st.date_input("Payment Date", value=payment_obj.payment_date)
            edit_amount = st.number_input(
                "Amount",
                min_value=0.0,
                step=100.0,
                value=float(payment_obj.amount or 0)
            )
            edit_payment_method = st.selectbox("Payment Method", payment_methods, index=current_method_index)
            edit_notes = st.text_area("Notes", value=payment_obj.notes or "")

            col1, col2 = st.columns(2)
            update_submitted = col1.form_submit_button("Update Payment")
            delete_submitted = col2.form_submit_button("Delete Payment")

            if update_submitted:
                if edit_amount <= 0:
                    st.error("Amount must be greater than 0.")
                else:
                    payment_obj.contract_id = contract_map[edit_contract_label]
                    payment_obj.payment_date = edit_payment_date
                    payment_obj.amount = edit_amount
                    payment_obj.payment_method = edit_payment_method
                    payment_obj.notes = edit_notes
                    session.commit()
                    st.success("Payment updated successfully")
                    st.rerun()

            if delete_submitted:
                session.delete(payment_obj)
                session.commit()
                st.success("Payment deleted successfully")
                st.rerun()
    else:
        st.info("No payments to edit")

st.subheader("Payments List")
all_payments = session.query(Payment).all()

if all_payments:
    rows = []
    refreshed_contracts = get_all_contracts(session)
    refreshed_lookup = {c.id: c for c in refreshed_contracts}

    for p in all_payments:
        contract = refreshed_lookup.get(p.contract_id)
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