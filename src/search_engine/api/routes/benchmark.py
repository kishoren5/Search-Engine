import concurrent.futures
import random
import time
from typing import Any, Literal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from search_engine.api.dependencies import get_global_retriever

try:
    import psutil
except ImportError:
    psutil = None

router = APIRouter(prefix="/v1/benchmark", tags=["benchmark"])

SAMPLE_QUERIES = [
    ("suspicious cash structuring smurfing CTR", {"risk_level": "CRITICAL"}),
    ("privacy mixer off-ramp layering", {"doc_type": "AML_SAR"}),
    ("OFAC SDN sanctions fuzzy match correspondent wire", {"risk_level": "HIGH"}),
    ("Basel III CET1 capital adequacy ratio", {"doc_type": "SEC_FILING"}),
    ("net interest margin commercial real estate mezzanine", {"ticker": "JPM"}),
    ("gross notional derivative credit default swap", {"ticker": "GS"}),
    ("SWIFT MT103 foreign exchange spot CLS settlement", {"doc_type": "SWIFT_TX"}),
    ("central bank reserve liquidity sweep Pacs 008", {"jurisdiction": "EU"}),
    ("syndicated credit facility debt EBITDA leverage", {"doc_type": "CREDIT_UNDERWRITING"}),
    ("counterparty margin deficit variation margin call", {"risk_level": "CRITICAL"}),
]


class BenchmarkRequest(BaseModel):
    query_count: int = Field(100, ge=10, le=1000, description="Total number of queries to execute")
    concurrency: int = Field(8, ge=1, le=32, description="Concurrent worker threads")
    workload: Literal["mixed", "aml", "sec", "swift"] = "mixed"
    custom_queries: list[str] | None = Field(None, description="Optional custom query strings")


class BenchmarkResponse(BaseModel):
    total_queries: int
    concurrency: int
    duration_seconds: float
    qps: float
    min_ms: float
    p50_ms: float
    p90_ms: float
    p95_ms: float
    p99_ms: float
    max_ms: float
    rss_mb: float
    error_count: int
    latency_buckets: list[dict[str, Any]] = []


def _run_single(retriever, query: str, filters: dict) -> float:
    t0 = time.perf_counter()
    _ = retriever.search(query=query, limit=10, filters=filters)
    return (time.perf_counter() - t0) * 1000.0


@router.post("/run", response_model=BenchmarkResponse)
def run_benchmark(req: BenchmarkRequest) -> BenchmarkResponse:
    retriever = get_global_retriever()
    if not retriever:
        raise HTTPException(status_code=503, detail="Search index is not currently loaded or ready")

    # If custom queries are supplied, use them
    if req.custom_queries and len(req.custom_queries) > 0:
        pool = [(cq.strip(), {}) for cq in req.custom_queries if cq.strip()]
    elif req.workload == "aml":
        pool = [q for q in SAMPLE_QUERIES if q[1].get("doc_type") == "AML_SAR" or "structuring" in q[0]]
    elif req.workload == "sec":
        pool = [q for q in SAMPLE_QUERIES if q[1].get("doc_type") == "SEC_FILING" or "Basel" in q[0]]
    elif req.workload == "swift":
        pool = [q for q in SAMPLE_QUERIES if q[1].get("doc_type") == "SWIFT_TX"]
    else:
        pool = SAMPLE_QUERIES

    if not pool:
        pool = SAMPLE_QUERIES

    selected_queries = [random.choice(pool) for _ in range(req.query_count)]

    latencies_ms: list[float] = []
    errors = 0
    start_time = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=req.concurrency) as executor:
        futures = [
            executor.submit(_run_single, retriever, q[0], q[1])
            for q in selected_queries
        ]
        for f in concurrent.futures.as_completed(futures):
            try:
                lat = f.result()
                latencies_ms.append(lat)
            except Exception:
                errors += 1

    total_time = max(time.perf_counter() - start_time, 0.001)
    qps = len(latencies_ms) / total_time

    latencies_ms.sort()
    n = len(latencies_ms)
    min_lat = latencies_ms[0] if n > 0 else 0.0
    p50_lat = latencies_ms[int(n * 0.50)] if n > 0 else 0.0
    p90_lat = latencies_ms[int(n * 0.90)] if n > 0 else 0.0
    p95_lat = latencies_ms[int(n * 0.95)] if n > 0 else 0.0
    p99_lat = latencies_ms[int(n * 0.99)] if n > 0 else 0.0
    max_lat = latencies_ms[-1] if n > 0 else 0.0

    rss_mb = psutil.Process().memory_info().rss / (1024 * 1024) if psutil else 0.0

    # Build latency distribution buckets
    b_under_05 = sum(1 for l in latencies_ms if l < 0.5)
    b_05_1 = sum(1 for l in latencies_ms if 0.5 <= l < 1.0)
    b_1_2 = sum(1 for l in latencies_ms if 1.0 <= l < 2.0)
    b_2_5 = sum(1 for l in latencies_ms if 2.0 <= l < 5.0)
    b_5_10 = sum(1 for l in latencies_ms if 5.0 <= l < 10.0)
    b_over_10 = sum(1 for l in latencies_ms if l >= 10.0)

    buckets = [
        {"bucket": "< 0.5ms", "count": b_under_05, "pct": round(b_under_05 / max(n, 1) * 100, 1)},
        {"bucket": "0.5-1ms", "count": b_05_1, "pct": round(b_05_1 / max(n, 1) * 100, 1)},
        {"bucket": "1-2ms", "count": b_1_2, "pct": round(b_1_2 / max(n, 1) * 100, 1)},
        {"bucket": "2-5ms", "count": b_2_5, "pct": round(b_2_5 / max(n, 1) * 100, 1)},
        {"bucket": "5-10ms", "count": b_5_10, "pct": round(b_5_10 / max(n, 1) * 100, 1)},
        {"bucket": "> 10ms", "count": b_over_10, "pct": round(b_over_10 / max(n, 1) * 100, 1)},
    ]

    return BenchmarkResponse(
        total_queries=req.query_count,
        concurrency=req.concurrency,
        duration_seconds=round(total_time, 3),
        qps=round(qps, 1),
        min_ms=round(min_lat, 2),
        p50_ms=round(p50_lat, 2),
        p90_ms=round(p90_lat, 2),
        p95_ms=round(p95_lat, 2),
        p99_ms=round(p99_lat, 2),
        max_ms=round(max_lat, 2),
        rss_mb=round(rss_mb, 1),
        error_count=errors,
        latency_buckets=buckets,
    )
