from __future__ import annotations
from pathlib import Path

import pandas as pd

from .config import DATA_PATH, FEATURES, RISK_THRESHOLD_GRADE, TARGET_COLUMN


def load_data(path: Path | str = DATA_PATH) -> pd.DataFrame:
    """UCI Student Performance Portuguese veri dosyasını yükler ve doğrular."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Veri dosyası bulunamadı: {path}. scripts/download_data.py çalıştırılabilir."
        )

    df = pd.read_csv(path, sep=";")
    required = set(FEATURES + [TARGET_COLUMN])
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"Veri setinde zorunlu sütunlar eksik: {missing}")

    return df


def prepare_xy(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Girdi özelliklerini ve ikili risk hedefini üretir.

    Risk sınıfı: final notu G3 < 10 ise 1, aksi durumda 0.
    G1 ve G2, final notundan önce bilinen ara dönem notlarıdır.
    """
    X = df[FEATURES].copy()
    y = (df[TARGET_COLUMN] < RISK_THRESHOLD_GRADE).astype(int)
    y.name = "risk"
    return X, y
