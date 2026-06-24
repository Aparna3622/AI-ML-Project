"""Generate model explainability output using SHAP if available,
otherwise fallback to model feature importances.
Writes outputs to `reports/` and `models/`.
"""
from pathlib import Path
import joblib
import pandas as pd

MODEL_PATH = Path("models/health_model.pkl")
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def explain():
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model not found. Run train.py first.")

    obj = joblib.load(str(MODEL_PATH))
    model = obj["model"]
    le = obj["le"]

    try:
        import shap
        import matplotlib.pyplot as plt

        # load a small sample for background
        df = pd.read_csv("data/sample_data.csv")
        X = df[["glucose", "haemoglobin", "cholesterol"]]

        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)

        # summary plot
        plt.figure(figsize=(8, 4))
        shap.summary_plot(shap_values, X, show=False)
        out = REPORTS_DIR / "shap_summary.png"
        plt.savefig(out, bbox_inches="tight")
        plt.close()

        # write short report
        with open(REPORTS_DIR / "shap_report.md", "w") as f:
            f.write("# SHAP Explainability Report\n\nGenerated SHAP summary plot for model features. See shap_summary.png.\n")

        print("SHAP explainability generated:", out)
    except Exception:
        # fallback to feature importances
        importances = model.feature_importances_
        feat_names = ["glucose", "haemoglobin", "cholesterol"]
        df_imp = pd.DataFrame({"feature": feat_names, "importance": importances})
        out = REPORTS_DIR / "feature_importances.csv"
        df_imp.to_csv(out, index=False)
        with open(REPORTS_DIR / "shap_report.md", "w") as f:
            f.write("# Explainability Fallback Report\n\nSHAP not available. Saved feature importances to feature_importances.csv.\n")
        print("Feature importances saved:", out)


if __name__ == "__main__":
    explain()
