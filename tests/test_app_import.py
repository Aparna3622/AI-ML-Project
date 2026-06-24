import importlib
import importlib.util
import pytest


def test_app_import():
    if importlib.util.find_spec("streamlit") is None:
        pytest.skip("streamlit not installed; skipping app import test")
    importlib.import_module("app")
