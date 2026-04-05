import os
import gradio as gr
from huggingface_hub import InferenceClient
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# 1. SETUP AKSES & MODEL
hf_token = os.environ.get("HF_TOKEN")
if not hf_token:
    raise ValueError("HF_TOKEN tidak ditemukan! Pastikan Anda sudah menambahkannya di Settings -> Secrets.")

print("Memuat Model AI...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

llm_client = InferenceClient(
    model="Qwen/Qwen2.5-7B-Instruct",
    token=hf_token
)

vector_db_global = None

# 2. FUNGSI MULTI-FILE INGESTION
def process_file(uploaded_file):
    global vector_db_global
    if uploaded_file is None:
        return "⚠️ Silakan unggah file terlebih dahulu."

    file_path = uploaded_file.name
    file_ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif file_ext == ".txt":
            loader = TextLoader(file_path)
        elif file_ext == ".docx":
            loader = Docx2txtLoader(file_path)
        elif file_ext == ".csv":
            loader = CSVLoader(file_path)
        else:
            return f"❌ Format {file_ext} belum didukung. Gunakan PDF, TXT, DOCX, atau CSV."

        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_documents(documents)
        
        vector_db_global = Chroma.from_documents(documents=texts, embedding=embeddings)
        return f"✅ File {file_ext.upper()} berhasil dipelajari! NexusAI siap digunakan."
    except Exception as e:
        return f"❌ Gagal memproses file: {str(e)}"

# 3. FUNGSI TAB 1: CHATBOT
def chat_nexus(message, history):
    global vector_db_global
    if vector_db_global is None:
        return "⚠️ Tolong unggah dan proses dokumen di panel sebelah kiri terlebih dahulu."
    try:
        docs = vector_db_global.similarity_search(message, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
        prompt = f"Anda adalah asisten AI perusahaan. Gunakan konteks dokumen berikut untuk menjawab pertanyaan.\n\nKonteks Dokumen:\n{context}\n\nPertanyaan: {message}\nJawaban:"
        
        messages = [{"role": "user", "content": prompt}]
        response = llm_client.chat_completion(messages=messages, max_tokens=1024)
        return response.choices[0].message.content
    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}"

# 4. FUNGSI TAB 2: DOCUMENT GENERATOR
def generate_document(prompt_type, custom_prompt):
    global vector_db_global
    
    if prompt_type == "Draf Email Internal":
        instruction = f"Tuliskan draf email internal perusahaan yang profesional berdasarkan instruksi berikut: {custom_prompt}"
    elif prompt_type == "Ringkasan Eksekutif":
        instruction = f"Buat ringkasan eksekutif (Executive Summary) yang formal dari instruksi berikut: {custom_prompt}"
    elif prompt_type == "Kerangka Proposal":
        instruction = f"Buat kerangka struktur proposal bisnis lengkap berdasarkan topik: {custom_prompt}"
    else:
        instruction = custom_prompt
    
    try:
        if vector_db_global is not None:
            docs = vector_db_global.similarity_search(instruction, k=4)
            context = "\n\n".join([doc.page_content for doc in docs])
            full_prompt = f"Berdasarkan informasi dari dokumen internal berikut:\n{context}\n\nLakukan tugas ini: {instruction}"
            
            messages = [{"role": "user", "content": full_prompt}]
            response = llm_client.chat_completion(messages=messages, max_tokens=1024)
            return response.choices[0].message.content
        else:
            messages = [{"role": "user", "content": instruction}]
            response = llm_client.chat_completion(messages=messages, max_tokens=1024)
            return response.choices[0].message.content
    except Exception as e:
        return f"Gagal membuat dokumen: {str(e)}"

# 5. ANTARMUKA GRADIO
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>🧠 NexusAI: Enterprise Knowledge & Generator Agent</h1>")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📂 Input Knowledge Base")
            file_input = gr.File(label="Unggah Dokumen (PDF, DOCX, TXT, CSV)")
            process_btn = gr.Button("🧠 Pelajari Dokumen", variant="primary")
            status_text = gr.Textbox(label="Status Sistem", interactive=False)
            process_btn.click(fn=process_file, inputs=file_input, outputs=status_text)
            
            gr.Markdown("""
            ---
            **Cara Penggunaan:**
            1. Unggah dokumen.
            2. Klik **Pelajari Dokumen**.
            3. Gunakan **Tab 1** untuk bertanya (Analisis).
            4. Gunakan **Tab 2** untuk menyuruh AI membuat draf dokumen baru.
            """)
            
        with gr.Column(scale=2):
            with gr.Tab("💬 Tab 1: Analisis & QnA (Baca)"):
                gr.Markdown("Tanyakan wawasan spesifik dari dokumen yang baru saja Anda unggah.")
                
                chatbot = gr.Chatbot(height=350) 
                msg = gr.Textbox(label="Pertanyaan Anda:", placeholder="Contoh: Apa kesimpulan utama dari laporan ini?")
                clear_chat = gr.Button("🗑️ Bersihkan Chat")
                
                def respond(user_message, chat_history):
                    bot_message = chat_nexus(user_message, chat_history)
                    chat_history.append({"role": "user", "content": user_message})
                    chat_history.append({"role": "assistant", "content": bot_message})
                    return "", chat_history
                
                msg.submit(respond, [msg, chatbot], [msg, chatbot])
                clear_chat.click(lambda: None, None, chatbot, queue=False)

            with gr.Tab("📝 Tab 2: Document Generator (Buat)"):
                gr.Markdown("Perintahkan AI untuk membuat dokumen baru yang bersumber dari dokumen Anda.")
                doc_type = gr.Dropdown(["Draf Email Internal", "Ringkasan Eksekutif", "Kerangka Proposal", "Bebas (Custom)"], label="Jenis Dokumen", value="Draf Email Internal")
                doc_instruction = gr.Textbox(label="Instruksi Tambahan", lines=3)
                generate_btn = gr.Button("✨ Generate Dokumen", variant="primary")
                doc_output = gr.Textbox(label="Hasil Dokumen Baru", lines=10, interactive=True)
                
                generate_btn.click(fn=generate_document, inputs=[doc_type, doc_instruction], outputs=doc_output)

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())