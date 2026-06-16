# Kullanıcı senaryosu

## Senaryo: Danışmanın riskli öğrenciyi incelemesi

1. Akademik danışman uygulamayı açar.
2. Öğrencinin yaşı, çalışma süresi, geçmiş başarısızlıkları, destek durumu, devamsızlığı ve G1-G2 notlarını forma girer.
3. **Riski hesapla** düğmesine basar.
4. Uygulama başarısızlık risk olasılığını ve düşük/orta/yüksek risk seviyesini gösterir.
5. SHAP açıklaması, riski en fazla artıran ve azaltan özellikleri listeler.
6. Danışman bu çıktıyı tek başına karar olarak değil, öğrenciyle görüşme ve destek ihtiyacını inceleme amacıyla kullanır.

## Örnek yüksek risk girdisi

- G1: 6
- G2: 7
- Devamsızlık: 18
- Geçmiş başarısızlık: 1
- Haftalık çalışma: 2 saatten az

## Örnek düşük risk girdisi

- G1: 15
- G2: 16
- Devamsızlık: 2
- Geçmiş başarısızlık: 0
- Haftalık çalışma: 5-10 saat
