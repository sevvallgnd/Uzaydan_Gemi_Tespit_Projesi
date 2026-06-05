##  1. Veri Kümesinin Özgün Olarak Oluşturulması ve Metodolojisi

Bu projedeki veri kümesi hazır bir kaynaktan alınmamış; tamamen tarafımdan geliştirilen veri toplama mimarisi ile **özgün (custom)** olarak sıfırdan inşa edilmiştir.

### 🛰️ Veri Toplama Süreci ve Grid (Izgara) Tarama Sistemi
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
