import numpy as np

from src.config import BACKGROUND_PATH
from src.data import load_data, prepare_xy
from src.explain import explain_instance
from src.model import load_model


def test_model_probability_is_valid():
    X, _ = prepare_xy(load_data())
    model = load_model()
    probability = model.predict_proba(X.iloc[[0]])[0, 1]
    assert 0.0 <= probability <= 1.0


def test_shap_explanation_has_all_original_features():
    X, _ = prepare_xy(load_data())
    model = load_model()
    background = np.load(BACKGROUND_PATH)
    explanation = explain_instance(model, X.iloc[[0]], background)
    assert set(explanation["ozellik"]) == set(X.columns)
    assert explanation["shap_katkisi"].notna().all()
