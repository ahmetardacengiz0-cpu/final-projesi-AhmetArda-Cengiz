from __future__ import annotations

import re

import numpy as np
import pandas as pd
import shap
from sklearn.pipeline import Pipeline

from .config import FEATURE_LABELS_TR


def _original_feature(encoded_name: str, original_columns: list[str]) -> str:
    if encoded_name in original_columns:
        return encoded_name
    for column in original_columns:
        if encoded_name.startswith(f"{column}_"):
            return column
    return re.split("_", encoded_name, maxsplit=1)[0]


def explain_instance(
    pipeline: Pipeline,
    instance: pd.DataFrame,
    background: np.ndarray,
) -> pd.DataFrame:
    """Seçili lojistik regresyon kararı için yerel SHAP katkılarını döndürür."""
    preprocessor = pipeline.named_steps["preprocessor"]
    estimator = pipeline.named_steps["model"]
    transformed = preprocessor.transform(instance)
    feature_names = preprocessor.get_feature_names_out().tolist()

    explainer = shap.LinearExplainer(estimator, background)
    shap_values = explainer(transformed).values[0]

    rows = []
    original_columns = instance.columns.tolist()
    for encoded_name, value in zip(feature_names, shap_values, strict=True):
        original = _original_feature(encoded_name, original_columns)
        rows.append(
            {
                "ozellik": original,
                "etiket": FEATURE_LABELS_TR.get(original, original),
                "kodlanmis_ozellik": encoded_name,
                "shap_katkisi": float(value),
            }
        )

    frame = pd.DataFrame(rows)
    aggregated = (
        frame.groupby(["ozellik", "etiket"], as_index=False)["shap_katkisi"]
        .sum()
        .sort_values("shap_katkisi", key=lambda series: series.abs(), ascending=False)
    )
    aggregated["etki"] = np.where(
        aggregated["shap_katkisi"] > 0,
        "Riski artırıyor",
        "Riski azaltıyor",
    )
    return aggregated
