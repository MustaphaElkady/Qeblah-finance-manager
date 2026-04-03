import streamlit as st
import pandas as pd
from datetime import date
from database import SessionLocal
from models import Expense, create_tables
from services import get_all_contracts
from auth import login_required, show_logout

st.set_page_config(page_title="Expenses", layout="wide")
login_required()
show_logout()

create_tables()
session = SessionLocal()

st.title("Expenses")

tab1, tab2 = st.tabs(["Add Expense", "Edit Expense"])

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
        with st.form("add_expense_form"):
            contract_label = st.selectbox("Contract", list(contract_map.keys()))
            expense_date = st.date_input("Expense Date", value=date.today())
            category = st.selectbox("Category", ["Photography", "Ads", "Design"])
            amount = st.number_input("Amount", min_value=0.0, step=100.0)
            notes = st.text_area("Notes")

            submitted = st.form_submit_button("Add Expense")

            if submitted:
                if amount <= 0:
                    st.error("Amount must be greater than 0.")
                else:
                    expense = Expense(
                        contract_id=contract_map[contract_label],
                        expense_date=expense_date,
                        category=category,
                        amount=amount,
                        notes=notes
                    )
                    session.add(expense)
                    session.commit()
                    st.success("Expense added successfully")
                    st.rerun()

# ================= Edit =================
with tab2:
    all_expenses = session.query(Expense).all()

    if all_expenses and contracts:
        expense_map = {
            f"{e.id} - Contract {e.contract_id} - {contract_lookup[e.contract_id].client.name if e.contract_id in contract_lookup else ''}": e.id
            for e in all_expenses
        }

        selected_expense_label = st.selectbox("Select Expense to Edit", list(expense_map.keys()))
        selected_expense_id = expense_map[selected_expense_label]

        expense_obj = session.query(Expense).filter(Expense.id == selected_expense_id).first()

        contract_labels = list(contract_map.keys())
        current_contract_label = next((label for label, cid in contract_map.items() if cid == expense_obj.contract_id), contract_labels[0])

        category_options = ["Photography", "Ads", "Design"]
        current_category_index = category_options.index(expense_obj.category) if expense_obj.category in category_options else 0

        with st.form("edit_expense_form"):
            edit_contract_label = st.selectbox(
                "Contract",
                contract_labels,
                index=contract_labels.index(current_contract_label)
            )
            edit_expense_date = st.date_input("Expense Date", value=expense_obj.expense_date)
            edit_category = st.selectbox("Category", category_options, index=current_category_index)
            edit_amount = st.number_input(
                "Amount",
                min_value=0.0,
                step=100.0,
                value=float(expense_obj.amount or 0)
            )
            edit_notes = st.text_area("Notes", value=expense_obj.notes or "")

            col1, col2 = st.columns(2)
            update_submitted = col1.form_submit_button("Update Expense")
            delete_submitted = col2.form_submit_button("Delete Expense")

            if update_submitted:
                if edit_amount <= 0:
                    st.error("Amount must be greater than 0.")
                else:
                    expense_obj.contract_id = contract_map[edit_contract_label]
                    expense_obj.expense_date = edit_expense_date
                    expense_obj.category = edit_category
                    expense_obj.amount = edit_amount
                    expense_obj.notes = edit_notes
                    session.commit()
                    st.success("Expense updated successfully")
                    st.rerun()

            if delete_submitted:
                session.delete(expense_obj)
                session.commit()
                st.success("Expense deleted successfully")
                st.rerun()
    else:
        st.info("No expenses to edit")

st.subheader("Expenses List")
all_expenses = session.query(Expense).all()

if all_expenses:
    rows = []
    refreshed_contracts = get_all_contracts(session)
    refreshed_lookup = {c.id: c for c in refreshed_contracts}

    for e in all_expenses:
        contract = refreshed_lookup.get(e.contract_id)
        rows.append({
            "ID": e.id,
            "Contract ID": e.contract_id,
            "Client": contract.client.name if contract else "",
            "Package": contract.package.package_name if contract else "",
            "Expense Date": e.expense_date,
            "Category": e.category,
            "Amount": e.amount,
            "Notes": e.notes
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, width="stretch")
else:
    st.info("No expenses yet")