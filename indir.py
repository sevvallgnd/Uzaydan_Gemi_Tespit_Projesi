import requests
import os
import time


API_KEY = 'AIzaSyAWXMx7GIwwQhnl2fC-oBNpG4ha0DyEXDQ'
SAVE_DIR = "Grid_VeriSeti_Bahamalar" 
os.makedirs(SAVE_DIR, exist_ok=True)


START_LAT, START_LON = 25.095, -77.400  
END_LAT, END_LON = 25.060, -77.300      


STEP = 0.0045 
ZOOM = 16 
MAX_IMAGES = 150 

count = 0 

def grid_download():
    global count
    lat = START_LAT
    print(f"Bahamalar Tropikal Tarama (Zoom: {ZOOM}) Başlatıldı...")
    
    while lat > END_LAT and count < MAX_IMAGES:
        current_lon = START_LON
        while current_lon < END_LON and count < MAX_IMAGES:
            url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{current_lon}&zoom={ZOOM}&size=640x640&maptype=satellite&key={API_KEY}"
            
            try:
                res = requests.get(url)
                if res.status_code == 200:
                    filename = f"bahamalar_{count}.jpg"
                    with open(os.path.join(SAVE_DIR, filename), "wb") as f:
                        f.write(res.content)
                    print(f"[{count+1}/{MAX_IMAGES}] İndirildi: {filename}")
                    count += 1
                else:
                    print(f"API Hatası ({res.status_code})")
                
                time.sleep(0.1) 
            except Exception as e:
                print(f"Bağlantı Hatası: {e}")
            
            current_lon += STEP 
        lat -= STEP 

grid_download()
print(f"\n--- 4. KONUM (BAHAMALAR) TAMAMLANDI ---")
