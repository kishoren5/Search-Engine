from fastapi.testclient import TestClient

from search_engine.api.app import app
from search_engine.api.dependencies import set_global_index
from search_engine.index.mmap_store import MMapIndexReader

client = TestClient(app)


def test_api_with_mmap_segment() -> None:
    segment_path = "data/bench_segments/scale_seg_001"
    reader = MMapIndexReader(segment_path)
    set_global_index(reader)

    # Health ready check
    res_ready = client.get("/health/ready")
    assert res_ready.status_code == 200
    assert res_ready.json()["status"] == "ready"
    assert res_ready.json()["corpus_size"] == reader.corpus_size

    # Search query
    res = client.get("/v1/search?q=consensus+raft&k=5")
    assert res.status_code == 200
    data = res.json()
    assert data["query"] == "consensus raft"
    assert len(data["results"]) == 5
    assert data["took_ms"] < 100.0  # Fast sub-100ms response
    assert data["results"][0]["score"] > 0
    assert "doc_id" in data["results"][0]
    assert "title" in data["results"][0]

    reader.close()
