import streamlit as st
import pandas as pd
from datetime import date
from database import SessionLocal
from models import Client, Package, Contract, Payment, Expense, create_tables
from services import get_all_contracts
from auth import login_required, show_logout

st.set_page_config(page_title="Contracts", layout="wide")
login_required()
show_logout()

create_tables()
session = SessionLocal()

st.title("Contracts")

tab1, tab2 = st.tabs(["Add Contract", "Edit Contract"])

clients = session.query(Client).all()
packages = session.query(Package).all()

# ================= Add =================
with tab1:
    if not clients or not packages:
        st.warning("Please add clients and packages first.")
    else:
        with st.form("add_contract_form"):
            client_map = {f"{c.id} - {c.name} - {c.company_name or ''}": c.id for c in clients}
            package_map = {f"{p.id} - {p.package_name}": p.id for p in packages}

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
                    st.rerun()

# ================= Edit =================
with tab2:
    contracts = get_all_contracts(session)

    if contracts:
        contract_map = {
            f"{c.id} - {c.client.name} - {c.package.package_name}": c.id
            for c in contracts
        }

        selected_contract_label = st.selectbox("Select Contract to Edit", list(contract_map.keys()))
        selected_contract_id = contract_map[selected_contract_label]

        contract_obj = session.query(Contract).filter(Contract.id == selected_contract_id).first()

        client_map = {f"{c.id} - {c.name} - {c.company_name or ''}": c.id for c in clients}
        package_map = {f"{p.id} - {p.package_name}": p.id for p in packages}

        client_labels = list(client_map.keys())
        package_labels = list(package_map.keys())

        current_client_label = next((label for label, cid in client_map.items() if cid == contract_obj.client_id), client_labels[0])
        current_package_label = next((label for label, pid in package_map.items() if pid == contract_obj.package_id), package_labels[0])

        with st.form("edit_contract_form"):
            edit_client_label = st.selectbox(
                "Client",
                client_labels,
                index=client_labels.index(current_client_label)
            )

            edit_package_label = st.selectbox(
                "Package",
                package_labels,
                index=package_labels.index(current_package_label)
            )

            edit_start_date = st.date_input("Start Date", value=contract_obj.start_date)
            edit_end_date = st.date_input("End Date", value=contract_obj.end_date)
            edit_agreed_price = st.number_input(
                "Agreed Price",
                min_value=0.0,
                step=100.0,
                value=float(contract_obj.agreed_price or 0)
            )

            status_options = ["Active", "Completed", "Cancelled"]
            current_status_index = status_options.index(contract_obj.status) if contract_obj.status in status_options else 0
            edit_status = st.selectbox("Status", status_options, index=current_status_index)

            col1, col2 = st.columns(2)
            update_submitted = col1.form_submit_button("Update Contract")
            delete_submitted = col2.form_submit_button("Delete Contract")

            if update_submitted:
                if edit_end_date < edit_start_date:
                    st.error("End Date cannot be earlier than Start Date.")
                elif edit_agreed_price <= 0:
                    st.error("Agreed Price must be greater than 0.")
                else:
                    contract_obj.client_id = client_map[edit_client_label]
                    contract_obj.package_id = package_map[edit_package_label]
                    contract_obj.start_date = edit_start_date
                    contract_obj.end_date = edit_end_date
                    contract_obj.agreed_price = edit_agreed_price
                    contract_obj.status = edit_status
                    session.commit()
                    st.success("Contract updated successfully")
                    st.rerun()

            if delete_submitted:
                payment_count = session.query(Payment).filter(Payment.contract_id == contract_obj.id).count()
                expense_count = session.query(Expense).filter(Expense.contract_id == contract_obj.id).count()

                if payment_count > 0 or expense_count > 0:
                    st.error("Cannot delete this contract because it has related payments or expenses.")
                else:
                    session.delete(contract_obj)
                    session.commit()
                    st.success("Contract deleted successfully")
                    st.rerun()
    else:
        st.info("No contracts to edit")

st.subheader("Contracts List")
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
    st.dataframe(df, width="stretch")
else:
    st.info("No contracts yet")