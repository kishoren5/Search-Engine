from search_engine.retrieval.fusion import RankedHit, reciprocal_rank_fusion


def test_rrf_promotes_documents_ranked_well_by_both_retrievers() -> None:
    lexical = [RankedHit("a", 9.0, 1), RankedHit("b", 8.0, 2)]
    dense = [RankedHit("b", 0.9, 1), RankedHit("a", 0.8, 2)]
    result = reciprocal_rank_fusion([lexical, dense], rrf_k=10, limit=2)
    assert {hit.doc_id for hit in result} == {"a", "b"}
    assert result[0].score == result[1].score


def test_rrf_is_deterministic_for_ties() -> None:
    hits = [RankedHit("z", 1.0, 1), RankedHit("a", 1.0, 1)]
    result = reciprocal_rank_fusion([hits], rrf_k=60, limit=2)
    assert [hit.doc_id for hit in result] == ["a", "z"]
