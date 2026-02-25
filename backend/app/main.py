from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db import get_db, init_db
from backend.app.services.ingestion import ingestion_service
from backend.app.services.vector_store import vector_store
from backend.app.services.trust_gate import trust_gate
from backend.app.services.reasoning import reasoning_service
from backend.app.models.metadata import Document, ChunkMetadata
import uuid
import os

app = FastAPI(title="Trust-Aware Knowledge Platform API")

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.post("/ingest/pdf")
async def ingest_pdf(
    title: str, 
    author: str = None, 
    version: str = None, 
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # Save file temporarily
    temp_path = f"temp_{uuid.uuid4()}.pdf"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        chunks = await ingestion_service.process_pdf(temp_path, title, author, version)
        
        # Create Document entry
        doc = Document(
            title=title,
            source_type="PDF",
            author=author,
            version=version
        )
        db.add(doc)
        await db.flush()

        # Prep for VDB and metadata
        v_ids = []
        v_vectors = []
        v_payloads = []

        for i, chunk in enumerate(chunks):
            v_id = str(uuid.uuid4())
            payload = {
                "document_id": doc.id,
                "title": title,
                "content": chunk["content"],
                "page": chunk["page"],
                "created_at": doc.created_at.isoformat()
            }
            # Mock embedding (1536 dims)
            vector = [0.1] * 1536 
            
            v_ids.append(v_id)
            v_vectors.append(vector)
            v_payloads.append(payload)

            chunk_meta = ChunkMetadata(
                document_id=doc.id,
                vector_id=v_id,
                content_hash="hash",
                chunk_index=i,
                page_number=chunk["page"]
            )
            db.add(chunk_meta)

        vector_store.upsert_chunks(v_ids, v_vectors, v_payloads)
        await db.commit()
        
        return {"document_id": doc.id, "chunks_ingested": len(chunks)}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/query")
async def query_knowledge(q: str):
    # 1. Embed query (Mock)
    query_vector = [0.1] * 1536
    
    # 2. Retrieve
    retrieved = vector_store.search(query_vector)
    
    # 3. Trust Gate
    scored_chunks, conflicts = trust_gate.evaluate_retrieval(retrieved)
    
    # 4. Generate Answer
    result = await reasoning_service.generate_answer(q, scored_chunks, conflicts)
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
