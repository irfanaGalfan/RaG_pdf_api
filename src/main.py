from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
# ✅ Import the modern class to fix the warning
from langchain_ollama import OllamaLLM 
from pypdf import PdfReader
from src.database import add_documents_to_vector_db, search_similar_documents, qdrant_client, COLLECTION_NAME, VectorParams, Distance
import io

app = FastAPI(title="100% Free Local AI Engine")

# ✅ Upgraded brain initialization
llm = OllamaLLM(model="llama3", temperature=0, num_predict=100)

class QueryInput(BaseModel):
    question: str

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        pdf_file = io.BytesIO(contents)
        reader = PdfReader(pdf_file)
        
        paragraphs = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                # Clean lines up nicely
                lines = [line.strip() for line in text.split("\n") if line.strip()]
                # Standard paragraph chunks (no heavy overlapping to keep database size light)
                for i in range(0, len(lines), 3):
                    chunk = " ".join(lines[i:i+3])
                    paragraphs.append(chunk)
        
        if not paragraphs:
            return {"status": "error", "message": "No readable text found in PDF."}
            
        # Clear database memory
        qdrant_client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
        
        add_documents_to_vector_db(paragraphs)
        return {
            "status": "success", 
            "message": f"Successfully processed '{file.filename}'. Ingested {len(paragraphs)} text blocks."
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/chat")
def chat_with_local_ai(data: QueryInput):
    # ⚡ OPTIMIZED: Changed limit to 3. Enough to find links, light enough to run instantly!
    context_chunks = search_similar_documents(data.question, limit=3)
    context_text = "\n".join(context_chunks)
    
    # Shortened prompt layout so Llama doesn't overthink
    prompt = f"""
    Answer the question briefly using the context below. Look for URLs/links if asked.
    If not found, say you don't know.

    Context:
    {context_text}

    Question: {data.question}
    Answer:
    """
    
    response = llm.invoke(prompt)
    return {"response": response, "source_used": context_chunks}
