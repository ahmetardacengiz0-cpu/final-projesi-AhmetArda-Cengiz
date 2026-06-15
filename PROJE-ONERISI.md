# PROJE ÖNERİSİ

## Seçilen görev numarası

**Seçenek 3 - Açıklanabilir Makine Öğrenmesi Karar Destek Ürünü**

## Ürünün adı

**Öğrenci Başarı Riski ve Açıklanabilir Erken Uyarı Sistemi**

## Çözülecek problem

Bir öğrencinin final notunda başarısızlık riski çoğu zaman dönem sonunda fark edilmektedir. Proje, ikinci dönem notu ve öğrencinin çalışma, devam ve destek bilgilerini kullanarak final notunun 10'un altında kalma olasılığını önceden tahmin etmeyi amaçlar. Böylece öğretmen veya akademik danışman, riskli öğrencileri erken inceleyebilir.

## Hedef kullanıcı

Öğretmenler, okul rehberlik birimleri ve akademik danışmanlar.

## Kullanılacak veri veya bilgi kaynakları

- UCI Machine Learning Repository - Student Performance veri seti
- Veri seti DOI: https://doi.org/10.24432/C5TG7T
- Scikit-learn resmî dokümantasyonu
- SHAP resmî dokümantasyonu
- Streamlit resmî dokümantasyonu

## Kullanılması planlanan teknolojiler

Python, pandas, scikit-learn, SHAP, Streamlit, matplotlib, pytest, GitHub Actions ve GitHub Issues.

## Beklenen ürün çıktısı

Kullanıcının öğrenci bilgilerini bir form üzerinden girdiği; sistemin risk olasılığı, risk düzeyi, kısa öneri ve SHAP tabanlı karar açıklaması ürettiği çalışan web uygulaması.

## Ürünün diğer çalışmalardan ayrılan yönü

Sistem yalnızca risk sınıfı vermeyecek; hangi özelliklerin tahmini artırdığını veya azalttığını kullanıcıya açıklayacaktır. Ayrıca model seçiminde yalnızca doğruluk değil, riskli öğrencileri yakalama oranı ve overfitting farkı birlikte değerlendirilecektir.
