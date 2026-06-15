from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .config import (
    ARTIFACT_DIR,
    BACKGROUND_PATH,
    METRICS_PATH,
    MODEL_PATH,
    RANDOM_STATE,
    TEST_SIZE,
)
from .data import load_data, prepare_xy


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    categorical = X.select_dtypes(include=["object", "category"]).columns.tolist()
    numeric = [column for column in X.columns if column not in categorical]

    numeric_pipe = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipe = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "onehot",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            ),
        ]
    )

    return ColumnTransformer(
        [
            ("num", numeric_pipe, numeric),
            ("cat", categorical_pipe, categorical),
        ],
        verbose_feature_names_out=False,
    )


def build_candidates(X: pd.DataFrame) -> dict[str, Pipeline]:
    return {
        "Lojistik Regresyon": Pipeline(
            [
                ("preprocessor", build_preprocessor(X)),
                (
                    "model",
                    LogisticRegression(
                        max_iter=2000,
                        class_weight="balanced",
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        ),
        "Rastgele Orman": Pipeline(
            [
                ("preprocessor", build_preprocessor(X)),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=300,
                        max_depth=6,
                        min_samples_leaf=2,
                        class_weight="balanced",
                        random_state=RANDOM_STATE,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
    }


def metric_dict(model: Pipeline, X: pd.DataFrame, y: pd.Series) -> dict[str, Any]:
    prediction = model.predict(X)
    probability = model.predict_proba(X)[:, 1]
    return {
        "accuracy": round(float(accuracy_score(y, prediction)), 4),
        "precision_risk": round(float(precision_score(y, prediction, zero_division=0)), 4),
        "recall_risk": round(float(recall_score(y, prediction, zero_division=0)), 4),
        "f1_risk": round(float(f1_score(y, prediction, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y, probability)), 4),
        "confusion_matrix": confusion_matrix(y, prediction).tolist(),
        "sample_count": int(len(y)),
    }


def train_and_save(
    model_path: Path | str = MODEL_PATH,
    metrics_path: Path | str = METRICS_PATH,
    background_path: Path | str = BACKGROUND_PATH,
) -> tuple[Pipeline, dict[str, Any]]:
    """İki modeli karşılaştırır; risk yakalama başarısı yüksek modeli kaydeder."""
    df = load_data()
    X, y = prepare_xy(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    comparison: dict[str, Any] = {}
    trained: dict[str, Pipeline] = {}
    for name, candidate in build_candidates(X).items():
        candidate.fit(X_train, y_train)
        trained[name] = candidate
        comparison[name] = {
            "train": metric_dict(candidate, X_train, y_train),
            "test": metric_dict(candidate, X_test, y_test),
        }
        comparison[name]["overfit_gap_auc"] = round(
            comparison[name]["train"]["roc_auc"]
            - comparison[name]["test"]["roc_auc"],
            4,
        )

    # Eğitimde asıl amaç riskli öğrencileri kaçırmamak olduğundan test recall önceliklidir;
    # eşitlikte ROC-AUC ve daha düşük overfit farkı kullanılır.
    selected_name = max(
        comparison,
        key=lambda name: (
            comparison[name]["test"]["recall_risk"],
            comparison[name]["test"]["roc_auc"],
            -comparison[name]["overfit_gap_auc"],
        ),
    )
    selected = trained[selected_name]

    model_path = Path(model_path)
    metrics_path = Path(metrics_path)
    background_path = Path(background_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(selected, model_path)

    preprocessor = selected.named_steps["preprocessor"]
    transformed_train = preprocessor.transform(X_train)
    rng = np.random.default_rng(RANDOM_STATE)
    sample_size = min(150, transformed_train.shape[0])
    sampled_indices = rng.choice(transformed_train.shape[0], size=sample_size, replace=False)
    np.save(background_path, transformed_train[sampled_indices])

    test_probability = selected.predict_proba(X_test)[:, 1]
    test_prediction = selected.predict(X_test)
    predictions = X_test.copy()
    predictions["gercek_risk"] = y_test.values
    predictions["tahmin_risk"] = test_prediction
    predictions["risk_olasiligi"] = np.round(test_probability, 4)
    predictions.to_csv(model_path.parent / "test_predictions.csv", index=False)

    metadata = {
        "selected_model": selected_name,
        "selection_rule": "Önce test risk recall, sonra ROC-AUC, sonra düşük overfit farkı",
        "target_definition": "G3 < 10 ise risk=1",
        "features": X.columns.tolist(),
        "dataset_rows": int(len(df)),
        "risk_count": int(y.sum()),
        "non_risk_count": int((1 - y).sum()),
        "random_state": RANDOM_STATE,
        "test_size": TEST_SIZE,
        "models": comparison,
    }
    metrics_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return selected, metadata


def load_model(path: Path | str = MODEL_PATH) -> Pipeline:
    path = Path(path)
    if not path.exists():
        model, _ = train_and_save()
        return model
    return joblib.load(path)
