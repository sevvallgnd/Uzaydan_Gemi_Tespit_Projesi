import os
from ultralytics import YOLO

def main():
    
    model = YOLO("yolov8n.pt")
    
   
    results = model.train(
        data=os.path.join(os.getcwd(), "Uzaydan_Gemi_Tespit_Sistemi-1", "data.yaml"), 
        epochs=1,           
        imgsz=512,          
        batch=8,           
        device="cpu",       
        optimizer="SGD",    
        fraction=0.8,       
        seed=42,            
        project="Gemi_Projesi_Runs",
        name="sprint2_baseline_yolov8"
    )
    
    print("=== SPRINT 2 BASELINE EĞİTİMİ BAŞARIYLA TAMAMLANDI ===")

if __name__ == "__main__":
    main()