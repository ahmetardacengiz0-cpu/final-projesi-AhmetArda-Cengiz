from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "student-por.csv"
ARTIFACT_DIR = PROJECT_ROOT / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "risk_model.joblib"
METRICS_PATH = ARTIFACT_DIR / "metrics.json"
BACKGROUND_PATH = ARTIFACT_DIR / "shap_background.npy"

TARGET_COLUMN = "G3"
RISK_THRESHOLD_GRADE = 10
RANDOM_STATE = 42
TEST_SIZE = 0.25

FEATURES = [
    "age",
    "address",
    "traveltime",
    "studytime",
    "failures",
    "schoolsup",
    "famsup",
    "higher",
    "internet",
    "famrel",
    "goout",
    "health",
    "absences",
    "G1",
    "G2",
]

FEATURE_LABELS_TR = {
    "age": "Yaş",
    "address": "Yerleşim türü",
    "traveltime": "Okula ulaşım süresi",
    "studytime": "Haftalık çalışma süresi",
    "failures": "Geçmiş başarısız ders sayısı",
    "schoolsup": "Okuldan ek destek",
    "famsup": "Aileden eğitim desteği",
    "higher": "Yükseköğretim hedefi",
    "internet": "Evde internet",
    "famrel": "Aile ilişkileri",
    "goout": "Arkadaşlarla dışarı çıkma sıklığı",
    "health": "Sağlık durumu",
    "absences": "Devamsızlık",
    "G1": "1. dönem notu",
    "G2": "2. dönem notu",
}
