# Health Prediction App

Simple Streamlit app that predicts health risk (Healthy / Prediabetes Risk / High Cholesterol Risk) from basic blood values and stores patient records in SQLite.

Features
- CRUD operations for patients
- Simple RandomForest ML model (trained on a tiny sample) saved to `models/health_model.pkl` on first run
- Data validation for email and DOB

Quick start

1. Create a virtual environment and install requirements:

```bash
pip install -r requirements.txt
```

2. Run the app:

```bash
streamlit run app.py
```

Notes
- The sample ML dataset is intentionally small and illustrative. Replace with a larger dataset for production use.
- The model is created automatically if `models/health_model.pkl` is missing.
