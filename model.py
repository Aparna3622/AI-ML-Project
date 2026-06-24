import os
from pathlib import Path
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


def train_and_save_model(path: str = "models/health_model.pkl"):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    # Sample dataset (small, illustrative)
    data = {
        "glucose": [80, 90, 110, 150, 170],
        "haemoglobin": [13, 14, 12, 11, 10],
        "cholesterol": [150, 180, 220, 260, 300],
        "risk": ["Healthy", "Healthy", "Prediabetes Risk", "High Cholesterol Risk", "High Cholesterol Risk"],
    }

    X = np.column_stack((data["glucose"], data["haemoglobin"], data["cholesterol"]))
    y = np.array(data["risk"])

    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y_enc)

    joblib.dump({"model": model, "le": le}, str(p))
    return str(p)


def load_model(path: str = "models/health_model.pkl"):
    if not os.path.exists(path):
        train_and_save_model(path)
    obj = joblib.load(path)
    return obj["model"], obj["le"]


if __name__ == "__main__":
    train_and_save_model()
