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

## Sprint 2: Manuel Veri Etiketleme, Lokal Baseline Model ve Altyapı Hazırlığı (06.06.2026)
Projenin bu aşamasında, uydu görüntülerinden oluşan ham veri kümesi üzerinde yüksek doğruluklu tahminler elde edebilmek amacıyla kapsamlı bir veri işleme ve manuel etiketleme (data annotation) süreci yürütülmüştür. Ardından yerel donanım üzerinde YOLOv8n mimarisiyle ilk prototip (baseline) denemeleri gerçekleştirilmiştir.

* **Manuel Veri Hazırlığı & Etiketleme:** Toplanan ham uydu fotoğrafları üzerindeki **3842 adet gemi nesnesi (instance) tek tek el ile (manuel)** bounding box (tahmin kutusu) kullanılarak etiketlenmiş ve YOLO formatına uygun hale getirilmiştir. Veri setinin kalitesini artırmak adına etiketleme standardı maksimum hassasiyette tutulmuştur.
* **Eğitim Ortamı:** Lokal Donanım (Intel CPU / Entegre Grafik Birimi)
* **Veri Seti Yapısı:** Roboflow üzerinde işlenen 763 adet özgün ve el ile etiketlenmiş uydu görüntüsü.
* **Hiperparametreler:** `epochs=1`, `batch=16`, `imgsz=640`
* **Karşılaşılan Kısıtlamalar:** Yerel bilgisayardaki CUDA/GPU destek yetersizliği nedeniyle eğitim tamamen CPU üzerine yüklenmiş, işlem sürelerinin aşırı uzaması ve donanım darboğazı (thermal throttling) sebebiyle derin eğitim (high epoch) döngülerine geçilememiştir.

### Çözülen Teknik Zorluklar
* **Veri Yolu (Path) Senkronizasyonu:** Yerel ortamdaki `data.yaml` dosyasının klasör hiyerarşisi, kütüphane okuma hatalarını engellemek adına mutlak yollarla (absolute paths) optimize edilmiştir.
* **Baseline Çıktısı:** Modelin rastgele tahmin ağırlıklarından sıyrılması amacıyla 1 Epoch'luk ilk deneme başarıyla tamamlanmış, bulut tabanlı GPU geçişinin (Sprint 3) mühendislik gerekçesi ve baseline metrik taban çizgisi oluşturulmuştur.

## Sprint 3: Derin Eğitim ve Optimizasyon (09.06.2026)
Model yerel ortam kısıtlamalarından çıkarılarak **Google Colab (T4 GPU)** bulut platformuna taşınmıştır. 
Önerilen YOLOv8n mimarisi, özgün veri kümesindeki 3842 gemi nesnesi üzerinden **100 Epoch** boyunca derin eğitime tabi tutulmuştur.

* **Eğitim Süresi:** 0.622 saat (~37 dakika)
* **Precision (Kesinlik):** %68.4
* **Recall (Duyarlılık):** %50.6
* **mAP50 Başarı Skoru:** **%56.6** (Akademik baseline başarı esiği aşılmıştır)
* **Inference (Çıkarım Hızı):** Görsel başına **2.4 ms** ile gerçek zamanlı tespite hazır hale getirilmiştir.

Eğitilen en kararlı ağırlık dosyasına `outputs/weights/best.pt` konumundan, 100 Epoch'luk pürüzsüz loss ve başarı eğrilerine ise `outputs/results.png` üzerinden erişilebilir.
