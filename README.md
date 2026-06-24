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

Additional artifacts
- Trained model and encoder: `models/health_model.pkl`
- Training metrics: `models/metrics.json`
- Confusion matrix CSV: `models/confusion_matrix.csv`
- Explainability report: `reports/shap_report.md` and `reports/feature_importances.csv` (if SHAP not installed)

Reproduce training locally
```
python train.py
python explainability.py
```

What I suggest next for the interview
- Add a short `train_report.md` summarizing dataset, metrics, and explainability results (I can generate this).
- Pin dependency versions in `requirements.txt` and add `Dockerfile` for reproducibility.
