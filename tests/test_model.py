import importlib.util
import pytest


if importlib.util.find_spec("numpy") is None or importlib.util.find_spec("sklearn") is None:
    pytest.skip("numpy or sklearn not installed; skipping model test", allow_module_level=True)
else:
    from model import load_model


    def test_model_predict():
        model, le = load_model()
        pred = model.predict([[80, 13, 150]])
        remark = le.inverse_transform(pred)[0]
        assert remark in ["Healthy", "Prediabetes Risk", "High Cholesterol Risk"]
