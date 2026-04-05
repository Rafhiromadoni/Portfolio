# 🧠 NexusAI: Enterprise Knowledge & Document Generator Agent

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-Enterprise-green)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Qwen_2.5-yellow)
![Gradio](https://img.shields.io/badge/Gradio-UI-orange)

NexusAI adalah purwarupa asisten cerdas berbasis **Retrieval-Augmented Generation (RAG)** yang dirancang untuk kebutuhan korporat. Aplikasi ini mendemonstrasikan bagaimana Large Language Models (LLM) dapat menghemat ratusan jam kerja dengan membaca dokumen internal dan menghasilkan ringkasan atau draf bisnis baru secara instan tanpa halusinasi.

##  Business Value & Fitur Utama
* **Multi-Format Data Ingestion:** Mampu mengekstrak konteks dari file `.pdf`, `.docx`, `.txt`, dan `.csv` secara dinamis.
* **Context-Aware QnA (Tab 1):** Sistem QA cerdas dengan Vector Database (Chroma) yang mencari informasi paling relevan dari dokumen perusahaan.
* **Automated Document Generator (Tab 2):** Perintah *one-click* untuk menyusun draf dokumen bisnis (Email Internal, Executive Summary, Kerangka Proposal) berdasarkan data yang diunggah.

##  Arsitektur & Tech Stack
* **LLM Engine:** `Qwen/Qwen2.5-7B-Instruct` (Melalui Inference API)
* **Embedding Model:** `all-MiniLM-L6-v2` (Sentence Transformers)
* **Orchestration:** LangChain (Custom Manual RAG Implementation)
* **Vector Database:** ChromaDB (In-memory)
* **Frontend:** Gradio 6.0

##  Engineering Insights
Proyek ini dibangun dengan fokus pada **stabilitas (reliability)** dan **skalabilitas**. 
Daripada bergantung sepenuhnya pada fungsi *black-box* seperti `langchain.chains` yang rentan terhadap konflik dependensi server (*Dependency Hell*), saya membangun logika *retrieval* dan *prompt engineering* secara manual. Selain itu, sistem komunikasi API telah dioptimalkan ke format *conversational* terbaru untuk memastikan kompatibilitas 100% dengan infrastruktur *cloud* Hugging Face.
