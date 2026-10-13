from fastapi.testclient import TestClient

from search_engine.api.app import app
from search_engine.api.dependencies import set_global_index
from search_engine.index.builder import InvertedIndex

client = TestClient(app)


def test_health_live() -> None:
    res = client.get("/health/live")
    assert res.status_code == 200
    assert res.json()["status"] == "alive"


def test_health_ready_unloaded() -> None:
    # Before index loaded
    res = client.get("/health/ready")
    assert res.status_code == 200
    # may be not_ready
    assert res.json()["status"] in ["ready", "not_ready"]


def test_search_endpoint() -> None:
    index = InvertedIndex()
    index.add_document("doc1", "distributed consensus raft paxos", title="Consensus Algorithms")
    set_global_index(index)

    ready_res = client.get("/health/ready")
    assert ready_res.status_code == 200
    assert ready_res.json()["status"] == "ready"

    res = client.get("/v1/search?q=consensus&k=5")
    assert res.status_code == 200
    data = res.json()
    assert data["query"] == "consensus"
    assert data["total_hits"] >= 1
    assert data["results"][0]["doc_id"] == "doc1"
    assert data["results"][0]["title"] == "Consensus Algorithms"
