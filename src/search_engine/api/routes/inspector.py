from pathlib import Path
from typing import Any
from fastapi import APIRouter, HTTPException, Query

from search_engine.api.dependencies import get_global_index
from search_engine.index.manifest import verify_manifest
from search_engine.index.mmap_store import MMapIndexReader

try:
    import psutil
except ImportError:
    psutil = None

router = APIRouter(prefix="/v1/inspect", tags=["inspect"])


@router.get("/stats")
def get_system_stats() -> dict[str, Any]:
    index = get_global_index()
    if not index:
        return {"status": "unloaded", "corpus_size": 0}

    is_mmap = isinstance(index, MMapIndexReader)
    manifest_info = {}
    manifest_valid = False
    files_info = []

    if is_mmap:
        seg_dir = index.segment_dir
        manifest_path = seg_dir / "manifest.json"
        manifest_valid = verify_manifest(manifest_path)
        manifest_info = index.manifest

        for f in seg_dir.glob("*"):
            if f.is_file():
                files_info.append({
                    "name": f.name,
                    "size_bytes": f.stat().st_size,
                    "size_mb": round(f.stat().st_size / (1024 * 1024), 2),
                })

    rss_mb = psutil.Process().memory_info().rss / (1024 * 1024) if psutil else 0.0

    return {
        "status": "ready",
        "index_type": "MMapIndexReader (Zero-Copy)" if is_mmap else "InvertedIndex",
        "corpus_size": index.corpus_size,
        "total_terms": index.total_terms,
        "avg_doc_length": round(index.average_document_length, 2),
        "manifest_valid": manifest_valid,
        "rss_memory_mb": round(rss_mb, 1),
        "files": files_info,
        "manifest": manifest_info,
    }


@router.get("/term")
def inspect_term(term: str = Query(..., min_length=1)) -> dict[str, Any]:
    index = get_global_index()
    if not index:
        raise HTTPException(status_code=503, detail="Index not loaded")

    clean_term = term.strip().lower()
    df = index.get_document_frequency(clean_term)

    lexicon_entry = {}
    if isinstance(index, MMapIndexReader):
        lexicon_entry = index.lexicon.get(clean_term, {})

    sample_postings = []
    if df > 0:
        doc_ids, tfs = index.get_postings(clean_term)
        for i in range(min(10, len(doc_ids))):
            d_id = doc_ids[i]
            # resolve doc_id string if available
            doc_str = ""
            if hasattr(index, "documents") and d_id < len(index.documents):
                doc_str = index.documents[d_id].get("doc_id", "")
            sample_postings.append({
                "int_doc_id": d_id,
                "doc_id": doc_str or f"doc_{d_id}",
                "term_frequency": tfs[i],
            })

    return {
        "term": clean_term,
        "document_frequency": df,
        "lexicon_entry": lexicon_entry,
        "in_lexicon": df > 0,
        "sample_postings": sample_postings,
    }
