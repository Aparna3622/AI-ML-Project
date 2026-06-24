from datetime import date
import streamlit as st
import pandas as pd
import re
import io
try:
    import plotly.express as px
except Exception:
    px = None

from model import load_model, train_and_save_model
import database


EMAIL_PATTERN = r'^[\w\.-]+@[\w\.-]+\.\w+$'


def validate_email(email: str) -> bool:
    return re.match(EMAIL_PATTERN, email) is not None


def validate_dob(dob: date) -> bool:
    return dob <= date.today()


def main():
    st.set_page_config(page_title="Health Prediction App", layout="wide")
    # Custom styling for a more attractive UI
    st.markdown(
        """
    <style>
    .stApp { background: linear-gradient(180deg,#f7fbff 0%, #ffffff 100%);} 
    .big-title {font-size:42px; font-weight:700; color:#0b3d91;}
    .card {background: #ffffff; border-radius:12px; padding: 12px; box-shadow: 0 2px 6px rgba(11,61,145,0.08);}
    .sidebar .css-1d391kg {background: linear-gradient(180deg,#ffffff, #f1f7ff);} 
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.sidebar.title("Health Prediction App")
    st.sidebar.markdown("Manage patients and predict health risk from blood values.")
    # dataset controls in sidebar
    with st.sidebar.expander("Dataset"):
        st.write("Upload a CSV with columns: glucose, haemoglobin, cholesterol, risk (optional)")
        uploaded = st.file_uploader("Upload CSV", type=["csv"])
        if uploaded:
            df_up = pd.read_csv(uploaded)
            st.write(f"Loaded {len(df_up)} rows")
            if st.button("Save uploaded as sample_data.csv"):
                df_up.to_csv("data/sample_data.csv", index=False)
                st.success("Saved to data/sample_data.csv")
        if st.button("Load sample dataset"):
            try:
                df_sample = pd.read_csv("data/sample_data.csv")
                st.success(f"Sample dataset loaded ({len(df_sample)} rows)")
            except Exception:
                st.error("No sample dataset found. Run training or generate data first.")

    # Init DB and model
    database.init_db()
    model, le = load_model()

    st.title("Health Prediction & Patient Management")

    with st.sidebar.expander("Add / Update Patient"):
        mode = st.radio("Action", ["Add New", "Update Existing"])
        if mode == "Add New":
            with st.form("add_form"):
                c1, c2 = st.columns([2, 1])
                with c1:
                    name = st.text_input("Full name", placeholder="e.g. John Doe")
                    dob = st.date_input("Date of birth")
                    email = st.text_input("Email", placeholder="name@example.com")
                with c2:
                    glucose = st.number_input("Glucose", min_value=0.0, max_value=1000.0, value=100.0, step=0.1, help="mg/dL")
                    haemoglobin = st.number_input("Haemoglobin", min_value=0.0, max_value=30.0, value=13.0, step=0.1, help="g/dL")
                    cholesterol = st.number_input("Cholesterol", min_value=0.0, max_value=1000.0, value=190.0, step=0.1, help="mg/dL")
                submitted = st.form_submit_button("Add Patient ✅")
                if submitted:
                    if not name:
                        st.error("Name is required")
                    elif not validate_email(email):
                        st.error("Invalid email")
                    elif not validate_dob(dob):
                        st.error("DOB cannot be in the future")
                    else:
                        g = float(glucose)
                        h = float(haemoglobin)
                        c = float(cholesterol)
                        pred = model.predict([[g, h, c]])
                        remark = le.inverse_transform(pred)[0]
                        pid = database.add_patient(name, dob.isoformat(), email, g, h, c, remark)
                        st.success(f"Patient added (id={pid}). Prediction: {remark}")
                        st.balloons()

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
                    glucose = st.number_input("Glucose", min_value=0.0, max_value=1000.0, value=float(row["glucose"]), step=0.1)
                    haemoglobin = st.number_input("Haemoglobin", min_value=0.0, max_value=30.0, value=float(row["haemoglobin"]), step=0.1)
                    cholesterol = st.number_input("Cholesterol", min_value=0.0, max_value=1000.0, value=float(row["cholesterol"]), step=0.1)
                    update_btn = st.form_submit_button("Update Patient ✏️")
                    delete_confirm = st.checkbox("Check to confirm delete")
                    delete_btn = st.form_submit_button("Delete Patient 🗑️")
                    if update_btn:
                        if not name:
                            st.error("Name is required")
                        elif not validate_email(email):
                            st.error("Invalid email")
                        elif not validate_dob(dob):
                            st.error("DOB cannot be in the future")
                        else:
                            g = float(glucose)
                            h = float(haemoglobin)
                            c = float(cholesterol)
                            pred = model.predict([[g, h, c]])
                            remark = le.inverse_transform(pred)[0]
                            database.update_patient(selected, name, dob.isoformat(), email, g, h, c, remark)
                            st.success(f"Patient updated. Prediction: {remark}")
                    if delete_btn:
                        if delete_confirm:
                            database.delete_patient(selected)
                            st.success("Patient deleted")
                        else:
                            st.error("Please check the confirmation box before deleting.")

    # Main area: dashboard and table
    st.header("Dashboard")
    rows = database.get_all_patients()
    rows_list = [dict(r) for r in rows] if rows else []
    df = pd.DataFrame(rows_list)

    # Interactive filters
    filt_col1, filt_col2 = st.columns([2, 3])
    with filt_col1:
        search_name = st.text_input("Search name")
    with filt_col2:
        remarks_filter = st.multiselect("Filter by remark", options=["Healthy", "Prediabetes Risk", "High Cholesterol Risk"], default=["Healthy", "Prediabetes Risk", "High Cholesterol Risk"]) if not df.empty else []

    if not df.empty:
        if search_name:
            df = df[df["full_name"].str.contains(search_name, case=False, na=False)]
        if remarks_filter:
            df = df[df["remarks"].isin(remarks_filter)]

    total = len(df)
    healthy = int((df["remarks"] == "Healthy").sum()) if "remarks" in df else 0
    predi = int((df["remarks"] == "Prediabetes Risk").sum()) if "remarks" in df else 0
    high = int((df["remarks"] == "High Cholesterol Risk").sum()) if "remarks" in df else 0

    # Enhanced KPI cards and donut chart for a polished dashboard
    def render_kpi(title: str, value: int, pct: float, color: str):
        st.markdown(f"""
            <div style='background:{color};padding:16px;border-radius:10px;box-shadow:0 4px 12px rgba(0,0,0,0.06);'>
                <div style='font-size:14px;color:rgba(255,255,255,0.9);'>{title}</div>
                <div style='font-size:28px;font-weight:700;color:#fff;margin-top:6px'>{value}</div>
                <div style='font-size:12px;color:rgba(255,255,255,0.85);margin-top:6px'>
                  {pct:.0f}% of total
                </div>
            </div>
        """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns([1.5, 1, 1, 1])
    k1.markdown("<div class='card' style='padding:18px'><div class='big-title'>Dashboard</div></div>", unsafe_allow_html=True)
    k2.write("")
    if total:
        render_kpi("Total Patients", total, 100.0, "#0b69ff")
        render_kpi("Healthy", healthy, healthy / total * 100 if total else 0, "#16a34a")
        render_kpi("Prediabetes", predi, predi / total * 100 if total else 0, "#f59e0b")
        render_kpi("High Cholesterol", high, high / total * 100 if total else 0, "#ef4444")
    else:
        k2.info("No data")

    # Donut chart showing distribution (Plotly if available, else Streamlit bar_chart)
    if total:
        if px is not None:
            fig = px.pie(values=[healthy, predi, high], names=["Healthy", "Prediabetes Risk", "High Cholesterol Risk"], hole=0.6,
                         color_discrete_map={"Healthy":"#16a34a","Prediabetes Risk":"#f59e0b","High Cholesterol Risk":"#ef4444"})
            fig.update_traces(textinfo='value+percent')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.bar_chart(pd.Series({"Healthy": healthy, "Prediabetes Risk": predi, "High Cholesterol Risk": high}))

    st.header("Patients")
    # pagination controls for table
    page_size = st.selectbox("Rows per page", [10, 25, 50, 100], index=1)
    total_pages = (len(df) // page_size) + (1 if len(df) % page_size else 0) if len(df) else 1
    page = st.number_input("Page", min_value=1, max_value=max(total_pages, 1), value=1)
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
        start = (page - 1) * page_size
        end = start + page_size
        st.dataframe(df_display.iloc[start:end])

        # Bar chart
        counts = df["remarks"].value_counts()
        st.bar_chart(counts)

        # CSV download
        csv = df.to_csv(index=False)
        b = csv.encode("utf-8")
        st.download_button("Download CSV", data=b, file_name="patients.csv", mime="text/csv")
    else:
        st.info("No patient records yet. Add patients using the sidebar form.")


if __name__ == "__main__":
    main()
