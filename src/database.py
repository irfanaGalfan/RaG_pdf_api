from langchain_ollama import OllamaEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

COLLECTION_NAME = "local_knowledge"
qdrant_client = QdrantClient(path="qdrant_db")

embeddings_model = OllamaEmbeddings(model="nomic-embed-text")

def init_collection():
    """Ensures the collection exists with the correct dimensions."""
    try:
        # Check if it exists
        qdrant_client.get_collection(collection_name=COLLECTION_NAME)
    except Exception:
        # If it doesn't exist (because we deleted the folder), create it fresh
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )

# Initialize it immediately on startup
init_collection()

def add_documents_to_vector_db(texts: list[str]):
    init_collection()  # Double check setup
    vectors = embeddings_model.embed_documents(texts)
    points = [
        PointStruct(id=str(uuid.uuid4()), vector=vectors[i], payload={"text": text})
        for i, text in enumerate(texts)
    ]
    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points)

def search_similar_documents(query: str, limit: int = 2):
    init_collection()  # Double check setup
    query_vector = embeddings_model.embed_query(query)
    search_results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit
    )
    return [point.payload["text"] for point in search_results.points if point.payload]
