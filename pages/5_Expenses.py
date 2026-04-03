import streamlit as st
import pandas as pd
from datetime import date
from database import SessionLocal
from models import Expense, create_tables
from services import get_all_contracts

st.set_page_config(page_title="Expenses", layout="wide")
create_tables()
session = SessionLocal()

st.title("Expenses")

contracts = get_all_contracts(session)

if not contracts:
    st.warning("Please add contracts first.")
else:
    with st.form("add_expense_form"):
        contract_map = {
            f"#{c.id} | {c.client.name} | {c.package.package_name}": c.id
            for c in contracts
        }

        contract_lookup = {c.id: c for c in contracts}

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

    all_expenses = session.query(Expense).all()

    if all_expenses:
        rows = []
        for e in all_expenses:
            contract = contract_lookup.get(e.contract_id)
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
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No expenses yet")