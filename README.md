##  1. Veri Kümesinin Özgün Olarak Oluşturulması ve Metodolojisi

Bu projedeki veri kümesi hazır bir kaynaktan alınmamış; tamamen tarafımdan geliştirilen veri toplama mimarisi ile **özgün (custom)** olarak sıfırdan inşa edilmiştir.

###  Veri Toplama Süreci ve Grid (Izgara) Tarama Sistemi
- **Veri Kaynağı:** Görseller, Google Static Maps API entegrasyonu kullanılarak dinamik olarak çekilmiştir.
- **Tarama Algoritması (`indir.py`):** Belirlenen stratejik coğrafi lokasyonların (koordinat sınırları), enlem ve boylam adımları üzerinden otomatik bir grid (ızgara) tarama algoritmasıyla taranması sağlanmıştır. Bu sayede manuel veri toplama hatalarının önüne geçilmiştir.
- **Çeşitlilik ve Genelleme Kapasitesi:** Modelin farklı coğrafi, spektral ve ışık koşullarında genelleme yeteneğini (generalization) artırmak adına dünya genelinde karakteristiği birbirinden tamamen farklı **4 ana lokasyon** taranmıştır:
  1. **Ambarlı (Türkiye):** Yoğun ticari konteyner limanı ve yoğun gemi trafiği dokusu.
  2. **Tuzla (Türkiye):** Endüstriyel tersane bölgeleri, doğrusal hangar çatıları ve kıyı yapıları.
  3. **Norveç Fiyortları:** Yüksek dağ gölgeleri, derin/koyu su dokusu ve zorlu topoğrafya.
  4. **Bahamalar:** Açık renkli sığ sular, mercan resifleri ve yüksek yansımalı deniz tabanı.

###  Veri Kümesi İstatistikleri ve Hiyerarşisi
Toplam **763 adet** özgün uydu görüntüsü toplanmış ve derin öğrenme modelinin veri yükleme akışına (`DataLoader`) uygun olarak şu hiyerarşide sınıflandırılmıştır:
- **`Gemi Var/`** -> `ambarli_1`, `bahamalar_1`, `norvec_1`, `tuzla_1` (Gemi/tekne içeren pikseller)
- **`Gemi Yok/`** -> `ambarli_2`, `bahamalar_2`, `norvec_2`, `tuzla_2` (Boş deniz, kara, bulut ve kıyı yapıları)

## Sprint 3: Derin Eğitim ve Optimizasyon (09.06.2026)
Model yerel ortam kısıtlamalarından çıkarılarak **Google Colab (T4 GPU)** bulut platformuna taşınmıştır. 
Önerilen YOLOv8n mimarisi, özgün veri kümesindeki 3842 gemi nesnesi üzerinden **100 Epoch** boyunca derin eğitime tabi tutulmuştur.

* **Eğitim Süresi:** 0.622 saat (~37 dakika)
* **Precision (Kesinlik):** %68.4
* **Recall (Duyarlılık):** %50.6
* **mAP50 Başarı Skoru:** **%56.6** (Akademik baseline başarı esiği aşılmıştır)
* **Inference (Çıkarım Hızı):** Görsel başına **2.4 ms** ile gerçek zamanlı tespite hazır hale getirilmiştir.

Eğitilen en kararlı ağırlık dosyasına `outputs/weights/best.pt` konumundan, 100 Epoch'luk pürüzsüz loss ve başarı eğrilerine ise `outputs/results.png` üzerinden erişilebilir.
