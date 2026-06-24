"""Train a RandomForest model with train/test split and save metrics.
Outputs:
- models/health_model.pkl
- models/metrics.json
- models/confusion_matrix.csv
"""
import json
from pathlib import Path
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


DATA_PATH = Path("data/sample_data.csv")
MODEL_PATH = Path("models/health_model.pkl")
METRICS_PATH = Path("models/metrics.json")
CM_PATH = Path("models/confusion_matrix.csv")


def load_or_generate_data(path: Path):
    if not path.exists():
        from data.generate_sample_data import generate

        print("Generating sample dataset...")
        generate(str(path))
    df = pd.read_csv(path)
    return df


def train(save: Path = MODEL_PATH, metrics_out: Path = METRICS_PATH, cm_out: Path = CM_PATH):
    df = load_or_generate_data(DATA_PATH)
    X = df[["glucose", "haemoglobin", "cholesterol"]].values
    y = df["risk"].values

    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42, stratify=y_enc)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds, average="weighted", zero_division=0)
    rec = recall_score(y_test, preds, average="weighted", zero_division=0)
    f1 = f1_score(y_test, preds, average="weighted", zero_division=0)
    cm = confusion_matrix(y_test, preds)

    metrics = {"accuracy": float(acc), "precision": float(prec), "recall": float(rec), "f1": float(f1)}

    save.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "le": le}, str(save))

    metrics_out.parent.mkdir(parents=True, exist_ok=True)
    with open(metrics_out, "w") as f:
        json.dump(metrics, f, indent=2)

    # save confusion matrix as CSV
    cm_out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(cm).to_csv(cm_out, index=False)

    print("Training complete. Metrics:", metrics)
    return metrics


if __name__ == "__main__":
    train()
