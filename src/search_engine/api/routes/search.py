import time
from typing import Literal
from fastapi import APIRouter, HTTPException, Query

from search_engine.api.dependencies import get_global_index, get_global_retriever
from search_engine.api.schemas import LatencyWaterfall, SearchResponse, SearchResultItem
from search_engine.retrieval.tokenizer import tokenize

router = APIRouter(prefix="/v1", tags=["search"])


@router.get("/search", response_model=SearchResponse)
def search(
    q: str = Query(..., min_length=1, max_length=512, description="Search query string"),
    k: int = Query(10, ge=1, le=100, description="Number of results to return"),
    mode: Literal["lexical", "hybrid", "semantic"] = Query("lexical", description="Retrieval mode"),
    ticker: str | None = Query(None, description="Filter by banking ticker/institution (e.g. JPM, GS)"),
    risk_level: str | None = Query(None, description="Filter by compliance risk (CRITICAL, HIGH, MEDIUM, LOW)"),
    doc_type: str | None = Query(None, description="Filter by regulatory type (AML_SAR, SEC_FILING, SWIFT_TX)"),
    jurisdiction: str | None = Query(None, description="Filter by jurisdiction (US, EU, UK, CH, SG, HK)"),
    min_amount: float | None = Query(None, description="Filter by minimum transaction amount"),
    k1: float = Query(1.2, ge=0.1, le=3.0, description="BM25 term frequency saturation parameter k1"),
    b: float = Query(0.75, ge=0.0, le=1.0, description="BM25 length normalization parameter b"),
    explain: bool = Query(False, description="Include term-level score contribution breakdown"),
) -> SearchResponse:
    retriever = get_global_retriever()
    index = get_global_index()

    if index is None or retriever is None:
        raise HTTPException(status_code=503, detail="Search index is not currently loaded or ready")

    # Build structured filters
    filters: dict[str, str | float] = {}
    if ticker:
        filters["ticker"] = ticker
    if risk_level:
        filters["risk_level"] = risk_level
    if doc_type:
        filters["doc_type"] = doc_type
    if jurisdiction:
        filters["jurisdiction"] = jurisdiction
    if min_amount is not None:
        filters["min_amount"] = min_amount

    t0 = time.perf_counter()
    _ = tokenize(q)
    t1 = time.perf_counter()
    tokenize_ms = max((t1 - t0) * 1000.0, 0.01)

    hits = retriever.search(query=q, limit=k, filters=filters if filters else None, k1=k1, b=b)
    t2 = time.perf_counter()
    retrieval_ms = max((t2 - t1) * 1000.0, 0.01)

    explained_hits = []
    hits_map = {}
    if explain and hasattr(retriever, "search_explained"):
        explained_hits = retriever.search_explained(
            query=q, limit=k, filters=filters if filters else None, k1=k1, b=b
        )
        hits_map = {item["doc_id"]: item for item in explained_hits}
    t3 = time.perf_counter()
    explain_ms = max((t3 - t2) * 1000.0, 0.0)

    results: list[SearchResultItem] = []
    for hit in hits:
        title, url, snippet = "", "", ""
        meta_dict: dict = {}

        if hasattr(index, "doc_metadata"):
            doc_meta = index.doc_metadata.get(hit.doc_id)
            if doc_meta:
                title, url, snippet = doc_meta.title, doc_meta.url, doc_meta.snippet
        elif hasattr(index, "get_doc_metadata_by_id"):
            raw_doc = index.get_doc_metadata_by_id(hit.doc_id)
            if raw_doc:
                title = raw_doc.get("title", "")
                url = raw_doc.get("url", "")
                snippet = raw_doc.get("snippet", "")
                meta_dict = raw_doc.get("metadata", {})

        expl = hits_map.get(hit.doc_id, {}).get("breakdown") if explain else None

        results.append(
            SearchResultItem(
                doc_id=hit.doc_id,
                title=title,
                url=url,
                snippet=snippet,
                score=round(hit.score, 4),
                rank=hit.rank,
                ticker=meta_dict.get("ticker"),
                risk_level=meta_dict.get("risk_level"),
                doc_type=meta_dict.get("doc_type"),
                amount=meta_dict.get("amount"),
                jurisdiction=meta_dict.get("jurisdiction"),
                explanation=expl,
            )
        )

    t4 = time.perf_counter()
    hydration_ms = max((t4 - t3) * 1000.0, 0.01)
    duration_ms = (t4 - t0) * 1000.0

    waterfall = LatencyWaterfall(
        tokenize_ms=round(tokenize_ms, 3),
        retrieval_ms=round(retrieval_ms, 3),
        explain_ms=round(explain_ms, 3),
        hydration_ms=round(hydration_ms, 3),
        total_ms=round(duration_ms, 3),
    )

    return SearchResponse(
        query=q,
        mode=mode,
        results=results,
        took_ms=round(duration_ms, 3),
        index_version="v1.0-fintech-mmap",
        partial=False,
        total_hits=len(results),
        k1=k1,
        b=b,
        waterfall=waterfall,
    )
