from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from src.config import BACKGROUND_PATH, METRICS_PATH
from src.explain import explain_instance
from src.model import load_model, train_and_save

st.set_page_config(
    page_title="Öğrenci Başarı Riski",
    page_icon="🎓",
    layout="wide",
)


@st.cache_resource
def load_resources():
    if not METRICS_PATH.exists() or not BACKGROUND_PATH.exists():
        train_and_save()
    model = load_model()
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    background = np.load(BACKGROUND_PATH)
    return model, metrics, background


model, metrics, background = load_resources()
selected_name = metrics["selected_model"]
selected_test = metrics["models"][selected_name]["test"]

st.title("🎓 Öğrenci Başarı Riski Karar Destek Sistemi")
st.caption(
    "İkinci dönem sonundaki mevcut bilgilerle final notunun 100 üzerinden 50'nin altında kalma riskini tahmin eder. "
    "Sonuç eğitim amaçlı karar desteğidir; tek başına öğrenci hakkında karar vermek için kullanılmamalıdır."
)

with st.sidebar:
    st.header("Model özeti")
    st.metric("Seçilen model", selected_name)
    st.metric("Test ROC-AUC", f"{selected_test['roc_auc']:.3f}")
    st.metric("Risk yakalama (Recall)", f"{selected_test['recall_risk']:.1%}")
    st.write(f"Veri seti: {metrics['dataset_rows']} öğrenci")
    st.write(f"Riskli örnek sayısı: {metrics['risk_count']}")
    st.info("Risk tanımı: Final notu 50/100 altında (veri setinde G3 < 10/20)")

st.subheader("Öğrenci bilgilerini girin")
col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider("Yaş", 15, 22, 17)
    address_label = st.selectbox("Yerleşim türü", ["Kentsel", "Kırsal"])
    traveltime = st.select_slider(
        "Okula ulaşım süresi",
        options=[1, 2, 3, 4],
        value=2,
        format_func=lambda x: {
            1: "15 dakikadan az",
            2: "15-30 dakika",
            3: "30-60 dakika",
            4: "60 dakikadan fazla",
        }[x],
    )
    studytime = st.select_slider(
        "Haftalık çalışma süresi",
        options=[1, 2, 3, 4],
        value=2,
        format_func=lambda x: {
            1: "2 saatten az",
            2: "2-5 saat",
            3: "5-10 saat",
            4: "10 saatten fazla",
        }[x],
    )
    failures = st.number_input("Geçmiş başarısız ders sayısı", 0, 4, 0)

with col2:
    schoolsup_label = st.selectbox("Okuldan ek eğitim desteği", ["Hayır", "Evet"])
    famsup_label = st.selectbox("Aileden eğitim desteği", ["Evet", "Hayır"])
    higher_label = st.selectbox("Yükseköğretime devam etme hedefi", ["Evet", "Hayır"])
    internet_label = st.selectbox("Evde internet erişimi", ["Evet", "Hayır"])
    famrel = st.slider("Aile ilişkilerinin kalitesi", 1, 5, 4)

with col3:
    goout = st.slider("Arkadaşlarla dışarı çıkma sıklığı", 1, 5, 3)
    health = st.slider("Genel sağlık durumu", 1, 5, 4)
    absences = st.number_input("Devamsızlık sayısı", 0, 93, 4)
    g1_100 = st.slider("1. dönem notu (100 üzerinden)", 0, 100, 55)
    g2_100 = st.slider("2. dönem notu (100 üzerinden)", 0, 100, 55)
    st.caption("Notlar model için otomatik olarak 20'lik ölçeğe dönüştürülür.")

input_frame = pd.DataFrame(
    [
        {
            "age": age,
            "address": "U" if address_label == "Kentsel" else "R",
            "traveltime": traveltime,
            "studytime": studytime,
            "failures": failures,
            "schoolsup": "yes" if schoolsup_label == "Evet" else "no",
            "famsup": "yes" if famsup_label == "Evet" else "no",
            "higher": "yes" if higher_label == "Evet" else "no",
            "internet": "yes" if internet_label == "Evet" else "no",
            "famrel": famrel,
            "goout": goout,
            "health": health,
            "absences": absences,
            # UCI veri setindeki G1 ve G2 notları 0-20 ölçeğindedir.
            # Kullanıcı 100'lük sistemde giriş yapar; model için 5'e bölünür.
            "G1": g1_100 / 5,
            "G2": g2_100 / 5,
        }
    ]
)

if st.button("Riski hesapla", type="primary", width="stretch"):
    risk_probability = float(model.predict_proba(input_frame)[0, 1])
    prediction = int(risk_probability >= 0.5)

    if risk_probability >= 0.70:
        risk_level = "Yüksek risk"
        recommendation = (
            "Öğrenciyle kısa bir görüşme planlanması, ders desteği ve devamsızlık nedenlerinin "
            "incelenmesi önerilir."
        )
    elif risk_probability >= 0.40:
        risk_level = "Orta risk"
        recommendation = (
            "Not ve devam durumu izlenmeli; gerekli görülürse erken akademik destek sunulmalıdır."
        )
    else:
        risk_level = "Düşük risk"
        recommendation = "Mevcut durum korunmalı ve öğrenci rutin olarak izlenmelidir."

    result_col, explanation_col = st.columns([1, 2])
    with result_col:
        st.subheader("Tahmin sonucu")
        st.metric("Risk olasılığı", f"{risk_probability:.1%}")
        if prediction == 1:
            st.error(risk_level)
        else:
            st.success(risk_level)
        st.write(recommendation)

    with explanation_col:
        st.subheader("Model bu sonuca neden ulaştı?")
        explanation = explain_instance(model, input_frame, background).head(8)
        display = explanation.sort_values("shap_katkisi")
        fig, ax = plt.subplots(figsize=(8, 4.6))
        ax.barh(display["etiket"], display["shap_katkisi"])
        ax.axvline(0, linewidth=1)
        ax.set_xlabel("SHAP katkısı (pozitif değer riski artırır)")
        ax.set_ylabel("")
        ax.set_title("En etkili özellikler")
        fig.tight_layout()
        st.pyplot(fig, width="stretch")
        st.dataframe(
            explanation[["etiket", "etki", "shap_katkisi"]].rename(
                columns={
                    "etiket": "Özellik",
                    "etki": "Yön",
                    "shap_katkisi": "SHAP katkısı",
                }
            ),
            hide_index=True,
            width="stretch",
        )

with st.expander("Model karşılaştırmasını göster"):
    rows = []
    for name, values in metrics["models"].items():
        rows.append(
            {
                "Model": name,
                "Test doğruluk": values["test"]["accuracy"],
                "Test ROC-AUC": values["test"]["roc_auc"],
                "Risk recall": values["test"]["recall_risk"],
                "Risk F1": values["test"]["f1_risk"],
                "AUC overfit farkı": values["overfit_gap_auc"],
            }
        )
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")

st.divider()
st.caption(
    "Veri kaynağı: UCI Machine Learning Repository - Student Performance. "
    "Bu uygulama gerçek bir okulun öğrenci verileriyle doğrulanmamıştır."
)
