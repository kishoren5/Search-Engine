import time
from typing import Any
from fastapi import APIRouter, HTTPException, Path

from search_engine.api.dependencies import get_global_index
from search_engine.api.schemas import (
    DocumentDetailResponse,
    IngestDocRequest,
    IngestDocResponse,
)

router = APIRouter(prefix="/v1", tags=["ingestion"])


@router.post("/ingest/document", response_model=IngestDocResponse)
def ingest_document(req: IngestDocRequest) -> IngestDocResponse:
    """Dynamically index a financial document in real time from the dashboard."""
    index = get_global_index()
    if not index:
        raise HTTPException(status_code=503, detail="Search index is not ready")

    t0 = time.perf_counter()

    doc_dict = {
        "title": req.title,
        "snippet": req.snippet,
        "url": f"https://compliance.bfsi.internal/records/{int(time.time())}",
        "metadata": {
            "doc_type": req.doc_type,
            "ticker": req.ticker,
            "risk_level": req.risk_level,
            "amount": req.amount,
            "jurisdiction": req.jurisdiction,
        },
    }

    if hasattr(index, "add_document_in_memory"):
        doc_id = index.add_document_in_memory(doc_dict)
    elif hasattr(index, "add_document"):
        # Fallback for InvertedIndex
        from search_engine.index.models import Document
        doc_id = f"DYN-{index.corpus_size + 1:06d}"
        doc = Document(
            doc_id=doc_id,
            title=req.title,
            body=req.snippet,
            metadata=doc_dict["metadata"],
        )
        index.add_document(doc)
    else:
        raise HTTPException(status_code=500, detail="Current index implementation does not support dynamic indexing")

    duration_ms = (time.perf_counter() - t0) * 1000.0

    return IngestDocResponse(
        doc_id=doc_id,
        status="INDEXED",
        tokens_indexed=doc_dict.get("length", 0),
        corpus_size_now=index.corpus_size,
        duration_ms=round(duration_ms, 2),
        message=f"Document {doc_id} successfully parsed, indexed, and available for zero-copy search.",
    )


@router.get("/document/{doc_id}", response_model=DocumentDetailResponse)
def get_document_details(
    doc_id: str = Path(..., description="Document identifier to inspect")
) -> DocumentDetailResponse:
    """Fetch complete raw document record and metadata for deep in-UI inspection."""
    index = get_global_index()
    if not index:
        raise HTTPException(status_code=503, detail="Search index is not ready")

    raw_doc = None
    if hasattr(index, "get_doc_metadata_by_id"):
        raw_doc = index.get_doc_metadata_by_id(doc_id)
    elif hasattr(index, "doc_metadata"):
        meta = index.doc_metadata.get(doc_id)
        if meta:
            raw_doc = {
                "doc_id": doc_id,
                "title": meta.title,
                "snippet": meta.snippet,
                "url": meta.url,
                "length": meta.length,
                "metadata": getattr(meta, "metadata", {}),
            }

    if not raw_doc:
        raise HTTPException(status_code=404, detail=f"Document '{doc_id}' not found in active index")

    return DocumentDetailResponse(
        doc_id=raw_doc.get("doc_id", doc_id),
        title=raw_doc.get("title", ""),
        snippet=raw_doc.get("snippet", ""),
        url=raw_doc.get("url", ""),
        length=raw_doc.get("length", 0),
        metadata=raw_doc.get("metadata", {}),
    )
