# 🏙️ IntelliStock AI: End-to-End Warehouse Intelligence

Proyek ini adalah sistem manajemen inventaris cerdas yang menggabungkan **Computer Vision** untuk deteksi stok otomatis dan **Time-Series Analysis** untuk prediksi kebutuhan barang (*Demand Forecasting*).

🚀 **[KLIK DI SINI UNTUK DEMO LIVE] (https://huggingface.co/spaces/rafhiromadoni/IntelliStock-AI)**

## 📌 Fitur Utama
* **AI Visual Scan:** Menggunakan arsitektur **YOLOv8** untuk mendeteksi dan menghitung jumlah stok barang dari input gambar secara real-time.
* **Automated Database:** Sistem otomatis mencatat hasil pemindaian ke dalam basis data CSV dengan stempel waktu (*timestamp*) untuk audit trail.
* **Demand Forecasting:** Menggunakan algoritma **Linear Regression** untuk menganalisis tren penggunaan stok dan memprediksi sisa hari sebelum barang habis (*Out-of-Stock prediction*).
* **Inventory Dashboard:** Antarmuka interaktif yang menyajikan data dalam bentuk tabel status (Aman/Low Stock) dan grafik tren stok.

## 🛠️ Tech Stack
* **Model:** YOLOv8 (Ultralytics)
* **Analytics:** Pandas, NumPy, Matplotlib
* **Interface:** Gradio
* **Deployment:** Hugging Face Spaces

## 📂 Alur Kerja Sistem
1. **Input:** User mengunggah foto rak/gudang.
2. **Process:** AI mendeteksi objek dan menghitung jumlah per kategori.
3. **Storage:** Data disimpan ke `inventory_log.csv`.
4. **Analysis:** Sistem memetakan data histori ke grafik untuk memprediksi masa depan stok.
