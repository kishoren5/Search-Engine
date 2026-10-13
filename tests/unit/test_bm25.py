from search_engine.index.builder import InvertedIndex
from search_engine.retrieval.bm25 import BM25Retriever, bm25_score


def test_bm25_score_monotonicity() -> None:
    # A document with higher term frequency should score higher than a document with lower tf, all else equal
    score_low_tf = bm25_score(
        query_terms=["search"],
        term_frequencies={"search": 1},
        document_length=10,
        document_frequencies={"search": 5},
        corpus_size=100,
        average_document_length=10.0,
    )

    score_high_tf = bm25_score(
        query_terms=["search"],
        term_frequencies={"search": 3},
        document_length=10,
        document_frequencies={"search": 5},
        corpus_size=100,
        average_document_length=10.0,
    )

    assert score_high_tf > score_low_tf


def test_bm25_retriever_ranking() -> None:
    index = InvertedIndex()
    index.add_document("doc1", "neural network deep learning artificial intelligence")
    index.add_document("doc2", "relational database index query sql optimization")
    index.add_document("doc3", "deep learning computer vision convolutional network")

    retriever = BM25Retriever(index)
    hits = retriever.search("deep learning", limit=5)

    assert len(hits) == 2
    matched_ids = {h.doc_id for h in hits}
    assert matched_ids == {"doc1", "doc3"}
    assert "doc2" not in matched_ids
    assert hits[0].rank == 1
    assert hits[1].rank == 2
