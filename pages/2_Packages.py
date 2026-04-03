import streamlit as st
import pandas as pd
from database import SessionLocal
from models import Package, create_tables
from services import get_all_packages
from auth import login_required, show_logout

st.set_page_config(page_title="Packages", layout="wide")
login_required()
show_logout()

create_tables()
session = SessionLocal()

st.title("Packages")

tab1, tab2 = st.tabs(["Add Package", "Edit Package"])

with tab1:
    with st.form("add_package_form"):
        package_name = st.text_input("Package Name")
        package_type = st.selectbox("Package Type", ["Reels", "Posts", "Mixed"])
        default_price = st.number_input("Default Price", min_value=0.0, step=100.0)
        description = st.text_area("Description")
        submitted = st.form_submit_button("Add Package")

        if submitted:
            if not package_name.strip():
                st.error("Package name is required")
            else:
                existing_package = session.query(Package).filter(Package.package_name == package_name.strip()).first()

                if existing_package:
                    st.error("This package already exists.")
                else:
                    package = Package(
                        package_name=package_name.strip(),
                        package_type=package_type,
                        default_price=default_price,
                        description=description
                    )
                    session.add(package)
                    session.commit()
                    st.success("Package added successfully")

with tab2:
    packages = get_all_packages(session)

    if packages:
        package_map = {f"{p.id} - {p.package_name}": p.id for p in packages}
        selected_package_label = st.selectbox("Select Package to Edit", list(package_map.keys()))
        selected_package_id = package_map[selected_package_label]

        package_obj = session.query(Package).filter(Package.id == selected_package_id).first()

        with st.form("edit_package_form"):
            edit_package_name = st.text_input("Package Name", value=package_obj.package_name or "")
            edit_package_type = st.selectbox(
                "Package Type",
                ["Reels", "Posts", "Mixed"],
                index=["Reels", "Posts", "Mixed"].index(package_obj.package_type) if package_obj.package_type in ["Reels", "Posts", "Mixed"] else 0
            )
            edit_default_price = st.number_input("Default Price", min_value=0.0, step=100.0, value=float(package_obj.default_price or 0))
            edit_description = st.text_area("Description", value=package_obj.description or "")

            col1, col2 = st.columns(2)
            update_submitted = col1.form_submit_button("Update Package")
            delete_submitted = col2.form_submit_button("Delete Package")

            if update_submitted:
                if not edit_package_name.strip():
                    st.error("Package name is required")
                else:
                    package_obj.package_name = edit_package_name.strip()
                    package_obj.package_type = edit_package_type
                    package_obj.default_price = edit_default_price
                    package_obj.description = edit_description
                    session.commit()
                    st.success("Package updated successfully")
                    st.rerun()

            if delete_submitted:
                session.delete(package_obj)
                session.commit()
                st.success("Package deleted successfully")
                st.rerun()
    else:
        st.info("No packages to edit")

st.subheader("Packages List")
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
    st.dataframe(df, width="stretch")
else:
    st.info("No packages yet")