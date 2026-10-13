from fastapi.testclient import TestClient

from search_engine.api.app import app
from search_engine.api.dependencies import set_global_index
from search_engine.index.mmap_store import MMapIndexReader
from search_engine.retrieval.bm25 import BM25Retriever

client = TestClient(app)


def test_fintech_mmap_search_and_filters() -> None:
    segment_path = "data/segments/fintech_prod_seg"
    reader = MMapIndexReader(segment_path)
    set_global_index(reader)

    # 1. Direct BM25Retriever test with structured filters
    retriever = BM25Retriever(reader)
    hits = retriever.search(
        query="suspicious cash structuring smurfing CTR",
        limit=5,
        filters={"risk_level": "CRITICAL"},
    )
    assert len(hits) > 0
    # Verify candidate metadata
    top_meta = reader.get_doc_metadata_by_id(hits[0].doc_id)
    assert top_meta is not None
    assert top_meta["metadata"]["risk_level"] == "CRITICAL"

    # 2. Test API root UI
    res_ui = client.get("/")
    assert res_ui.status_code == 200
    assert "BFSI Sentinel" in res_ui.text

    # 3. Test API /v1/search with query + ticker filter and waterfall
    res_search = client.get("/v1/search?q=Basel+CET1&ticker=JPM&k=5")
    assert res_search.status_code == 200
    data = res_search.json()
    assert data["total_hits"] > 0
    assert data.get("waterfall") is not None
    for item in data["results"]:
        assert item["ticker"] == "JPM"

    # 4. Test In-Engine Automated Verification Suite runner
    res_suite = client.post("/v1/test/run-suite")
    assert res_suite.status_code == 200
    suite_data = res_suite.json()
    assert suite_data["all_passed"] is True
    assert suite_data["total_tests"] == 6

    # 5. Test Golden IR Relevance Evaluation
    res_eval = client.post("/v1/test/eval-relevance", json={"k1": 1.2, "b": 0.75})
    assert res_eval.status_code == 200
    eval_data = res_eval.json()
    assert eval_data["mrr"] >= 0.80
    assert len(eval_data["metrics"]) > 0

    # 6. Test Live Ingestion Playground
    res_ingest = client.post(
        "/v1/ingest/document",
        json={
            "title": "Ad-hoc SAR Test Alert",
            "snippet": "Smurfing cash structuring detected in live testing sandbox.",
            "doc_type": "AML_SAR",
            "ticker": "JPM",
            "risk_level": "CRITICAL",
            "amount": 950000.0,
            "jurisdiction": "US",
        },
    )
    assert res_ingest.status_code == 200
    ingest_data = res_ingest.json()
    assert ingest_data["status"] == "INDEXED"
    new_doc_id = ingest_data["doc_id"]

    # 7. Test Document Detail Inspector Modal endpoint
    res_doc = client.get(f"/v1/document/{new_doc_id}")
    assert res_doc.status_code == 200
    assert res_doc.json()["title"] == "Ad-hoc SAR Test Alert"

    # 8. Test Live Benchmark endpoint with custom queries
    res_bench = client.post(
        "/v1/benchmark/run",
        json={"query_count": 10, "concurrency": 2, "workload": "mixed"},
    )
    assert res_bench.status_code == 200
    bench_data = res_bench.json()
    assert bench_data["qps"] > 0
    assert len(bench_data["latency_buckets"]) == 6

    # 9. Test Lexicon Inspector with sample postings preview
    res_term = client.get("/v1/inspect/term?term=smurfing")
    assert res_term.status_code == 200
    term_data = res_term.json()
    assert term_data["in_lexicon"] is True
    assert len(term_data["sample_postings"]) > 0

    reader.close()
