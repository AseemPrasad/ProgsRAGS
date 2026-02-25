import os
from qdrant_client import QdrantClient
from qdrant_client.http import models

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "knowledge_chunks"

class VectorStore:
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL)
        self._ensure_collection()

    def _ensure_collection(self):
        try:
            self.client.get_collection(COLLECTION_NAME)
        except Exception:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
            )

    def upsert_chunks(self, ids, vectors, payloads):
        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=models.Batch(
                ids=ids,
                vectors=vectors,
                payloads=payloads
            )
        )

    def search(self, vector, limit=10, score_threshold=0.7):
        return self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=limit,
            score_threshold=score_threshold,
            with_payload=True
        )

vector_store = VectorStore()
