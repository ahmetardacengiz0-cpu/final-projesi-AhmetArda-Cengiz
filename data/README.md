# Veri kaynağı

Bu klasördeki `student-por.csv`, **UCI Machine Learning Repository - Student Performance** veri setinin Portekizce dersi bölümüdür.

- Resmî veri sayfası: https://archive.ics.uci.edu/dataset/320/student+performance
- DOI: https://doi.org/10.24432/C5TG7T
- Resmî indirme: https://archive.ics.uci.edu/static/public/320/student%2Bperformance.zip
- Lisans: Creative Commons Attribution 4.0 International (CC BY 4.0)
- Veri sahibi/atıf: Cortez, P. (2008). *Student Performance*. UCI Machine Learning Repository.

Dosyanın projeye eklenen kopyası 649 satır ve 33 sütun içerir. SHA-256: `a7594a11d7771c0efe1a740824e0e833da9c4cad07c39a9766a874575563fb3f`. Veri; okul raporları ve öğrenci anketlerinden elde edilen demografik, sosyal, okul ve not özelliklerini içerir. Hedef olarak `G3 < 10` koşulu ile ikili risk sınıfı üretilmiştir.

Projenin çevrimdışı çalışabilmesi için veri dosyası depoya eklenmiştir. Yeniden indirmek için:

```bash
python scripts/download_data.py
```
