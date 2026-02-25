import hashlib
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.app.services.vector_store import vector_store
from backend.app.models.metadata import Document, ChunkMetadata
import uuid

class IngestionService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "\n", " ", ""]
        )

    async def process_pdf(self, file_path: str, title: str, author: str = None, version: str = None):
        reader = PdfReader(file_path)
        chunks = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if not text:
                continue
            
            page_chunks = self.text_splitter.split_text(text)
            for j, content in enumerate(page_chunks):
                chunks.append({
                    "content": content,
                    "page": i + 1,
                    "index": j
                })

        # Generate embeddings (Mock for now, will integrate OpenAI)
        # In real implementation, batch generate embeddings
        
        # Save to metadata DB and Vector Store
        # This will be called from a FastAPI endpoint with DB session
        return chunks

ingestion_service = IngestionService()
