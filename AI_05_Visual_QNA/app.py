import gradio as gr
from transformers import pipeline

# 1. LOAD MULTIMODAL MODEL (Visual Question Answering)
print("Sedang memuat model Multimodal ViLT...")
# Model ini secara spesifik dilatih untuk menjawab pertanyaan bahasa Inggris dari sebuah gambar
vqa_pipeline = pipeline("visual-question-answering", model="dandelin/vilt-b32-finetuned-vqa")

def answer_question(image, question):
    if image is None or not question.strip():
        return "⚠️ Mohon masukkan gambar dan ketik pertanyaannya terlebih dahulu."
    
    try:
        # AI memproses gambar dan teks (pertanyaan) secara bersamaan
        result = vqa_pipeline(image=image, question=question)
        
        # Ambil jawaban dengan probabilitas tertinggi
        top_answer = result[0]['answer']
        score = round(result[0]['score'] * 100, 1)
        
        return f"### 🤖 Jawaban AI: **{top_answer.capitalize()}**\n_Tingkat Keyakinan: {score}%_"
    except Exception as e:
        return f"⚠️ Terjadi kesalahan saat memproses: {str(e)}"

# 2. MEMBUAT ANTARMUKA GRADIO
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    <h1 style='text-align: center;'>👁️‍🗨️ VisionQuery: Multimodal AI</h1>
    <p style='text-align: center;'>Sistem cerdas perpaduan <b>Computer Vision</b> dan <b>NLP</b>. Unggah gambar dan tanyakan apa saja tentang isi gambar tersebut!</p>
    """)
    
    with gr.Row():
        with gr.Column():
            inp_img = gr.Image(type="pil", label="📂 Upload Gambar Bebas")
            # Catatan: Karena model pre-trained dasar ini berbahasa Inggris, kita arahkan user pakai bahasa Inggris
            inp_text = gr.Textbox(label="❓ Pertanyaan (Gunakan Bahasa Inggris)", placeholder="Contoh: What color is the car? / How many people are there?")
            btn = gr.Button("🧠 Analisis Gambar & Teks", variant="primary")
            
        with gr.Column():
            out_text = gr.Markdown(label="Hasil Analisis")
            
    # Menghubungkan tombol
    btn.click(fn=answer_question, inputs=[inp_img, inp_text], outputs=out_text)
    
    # Menambahkan contoh agar tampilan lebih profesional
    gr.Markdown("""
    ---
    **💡 Cara Kerja (Arsitektur Early/Late Fusion):**
    Aplikasi ini menggunakan model *Transformer* yang menerima dua jenis input berbeda (Piksel Gambar dan Token Teks). AI mengekstraksi fitur dari keduanya, menggabungkannya, dan mengklasifikasikan jawaban yang paling tepat berdasarkan konteks visual.
    """)

if __name__ == "__main__":
    demo.launch()