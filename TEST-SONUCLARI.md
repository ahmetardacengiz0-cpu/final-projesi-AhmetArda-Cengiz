# Test sonuçları

Bu dosyadaki sayısal sonuçlar `python train.py` komutu ile yeniden üretilebilir. Test bölmesi veri setinin %25'idir ve hedef sınıf oranı korunmuştur (`random_state=42`, stratified split).

## Model karşılaştırması

| Model | Eğitim doğruluk | Test doğruluk | Test ROC-AUC | Risk recall | Risk F1 | AUC farkı |
|---|---:|---:|---:|---:|---:|---:|
| Lojistik Regresyon | 0.924 | 0.890 | 0.941 | 0.920 | 0.719 | 0.045 |
| Rastgele Orman | 0.967 | 0.877 | 0.944 | 0.840 | 0.677 | 0.055 |

## Overfitting / underfitting değerlendirmesi

Lojistik Regresyonun eğitim-test ROC-AUC farkı 0,045; Rastgele Ormanın farkı 0,055'tir. İki model de eğitimde daha iyi sonuç verdiği için hafif overfitting vardır. Rastgele Orman daha yüksek eğitim başarısına rağmen testte riskli öğrencilerin %84'ünü yakalarken Lojistik Regresyon %92'sini yakalamıştır. Bu nedenle son model olarak Lojistik Regresyon seçilmiştir. Sonuçlar modelin tamamen ezberlemediğini, ancak daha büyük ve yerel veriyle doğrulanması gerektiğini gösterir.

## Beş kullanıcı testi

| No | Senaryo | Risk olasılığı | Gözlenen davranış | Sonuç |
|---:|---|---:|---|---|
| 1 | G1=6, G2=7, devamsızlık=18, geçmiş başarısızlık=1 | %99,79 | Yüksek risk üretildi | Başarılı |
| 2 | G1=15, G2=16, devamsızlık=2 | <%0,01 | Düşük risk üretildi | Başarılı |
| 3 | Sınır değer: G1=9, G2=9, devamsızlık=6 | %53,51 | Eşik üstünde risk üretildi ve açıklama oluşturuldu | Başarılı |
| 4 | Formdaki tüm sayısal alanların minimum değerleri | %100,00 | Uygulama hata vermeden tahmin üretti | Başarılı |
| 5 | Formdaki tüm sayısal alanların maksimum değerleri | <%0,01 | Uygulama hata vermeden tahmin üretti; yüksek G1-G2 etkisi baskın çıktı | Başarılı |

## Başarısız veya yetersiz kalınan durum

Veri setinde Türkiye'deki öğrenciler bulunmadığı için modelin Türkiye'deki gerçek bir okulda aynı performansı göstereceği varsayılamaz. Ayrıca G1 ve G2 notları henüz oluşmamışsa sistem güçlü bir erken dönem tahmini yapamaz. Uygulama bu nedenle tanı veya otomatik karar aracı değil, eğitim amaçlı bir prototiptir.

## Otomatik testler

```bash
pytest -q
```

Testler veri dosyasının biçimini, hedef sınıfı, model olasılığını ve SHAP açıklamasının üretilebildiğini kontrol eder.
