from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, DateTime, JSON, ForeignKey, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    source_type: Mapped[str] = mapped_column(String(50))  # PDF, URL, etc.
    source_url: Mapped[Optional[str]] = mapped_column(String(500))
    author: Mapped[Optional[str]] = mapped_column(String(100))
    version: Mapped[Optional[str]] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)

    chunks: Mapped[List["ChunkMetadata"]] = relationship("ChunkMetadata", back_populates="document")

class ChunkMetadata(Base):
    __tablename__ = "chunk_metadata"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    vector_id: Mapped[str] = mapped_column(String(100))  # ID in Qdrant
    content_hash: Mapped[str] = mapped_column(String(64))
    chunk_index: Mapped[int] = mapped_column()
    page_number: Mapped[Optional[int]] = mapped_column()
    
    document: Mapped["Document"] = relationship("Document", back_populates="chunks")

class QueryLog(Base):
    __tablename__ = "query_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    query: Mapped[str] = mapped_column(String(1000))
    answer: Mapped[str] = mapped_column(JSON)
    confidence_score: Mapped[float] = mapped_column(Float)
    is_blocked: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class ConflictReport(Base):
    __tablename__ = "conflict_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    query_id: Mapped[Optional[int]] = mapped_column(ForeignKey("query_logs.id"))
    conflict_type: Mapped[str] = mapped_column(String(50))  # Temporal, Statement
    description: Mapped[str] = mapped_column(String(1000))
    affected_chunks: Mapped[list] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
