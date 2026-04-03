import streamlit as st
import pandas as pd
from database import SessionLocal
from models import Package, create_tables
from services import get_all_packages

st.set_page_config(page_title="Packages", layout="wide")
create_tables()
session = SessionLocal()

st.title("Packages")

with st.form("add_package_form"):
    package_name = st.text_input("Package Name")
    package_type = st.selectbox("Package Type", ["Reels", "Posts", "Mixed"])
    default_price = st.number_input("Default Price", min_value=0.0, step=100.0)
    description = st.text_area("Description")
    submitted = st.form_submit_button("Add Package")

    if submitted:
        if package_name.strip():
            package = Package(
                package_name=package_name,
                package_type=package_type,
                default_price=default_price,
                description=description
            )
            session.add(package)
            session.commit()
            st.success("Package added successfully")
        else:
            st.error("Package name is required")

packages = get_all_packages(session)

if packages:
    df = pd.DataFrame([
        {
            "ID": p.id,
            "Package Name": p.package_name,
            "Type": p.package_type,
            "Default Price": p.default_price,
            "Description": p.description
        }
        for p in packages
    ])
    st.dataframe(df, use_container_width=True)
else:
    st.info("No packages yet")