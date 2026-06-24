"""Generate a sample dataset for health risk prediction.
Creates `data/sample_data.csv` with columns: glucose, haemoglobin, cholesterol, risk
"""
import csv
import random
from pathlib import Path


def generate(path: str = "data/sample_data.csv", n: int = 500, seed: int = 42):
    random.seed(seed)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for i in range(n):
        # base healthy ranges
        glucose = round(random.gauss(100, 25))
        haemoglobin = round(random.gauss(13.5, 1.5), 1)
        cholesterol = round(random.gauss(190, 40))

        # simple rule to assign risk label (for demo)
        if glucose < 100 and cholesterol < 200 and haemoglobin >= 12:
            risk = "Healthy"
        elif 100 <= glucose < 140 or 200 <= cholesterol < 240:
            risk = "Prediabetes Risk"
        else:
            risk = "High Cholesterol Risk"

        rows.append({
            "glucose": glucose,
            "haemoglobin": haemoglobin,
            "cholesterol": cholesterol,
            "risk": risk,
        })

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["glucose", "haemoglobin", "cholesterol", "risk"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


if __name__ == "__main__":
    generate()
