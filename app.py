import streamlit as st
from ultralytics import YOLO
from PIL import Image, ImageEnhance
import numpy as np
import cv2

# Sayfa Genişlik ve Tema Ayarları
st.set_page_config(page_title="Uzaydan Gemi Tespit Sistemi", layout="wide")

st.title("🛰️ Uzaydan Gemi Tespit Sistemi - Sprint 4 Paneli")
st.write("Roboflow 3x Veri Artırımı ve Fine-Tuning ile Optimize Edilmiş Derin Öğrenme Modeli")


st.sidebar.header("🛠️ Model Kontrol Paneli")

model_path = st.sidebar.text_input("Model Ağırlık Yolu (Ağırlık Dosyasının Adı)", "best.pt")

conf_threshold = st.sidebar.slider(
    "🎯 Confidence (Güven Eşiği) Ayarı", 
    min_value=0.05, 
    max_value=1.00, 
    value=0.25, 
    step=0.05,
    help="Modelin bir nesneye gemi demesi için gereken minimum emin olma oranı."
)


tta_active = st.sidebar.checkbox(
    "🧠 Test-Time Augmentation (TTA) Aktif Et", 
    value=False,
    help="Çıkarım anında görsele eş zamanlı filtre uygulayarak küçük nesne yakalama oranını artırır."
)


@st.cache_resource
def load_model(path):
    try:
        return YOLO(path)
    except Exception as e:
        st.error(f"Model yüklenirken hata oluştu! Klasörde '{path}' dosyasının olduğundan emin olun. Hata: {e}")
        return None

model = load_model(model_path)


uploaded_file = st.file_uploader("Lütfen analiz edilecek uydu görüntüsünü (.jpg, .jpeg, .png) yükleyin...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🖼️ Orijinal Uydu Görüntüsü")
        st.image(image, use_container_width=True)
        
    with col2:
        st.subheader("🔍 Yapay Zeka Analiz Çıktısı")
        
        if model is not None:
            if tta_active:
                enhancer = ImageEnhance.Contrast(image)
                processed_image = enhancer.enhance(1.3)  
            else:
                processed_image = image
                
            
            img_np = np.array(processed_image)
            results = model.predict(source=img_np, conf=conf_threshold, device='cpu')
            
            
            res_plotted = results[0].plot()
            st.image(res_plotted, channels="BGR", use_container_width=True)
            
           
            boxes = results[0].boxes
            detected_ships = len(boxes)
            
            if detected_ships > 0:
                st.success(f"✅ Analiz Başarılı: Bölgede toplam {detected_ships} adet gemi/tekne tespit edildi!")
            else:
                st.warning("⚠️ Bölgede herhangi bir gemi tespiti yapılamadı. Güven eşiğini düşürmeyi deneyebilirsiniz.")