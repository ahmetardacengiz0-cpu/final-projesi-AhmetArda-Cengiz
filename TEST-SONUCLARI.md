# Test sonuçları

Bu dosyadaki sayısal sonuçlar `python3 train.py` komutu ile yeniden üretilebilir. Test bölmesi veri setinin %25’idir ve hedef sınıf oranı korunmuştur (`random_state=42`, stratified split).

## Model karşılaştırması

| Model | Eğitim doğruluğu | Test doğruluğu | Test ROC-AUC | Risk recall | Risk F1 | AUC farkı |
|---|---:|---:|---:|---:|---:|---:|
| Lojistik Regresyon | 0.924 | 0.890 | 0.941 | 0.920 | 0.719 | 0.045 |
| Rastgele Orman | 0.967 | 0.877 | 0.944 | 0.840 | 0.677 | 0.055 |

## Overfitting / underfitting değerlendirmesi

Lojistik Regresyonun eğitim-test ROC-AUC farkı 0,045; Rastgele Ormanın farkı 0,055’tir. İki model de eğitimde daha iyi sonuç verdiği için hafif overfitting vardır. Rastgele Orman daha yüksek eğitim başarısına rağmen testte riskli öğrencilerin %84’ünü yakalarken Lojistik Regresyon %92’sini yakalamıştır. Bu nedenle son model olarak Lojistik Regresyon seçilmiştir.

Sonuçlar modelin tamamen ezberlemediğini, ancak daha büyük ve yerel bir veri setiyle yeniden doğrulanması gerektiğini göstermektedir.

## Beş kullanıcı testi

| No | Senaryo | Risk olasılığı | Gözlenen davranış | Sonuç |
|---:|---|---:|---|---|
| 1 | G1=30/100, G2=35/100, devamsızlık=18, geçmiş başarısızlık=1 | %99,79 | Yüksek risk üretildi | Başarılı |
| 2 | G1=75/100, G2=80/100, devamsızlık=2 | <%0,01 | Düşük risk üretildi | Başarılı |
| 3 | Sınır değer: G1=45/100, G2=45/100, devamsızlık=6 | %53,51 | Eşik üstünde risk üretildi ve açıklama oluşturuldu | Başarılı |
| 4 | Formdaki tüm sayısal alanların minimum değerleri | %100,00 | Uygulama hata vermeden tahmin üretti | Başarılı |
| 5 | Formdaki tüm sayısal alanların maksimum değerleri | <%0,01 | Uygulama hata vermeden tahmin üretti; yüksek G1-G2 etkisi baskın çıktı | Başarılı |

Not: UCI veri setindeki notlar 20’lik sistemdedir. Yukarıdaki G1 ve G2 değerleri uygulamadaki kullanıcı girişine uygun olarak 100’lük sistemde gösterilmiştir. Uygulama bu değerleri model için otomatik olarak 20’lik ölçeğe dönüştürür.

## Başarısız veya yetersiz kalınan durum

Veri setinde Türkiye’deki öğrenciler bulunmadığı için modelin Türkiye’deki gerçek bir okulda aynı performansı göstereceği varsayılamaz. Ayrıca G1 ve G2 notları henüz oluşmamışsa sistem güçlü bir erken dönem tahmini yapamaz. Uygulama bu nedenle tanı veya otomatik karar aracı değil, eğitim amaçlı bir prototiptir.

## Otomatik testler

```bash
python3 -m pytest -q
```

Hazırlanan otomatik testler:

1. Veri dosyasının biçimini ve gerekli sütunları kontrol eder.
2. Risk hedefinin doğru üretildiğini kontrol eder.
3. Model olasılığının 0–1 aralığında olduğunu doğrular.
4. SHAP açıklamasının üretilebildiğini kontrol eder.
5. Streamlit uygulamasının temel akışını test eder.

Testlerin tamamı başarıyla geçmiştir.
