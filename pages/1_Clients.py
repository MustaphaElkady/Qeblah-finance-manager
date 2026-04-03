import streamlit as st
import pandas as pd
from database import SessionLocal
from models import Client, create_tables
from services import get_all_clients
st.set_page_config(page_title="Clients", layout="wide")
create_tables()
session = SessionLocal()
st.title("Clients")
with st.form("add_client_form"):
     name = st.text_input("Client Name")
     phone = st.text_input("Phone")
     company_name = st.text_input("Company Name")
     email = st.text_input("Email")
     notes = st.text_area("Notes")
     submitted = st.form_submit_button("Add Client")
     if submitted:
          if name.strip():
            client = Client(
                name=name,
                phone=phone,
                company_name=company_name,
                email=email,
                notes=notes
            )
            session.add(client)
            session.commit()
            st.success("Client added successfully")
          else:
              st.error("client name is required")
clients = get_all_clients(session)
if clients:
    df = pd.DataFrame([
        {
            "ID": c.id,
            "Name": c.name,
            "Phone": c.phone,
            "Email": c.email,
            "Company": c.company_name,
            "Notes": c.notes
        }
        for c in clients
    ])
    st.dataframe(df, use_container_width=True)
else:
    st.info("No clients yet")
