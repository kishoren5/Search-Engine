from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class RankedHit:
    doc_id: str
    score: float
    rank: int


def reciprocal_rank_fusion(
    ranked_lists: Sequence[Sequence[RankedHit]],
    *,
    rrf_k: int = 60,
    limit: int = 10,
) -> list[RankedHit]:
    """Fuse ranked lists using RRF; scores in input lists need not be calibrated."""
    if rrf_k <= 0 or limit <= 0:
        raise ValueError("rrf_k and limit must be positive")

    fused: dict[str, float] = {}
    for hits in ranked_lists:
        for hit in hits:
            if hit.rank < 1:
                raise ValueError("ranks must be 1-based positive integers")
            fused[hit.doc_id] = fused.get(hit.doc_id, 0.0) + 1.0 / (rrf_k + hit.rank)

    ordered = sorted(fused.items(), key=lambda item: (-item[1], item[0]))[:limit]
    return [
        RankedHit(doc_id=doc_id, score=score, rank=rank)
        for rank, (doc_id, score) in enumerate(ordered, start=1)
    ]
