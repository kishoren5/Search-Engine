from typing import Any, Literal
from pydantic import BaseModel, Field


class LatencyWaterfall(BaseModel):
    tokenize_ms: float
    retrieval_ms: float
    explain_ms: float
    hydration_ms: float
    total_ms: float


class SearchResultItem(BaseModel):
    doc_id: str
    title: str = ""
    url: str = ""
    snippet: str = ""
    score: float
    rank: int
    ticker: str | None = None
    risk_level: str | None = None
    doc_type: str | None = None
    amount: float | None = None
    jurisdiction: str | None = None
    explanation: list[dict[str, Any]] | None = None


class SearchResponse(BaseModel):
    query: str
    mode: Literal["lexical", "hybrid", "semantic"]
    results: list[SearchResultItem]
    took_ms: float
    index_version: str
    partial: bool = False
    total_hits: int
    k1: float = 1.2
    b: float = 0.75
    waterfall: LatencyWaterfall | None = None


class HealthStatus(BaseModel):
    status: Literal["alive", "ready", "not_ready"]
    version: str = "1.0.0-fintech-mmap"
    corpus_size: int = 0
    reason: str | None = None


# Testing & Verification Schemas
class TestCaseResult(BaseModel):
    test_id: str
    name: str
    category: str
    status: Literal["PASSED", "FAILED", "SKIPPED"]
    duration_ms: float
    summary: str
    log: str


class TestSuiteResponse(BaseModel):
    total_tests: int
    passed_tests: int
    failed_tests: int
    duration_ms: float
    all_passed: bool
    results: list[TestCaseResult]


class RelevanceMetricItem(BaseModel):
    query: str
    expected_archetype: str
    p_at_5: float
    p_at_10: float
    reciprocal_rank: float
    top_hit_id: str
    top_hit_title: str
    top_hit_doc_type: str


class RelevanceEvalResponse(BaseModel):
    queries_evaluated: int
    mean_p5: float
    mean_p10: float
    mrr: float
    k1_used: float
    b_used: float
    took_ms: float
    metrics: list[RelevanceMetricItem]


# Dynamic Ingestion Schemas
class IngestDocRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=256)
    snippet: str = Field(..., min_length=5, max_length=4096)
    doc_type: str = Field("AML_SAR")
    ticker: str = Field("JPM")
    risk_level: str = Field("CRITICAL")
    amount: float | None = Field(None)
    jurisdiction: str = Field("US")


class IngestDocResponse(BaseModel):
    doc_id: str
    status: str
    tokens_indexed: int
    corpus_size_now: int
    duration_ms: float
    message: str


class DocumentDetailResponse(BaseModel):
    doc_id: str
    title: str
    snippet: str
    url: str
    length: int
    metadata: dict[str, Any]
