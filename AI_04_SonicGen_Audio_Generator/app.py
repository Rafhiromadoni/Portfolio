import gradio as gr
from transformers import pipeline
import scipy.io.wavfile
import numpy as np

# 1. LOAD MODEL MUSICGEN
# Kita menggunakan versi 'small' agar cepat & ringan di Free Tier Hugging Face
print("Sedang memuat model MusicGen...")
synthesiser = pipeline("text-to-audio", model="facebook/musicgen-small")

def generate_music(text, duration):
    if not text:
        return None
    
    print(f"🎵 Membuat musik: '{text}' selama {duration} detik...")
    
    # Generate audio
    # forward_params max_new_tokens mengatur durasi (kurang lebih 1 token ≈ 0.02 detik)
    # 256 token ≈ 5 detik, 512 ≈ 10 detik
    # Kita buat dinamis berdasarkan input user
    max_tokens = int(duration * 50) 
    
    music = synthesiser(text, forward_params={"max_new_tokens": max_tokens})
    
    # Konversi output ke format yang bisa diputar Gradio
    audio_data = music["audio"]
    sampling_rate = music["sampling_rate"]
    
    # Normalisasi audio agar suaranya jelas
    audio_data = audio_data / np.max(np.abs(audio_data))
    
    return (sampling_rate, audio_data.T)

# 2. ANTARMUKA GRADIO
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    <h1 style='text-align: center;'>🎵 SonicGen: AI Music Creator</h1>
    <p style='text-align: center;'>Jadilah komposer musik instan! Ketik deskripsi musik yang Anda inginkan, dan AI akan menciptakannya untuk Anda.</p>
    """)
    
    with gr.Row():
        with gr.Column():
            inp_text = gr.Textbox(
                label="🎹 Deskripsi Musik (Prompt)", 
                placeholder="Contoh: 80s pop track with synth drums and nostalgic melody",
                lines=2
            )
            inp_duration = gr.Slider(minimum=5, maximum=15, value=10, step=1, label="⏱️ Durasi (Detik)")
            btn = gr.Button("✨ Ciptakan Musik", variant="primary")
            
        with gr.Column():
            out_audio = gr.Audio(label="🎧 Hasil Generasi AI", type="numpy")
            
    # Contoh prompt agar user bisa langsung mencoba
    gr.Examples(
        examples=[
            ["A dynamic soundtrack for an epic space battle", 10],
            ["Lo-fi hip hop beat perfect for studying and relaxing", 10],
            ["Acoustic guitar melody with birds chirping in background", 10]
        ],
        inputs=[inp_text, inp_duration]
    )

    btn.click(fn=generate_music, inputs=[inp_text, inp_duration], outputs=out_audio)

if __name__ == "__main__":
    demo.launch()