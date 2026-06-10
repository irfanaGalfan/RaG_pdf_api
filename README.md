# RaG_pdf_api
# 📄 Free Local PDF Chat Engine (RAG Pipeline)

A completely secure, private, and 100% local Retrieval-Augmented Generation (RAG) system that allows you to upload documents (like resumes or certificates) and ask complex questions about them. 

This application processes documents line-by-line, converts them into high-dimensional vector embeddings, stores them inside an embedded database, and passes relevant context chunks to **Llama 3** for ultra-fast, intelligent question answering.

---

## 🛠️ The Tech Stack

* **Frontend:** Streamlit (Clean, reactive chat workspace)
* **Backend API:** FastAPI / Uvicorn (High-performance backend routing)
* **Vector Database:** Qdrant Client (Embedded storage engine)
* **LLM Framework:** LangChain & `langchain-ollama`
* **Local AI Models:** * `llama3` (Text generation brain)
    * `nomic-embed-text` (High-accuracy document text embedding)

---

## 📐 Architecture & Data Flow

1. **Document Upload:** The user drops a PDF into the Streamlit interface.
2. **Text Parsing & Chunking:** FastAPI extracts text line-by-line using `pypdf` and groups sentences into concise, clean contextual windows.
3. **Vector Generation:** Text chunks are vectorized using Ollama's local `nomic-embed-text` model.
4. **Vector Storage:** Embeddings are written straight to a local embedded `qdrant_db` workspace folder.
5. **Contextual Querying:** When a chat query is submitted, the system searches the database for the top matching context blocks, inserts them into an optimized prompt boundary, and passes them to Llama 3 for instant generation.

---

## 🚀 How to Run the Project Locally

### 1. Prerequisites
Ensure you have **Ollama** installed on your machine and have pulled the required models:
```cmd

ollama pull llama3
ollama pull nomic-embed-text
2. Installation
Open your terminal inside the project directory and install the required Python dependencies:

DOS
pip install fastapi uvicorn streamlit qdrant-client langchain-ollama pypdf pydantic
3. Start the Backend API
Run the high-performance FastAPI server. Note: We run without the --reload flag to cleanly prevent Windows multiprocessing file-locking race conditions on the local database folder.

DOS
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
4. Start the Streamlit User Interface
Open a separate terminal window and launch your browser control panel dashboard:

DOS
python -m streamlit run src/app.py
Open your browser to http://localhost:8501, upload your file, hit Process, and begin chatting!

🔒 Privacy & Security Guardrails
Because this entire ecosystem runs on your physical machine, zero bytes of data leave your computer. No external cloud APIs are called, making it perfectly safe for analyzing highly confidential personal data, company resumes, or financial document profiles.
