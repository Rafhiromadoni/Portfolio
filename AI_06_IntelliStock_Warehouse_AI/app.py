import gradio as gr
from ultralytics import YOLO
import pandas as pd
import datetime
import os

# 1. LOAD MODEL
model = YOLO('yolov8n.pt') 

# 2. KONFIGURASI DATABASE (CSV)
DB_FILE = 'inventory_log.csv'

def save_to_database(df_results):
    # Cek apakah file sudah ada, jika belum buat header-nya
    file_exists = os.path.isfile(DB_FILE)
    
    # Tambahkan kolom Timestamp untuk pencatatan waktu
    df_results['Timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Simpan ke CSV (mode append)
    df_results.to_csv(DB_FILE, mode='a', index=False, header=not file_exists)
    return f"✅ Data berhasil disimpan ke {DB_FILE}"

def process_inventory(img):
    if img is None:
        return None, None, "### ⚠️ Silakan unggah foto."

    # 3. DETEKSI
    results = model(img)
    res_plotted = results[0].plot()
    
    # 4. HITUNG STOK
    detections = results[0].boxes.cls.tolist()
    names = model.names
    counts = {}
    for class_id in detections:
        name = names[int(class_id)]
        counts[name] = counts.get(name, 0) + 1
    
    # 5. DATA PREPARATION
    inventory_data = []
    if counts:
        for item, count in counts.items():
            status = "✅ AMAN" if count >= 5 else "🚨 LOW STOCK"
            inventory_data.append([item.upper(), count, status])
    
    df_inventory = pd.DataFrame(inventory_data, columns=["Nama Barang", "Jumlah", "Status"])
    
    # 6. AUTO-SAVE KE DATABASE
    if not df_inventory.empty:
        db_status = save_to_database(df_inventory)
    else:
        db_status = "ℹ️ Tidak ada data untuk disimpan."
        
    return res_plotted, df_inventory, db_status

# 7. UI GRADIO
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("<h1 style='text-align: center;'>🏙️ IntelliStock AI + Database</h1>")
    
    with gr.Row():
        with gr.Column():
            input_img = gr.Image(type="numpy", label="Scan Barcode/Rak")
            btn = gr.Button("🔍 Jalankan Scan & Update Database", variant="primary")
            
        with gr.Column():
            output_img = gr.Image(label="Visual Detection")
            db_msg = gr.Markdown() # Menampilkan status penyimpanan
            output_table = gr.Dataframe(label="Laporan Inventaris")

    btn.click(fn=process_inventory, inputs=input_img, outputs=[output_img, output_table, db_msg])

if __name__ == "__main__":
    demo.launch()