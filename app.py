from datetime import date
import streamlit as st
import pandas as pd
import re

from model import load_model, train_and_save_model
import database


EMAIL_PATTERN = r'^[\w\.-]+@[\w\.-]+\.\w+$'


def validate_email(email: str) -> bool:
    return re.match(EMAIL_PATTERN, email) is not None


def validate_dob(dob: date) -> bool:
    return dob <= date.today()


def main():
    st.set_page_config(page_title="Health Prediction App", layout="wide")
    st.sidebar.title("Health Prediction App")

    # Init DB and model
    database.init_db()
    model, le = load_model()

    st.title("Health Prediction & Patient Management")

    with st.sidebar.expander("Add / Update Patient"):
        mode = st.radio("Action", ["Add New", "Update Existing"])
        if mode == "Add New":
            with st.form("add_form"):
                name = st.text_input("Full name")
                dob = st.date_input("Date of birth")
                email = st.text_input("Email")
                glucose = st.text_input("Glucose")
                haemoglobin = st.text_input("Haemoglobin")
                cholesterol = st.text_input("Cholesterol")
                submitted = st.form_submit_button("Add Patient")
                if submitted:
                    if not name:
                        st.error("Name is required")
                    elif not validate_email(email):
                        st.error("Invalid email")
                    elif not validate_dob(dob):
                        st.error("DOB cannot be in the future")
                    else:
                        try:
                            g = float(glucose)
                            h = float(haemoglobin)
                            c = float(cholesterol)
                        except ValueError:
                            st.error("Glucose, Haemoglobin, and Cholesterol must be numbers")
                        else:
                            pred = model.predict([[g, h, c]])
                            remark = le.inverse_transform(pred)[0]
                            pid = database.add_patient(name, dob.isoformat(), email, g, h, c, remark)
                            st.success(f"Patient added (id={pid}). Prediction: {remark}")

        else:
            patients = database.get_all_patients()
            ids = [r["id"] for r in patients]
            selected = st.selectbox("Select patient id to edit", options=ids if ids else [None])
            if selected:
                row = database.get_patient(selected)
                with st.form("update_form"):
                    name = st.text_input("Full name", value=row["full_name"])
                    dob = st.date_input("Date of birth", value=pd.to_datetime(row["dob"]).date())
                    email = st.text_input("Email", value=row["email"])
                    glucose = st.text_input("Glucose", value=str(row["glucose"]))
                    haemoglobin = st.text_input("Haemoglobin", value=str(row["haemoglobin"]))
                    cholesterol = st.text_input("Cholesterol", value=str(row["cholesterol"]))
                    update_btn = st.form_submit_button("Update Patient")
                    delete_btn = st.form_submit_button("Delete Patient")
                    if update_btn:
                        if not name:
                            st.error("Name is required")
                        elif not validate_email(email):
                            st.error("Invalid email")
                        elif not validate_dob(dob):
                            st.error("DOB cannot be in the future")
                        else:
                            try:
                                g = float(glucose)
                                h = float(haemoglobin)
                                c = float(cholesterol)
                            except ValueError:
                                st.error("Glucose, Haemoglobin, and Cholesterol must be numbers")
                            else:
                                pred = model.predict([[g, h, c]])
                                remark = le.inverse_transform(pred)[0]
                                database.update_patient(selected, name, dob.isoformat(), email, g, h, c, remark)
                                st.success(f"Patient updated. Prediction: {remark}")
                    if delete_btn:
                        database.delete_patient(selected)
                        st.success("Patient deleted")

    # Main area: dashboard and table
    st.header("Dashboard")
    rows = database.get_all_patients()
    rows_list = [dict(r) for r in rows] if rows else []
    df = pd.DataFrame(rows_list)

    total = len(df)
    healthy = int((df["remarks"] == "Healthy").sum()) if "remarks" in df else 0
    predi = int((df["remarks"] == "Prediabetes Risk").sum()) if "remarks" in df else 0
    high = int((df["remarks"] == "High Cholesterol Risk").sum()) if "remarks" in df else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Patients", total)
    c2.metric("Healthy", healthy)
    c3.metric("Prediabetes Risk", predi)
    c4.metric("High Cholesterol Risk", high)

    st.header("Patients")
    if not df.empty:
        # add colored emojis for quick visual
        def decorate(r):
            if r == "Healthy":
                return "🟢 " + r
            if r == "Prediabetes Risk":
                return "🟠 " + r
            if r == "High Cholesterol Risk":
                return "🔴 " + r
            return r

        df_display = df.copy()
        if "remarks" in df_display:
            df_display["remarks"] = df_display["remarks"].apply(decorate)
        st.dataframe(df_display)
    else:
        st.info("No patient records yet. Add patients using the sidebar form.")


if __name__ == "__main__":
    main()
