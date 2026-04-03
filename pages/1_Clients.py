import pandas as pd
import streamlit as st
from auth import login_required, show_logout
from database import SessionLocal
from models import Client, Contract, create_tables
from services import get_all_clients

st.set_page_config(page_title="Clients", layout="wide")
login_required()
show_logout()

create_tables()
session = SessionLocal()

st.title("Clients")

tab1, tab2 = st.tabs(["Add Client", "Edit Client"])

with tab1:
    with st.form("add_client_form"):
        name = st.text_input("Client Name")
        phone = st.text_input("Phone")
        company_name = st.text_input("Company Name")
        email = st.text_input("Email")
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add Client")

        if submitted:
            if not name.strip():
                st.error("Client name is required")
            elif not phone.strip():
                st.error("Phone is required")
            else:
                existing_client = session.query(Client).filter(Client.name == name.strip()).first()
                if existing_client:
                    st.error("A client with this name already exists.")
                else:
                    client = Client(
                        name=name.strip(),
                        phone=phone.strip(),
                        company_name=company_name.strip(),
                        email=email.strip(),
                        notes=notes,
                    )
                    session.add(client)
                    session.commit()
                    st.success("Client added successfully")
                    st.rerun()

with tab2:
    clients = get_all_clients(session)
    if clients:
        client_map = {f"{c.id} - {c.name}": c.id for c in clients}
        selected_client_label = st.selectbox("Select Client to Edit", list(client_map.keys()))
        selected_client_id = client_map[selected_client_label]
        client_obj = session.query(Client).filter(Client.id == selected_client_id).first()

        with st.form("edit_client_form"):
            edit_name = st.text_input("Client Name", value=client_obj.name or "")
            edit_phone = st.text_input("Phone", value=client_obj.phone or "")
            edit_company_name = st.text_input("Company Name", value=client_obj.company_name or "")
            edit_email = st.text_input("Email", value=client_obj.email or "")
            edit_notes = st.text_area("Notes", value=client_obj.notes or "")

            col1, col2 = st.columns(2)
            update_submitted = col1.form_submit_button("Update Client")
            delete_submitted = col2.form_submit_button("Delete Client")

            if update_submitted:
                if not edit_name.strip():
                    st.error("Client name is required")
                elif not edit_phone.strip():
                    st.error("Phone is required")
                else:
                    client_obj.name = edit_name.strip()
                    client_obj.phone = edit_phone.strip()
                    client_obj.company_name = edit_company_name.strip()
                    client_obj.email = edit_email.strip()
                    client_obj.notes = edit_notes
                    session.commit()
                    st.success("Client updated successfully")
                    st.rerun()

            if delete_submitted:
                related_contracts = session.query(Contract).filter(Contract.client_id == client_obj.id).count()
                if related_contracts > 0:
                    st.error("Cannot delete this client because there are contracts linked to it.")
                else:
                    session.delete(client_obj)
                    session.commit()
                    st.success("Client deleted successfully")
                    st.rerun()
    else:
        st.info("No clients to edit")

st.subheader("Clients List")
clients = get_all_clients(session)
if clients:
    df = pd.DataFrame([
        {
            "ID": c.id,
            "Name": c.name,
            "Phone": c.phone,
            "Company": c.company_name,
            "Email": c.email,
            "Notes": c.notes,
        }
        for c in clients
    ])
    st.dataframe(df, width="stretch")
else:
    st.info("No clients yet")
