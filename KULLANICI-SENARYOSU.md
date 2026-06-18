# Kullanıcı senaryosu

## Senaryo: Danışmanın riskli öğrenciyi incelemesi

1. Akademik danışman uygulamayı açar.
2. Öğrencinin yaşı, çalışma süresi, geçmiş başarısızlıkları, destek durumu, devamsızlığı ve G1-G2 notlarını forma girer.
3. G1 ve G2 notlarını 100 üzerinden girer.
4. **Riski hesapla** düğmesine basar.
5. Uygulama başarısızlık risk olasılığını ve düşük/orta/yüksek risk seviyesini gösterir.
6. SHAP açıklaması, riski en fazla artıran ve azaltan özellikleri listeler.
7. Danışman bu çıktıyı tek başına karar olarak değil, öğrenciyle görüşme ve destek ihtiyacını inceleme amacıyla kullanır.

## Örnek yüksek risk girdisi

- G1: 30/100
- G2: 35/100
- Devamsızlık: 18
- Geçmiş başarısızlık: 1
- Haftalık çalışma: 2 saatten az

Beklenen davranış: Sistem yüksek risk olasılığı üretir ve düşük dönem notları ile geçmiş başarısızlık gibi özelliklerin tahmine etkisini açıklar.

## Örnek düşük risk girdisi

- G1: 75/100
- G2: 80/100
- Devamsızlık: 2
- Geçmiş başarısızlık: 0
- Haftalık çalışma: 5–10 saat

Beklenen davranış: Sistem düşük risk olasılığı üretir ve yüksek dönem notlarının riski azaltan etkisini açıklar.

## Kullanım notu

UCI veri setindeki G1 ve G2 notları 0–20 ölçeğindedir. Uygulama kullanıcıdan aldığı 100’lük notları model için otomatik olarak 5’e bölerek 20’lik ölçeğe dönüştürür.
