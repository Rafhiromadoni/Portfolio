# 👁️‍🗨️ Visual Q&A: Multimodal AI Assistant

Proyek ini adalah demonstrasi **Direct Deployment** untuk model *Multimodal Artificial Intelligence*. Aplikasi ini tidak melalui proses *training* di *notebook* lokal, melainkan langsung diimplementasikan sebagai layanan *web* menggunakan skrip Python.

🚀 **[KLIK DI SINI UNTUK MENCOBA APLIKASI SECARA LIVE] (https://huggingface.co/spaces/rafhiromadoni/MultimodalVisualQnA)**

## 📌 Deskripsi Proyek
Aplikasi Visual Question Answering (VQA) ini mengizinkan pengguna untuk mengunggah sebuah gambar dan mengajukan pertanyaan berbasis teks terkait gambar tersebut. Model Multimodal di belakang layar akan menganalisis piksel gambar sekaligus memahami konteks pertanyaan untuk memberikan jawaban yang akurat secara *real-time*.

## 📂 Struktur Folder
* `app.py`: Skrip utama yang berisi inisialisasi model *Vision-Language* dan antarmuka antarmuka interaktif.
* `requirements.txt`: Daftar dependensi pustaka (*library*) yang dibutuhkan oleh *server* (seperti `transformers`, `torch`, `Pillow`).

## 💡 Tech Stack & Arsitektur
* **Framework:** Python, Gradio, Hugging Face `transformers`
* **Arsitektur:** Multimodal (Vision & Language Model)
* **Computer Vision:** Memproses dan mengekstraksi fitur dari gambar (menggunakan library `Pillow`).
* **NLP:** Memproses teks pertanyaan dan melakukan generasi teks jawaban.

## 📸 Pratinjau Aplikasi

