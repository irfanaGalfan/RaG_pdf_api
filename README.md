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
