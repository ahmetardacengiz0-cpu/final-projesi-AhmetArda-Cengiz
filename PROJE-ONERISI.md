# PROJE ÖNERİSİ

## Seçilen görev numarası

Seçenek 3 – Açıklanabilir Makine Öğrenmesi Karar Destek Ürünü

## Ürünün adı

Öğrenci Başarı Riski ve Açıklanabilir Erken Uyarı Sistemi

## Çözülecek problem

Bir öğrencinin final notunda başarısızlık riski çoğu zaman dönem sonunda fark edilmektedir. Bu proje; öğrencinin dönem içi notlarını, çalışma süresini, devamsızlığını, geçmiş başarısızlıklarını ve destek bilgilerini kullanarak final notunun **50/100 altında kalma olasılığını** önceden tahmin etmeyi amaçlar.

UCI veri setinde notlar 0–20 ölçeğindedir ve risk hedefi `G3 < 10/20` olarak tanımlanmıştır. Bu değer 100’lük sistemde `50/100` değerine karşılık gelir. Uygulama kullanıcıdan G1 ve G2 notlarını 100 üzerinden alır ve model için otomatik olarak 20’lik ölçeğe dönüştürür.

Böylece öğretmen veya akademik danışman, riskli öğrencileri erken inceleyebilir ve uygun destek sürecini planlayabilir.

## Hedef kullanıcı

Öğretmenler, okul rehberlik birimleri, akademik danışmanlar ve eğitim yöneticileri.

## Kullanılacak veri veya bilgi kaynakları

- UCI Machine Learning Repository – Student Performance veri seti
- Veri seti DOI: [10.24432/C5TG7T](https://doi.org/10.24432/C5TG7T)
- Scikit-learn resmî dokümantasyonu
- SHAP resmî dokümantasyonu
- Streamlit resmî dokümantasyonu

## Kullanılması planlanan teknolojiler

Python, pandas, NumPy, scikit-learn, SHAP, Streamlit, matplotlib, pytest, GitHub ve GitHub Issues.

## Beklenen ürün çıktısı

Kullanıcının öğrenci bilgilerini bir form üzerinden girdiği; sistemin risk olasılığı, risk düzeyi, kısa öneri ve SHAP tabanlı karar açıklaması ürettiği çalışan bir web uygulaması.

## Ürünün diğer çalışmalardan ayrılan yönü

Sistem yalnızca risk sınıfı vermeyecek; hangi özelliklerin tahmini artırdığını veya azalttığını kullanıcıya açıklayacaktır. Ayrıca model seçiminde yalnızca doğruluk değil, riskli öğrencileri yakalama oranı ve eğitim-test performans farkı birlikte değerlendirilecektir.
