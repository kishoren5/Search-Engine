import heapq
import math
from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Any

from search_engine.index.builder import InvertedIndex
from search_engine.index.mmap_store import MMapIndexReader
from search_engine.retrieval.fusion import RankedHit
from search_engine.retrieval.tokenizer import tokenize


def bm25_score(
    query_terms: Sequence[str],
    term_frequencies: Mapping[str, int],
    document_length: int,
    document_frequencies: Mapping[str, int],
    corpus_size: int,
    average_document_length: float,
    *,
    k1: float = 1.2,
    b: float = 0.75,
) -> float:
    """Reference BM25 scorer for a single document."""
    if corpus_size <= 0 or average_document_length <= 0:
        return 0.0

    score = 0.0
    for term in query_terms:
        tf = term_frequencies.get(term, 0)
        df = document_frequencies.get(term, 0)
        if tf <= 0 or df <= 0:
            continue
        idf = math.log(1.0 + (corpus_size - df + 0.5) / (df + 0.5))
        norm = tf + k1 * (1.0 - b + b * document_length / average_document_length)
        score += idf * (tf * (k1 + 1.0)) / norm
    return score


class BM25Retriever:
    """High-performance BM25 retrieval engine with mmap support, hyperparameter tuning, and structured filtering."""

    def __init__(
        self,
        index: InvertedIndex | MMapIndexReader | Any,
        k1: float = 1.2,
        b: float = 0.75,
    ) -> None:
        self.index = index
        self.k1 = k1
        self.b = b

    def _matches_filters(self, doc_data: dict[str, Any] | None, filters: dict[str, Any] | None) -> bool:
        if not filters:
            return True
        if not doc_data:
            return False

        meta = doc_data.get("metadata", {})
        for key, expected_val in filters.items():
            if expected_val is None or expected_val == "":
                continue

            if key == "min_amount":
                amt = float(meta.get("amount", 0.0))
                if amt < float(expected_val):
                    return False
            elif key == "max_amount":
                amt = float(meta.get("amount", 0.0))
                if amt > float(expected_val):
                    return False
            else:
                actual = str(meta.get(key, "")).strip().upper()
                expected = str(expected_val).strip().upper()
                if actual != expected:
                    return False
        return True

    def search(
        self,
        query: str,
        limit: int = 10,
        filters: dict[str, Any] | None = None,
        k1: float | None = None,
        b: float | None = None,
    ) -> list[RankedHit]:
        """Search index with BM25 scoring, optional hyperparameter overrides, and structured filtering."""
        if limit <= 0:
            return []

        query_terms = tokenize(query)
        if not query_terms:
            return []

        corpus_size = self.index.corpus_size
        avgdl = self.index.average_document_length

        if corpus_size == 0 or avgdl <= 0.0:
            return []

        effective_k1 = k1 if k1 is not None else self.k1
        effective_b = b if b is not None else self.b

        is_mmap = isinstance(self.index, MMapIndexReader)

        if is_mmap:
            return self._search_mmap(query_terms, corpus_size, avgdl, limit, filters, effective_k1, effective_b)
        else:
            return self._search_inverted(query_terms, corpus_size, avgdl, limit, filters, effective_k1, effective_b)

    def _search_mmap(
        self,
        query_terms: list[str],
        corpus_size: int,
        avgdl: float,
        limit: int,
        filters: dict[str, Any] | None = None,
        k1: float = 1.2,
        b: float = 0.75,
    ) -> list[RankedHit]:
        scores: dict[int, float] = defaultdict(float)
        doc_lengths = self.index.doc_lengths

        for term in query_terms:
            doc_ids, tfs = self.index.get_postings(term)
            if not doc_ids:
                continue

            df = len(doc_ids)
            idf = math.log(1.0 + (corpus_size - df + 0.5) / (df + 0.5))

            for i in range(len(doc_ids)):
                int_doc_id = doc_ids[i]
                tf = tfs[i]
                doc_len = doc_lengths[int_doc_id] if int_doc_id < len(doc_lengths) else int(avgdl)

                norm = tf + k1 * (1.0 - b + b * doc_len / avgdl)
                scores[int_doc_id] += idf * (tf * (k1 + 1.0)) / norm

        if not scores:
            return []

        filtered_scores: list[tuple[int, float]] = []
        if filters:
            for int_doc_id, score in scores.items():
                doc_data = self.index.get_doc_metadata(int_doc_id)
                if self._matches_filters(doc_data, filters):
                    filtered_scores.append((int_doc_id, score))
        else:
            filtered_scores = list(scores.items())

        if not filtered_scores:
            return []

        top_candidates = heapq.nlargest(
            limit,
            filtered_scores,
            key=lambda item: (item[1], -item[0]),
        )

        results: list[RankedHit] = []
        for rank, (int_doc_id, score) in enumerate(top_candidates, start=1):
            meta = self.index.get_doc_metadata(int_doc_id)
            doc_str_id = meta["doc_id"] if meta else str(int_doc_id)
            results.append(RankedHit(doc_id=doc_str_id, score=score, rank=rank))

        return results

    def _search_inverted(
        self,
        query_terms: list[str],
        corpus_size: int,
        avgdl: float,
        limit: int,
        filters: dict[str, Any] | None = None,
        k1: float = 1.2,
        b: float = 0.75,
    ) -> list[RankedHit]:
        scores: dict[str, float] = defaultdict(float)

        for term in query_terms:
            postings = self.index.get_postings(term)
            if not postings:
                continue

            df = len(postings)
            idf = math.log(1.0 + (corpus_size - df + 0.5) / (df + 0.5))

            for posting in postings:
                doc_id = posting.doc_id
                tf = posting.term_frequency
                meta = self.index.doc_metadata.get(doc_id)
                doc_len = meta.length if meta else int(avgdl)

                norm = tf + k1 * (1.0 - b + b * doc_len / avgdl)
                scores[doc_id] += idf * (tf * (k1 + 1.0)) / norm

        if not scores:
            return []

        filtered_scores = list(scores.items())

        top_candidates = heapq.nlargest(
            limit,
            filtered_scores,
            key=lambda item: (item[1], [-ord(c) for c in item[0]]),
        )

        return [
            RankedHit(doc_id=doc_id, score=score, rank=rank)
            for rank, (doc_id, score) in enumerate(top_candidates, start=1)
        ]

    def search_explained(
        self,
        query: str,
        limit: int = 10,
        filters: dict[str, Any] | None = None,
        k1: float | None = None,
        b: float | None = None,
    ) -> list[dict[str, Any]]:
        """Search and return full term-level score contribution breakdown for explainability."""
        query_terms = tokenize(query)
        if not query_terms:
            return []

        hits = self.search(query=query, limit=limit, filters=filters, k1=k1, b=b)
        explained: list[dict[str, Any]] = []

        effective_k1 = k1 if k1 is not None else self.k1
        effective_b = b if b is not None else self.b
        corpus_size = self.index.corpus_size
        avgdl = self.index.average_document_length

        for hit in hits:
            breakdown = []
            matched_terms = []

            for term in query_terms:
                df = self.index.get_document_frequency(term)
                if df == 0:
                    continue
                idf = math.log(1.0 + (corpus_size - df + 0.5) / (df + 0.5))

                # Check if term occurs in this doc
                doc_meta = None
                doc_len = int(avgdl)
                tf = 0

                if isinstance(self.index, MMapIndexReader):
                    import bisect
                    doc_meta = self.index.get_doc_metadata_by_id(hit.doc_id)
                    if doc_meta:
                        doc_len = doc_meta.get("length", int(avgdl))
                    doc_ids, tfs = self.index.get_postings(term)
                    int_id = getattr(self.index, "_doc_id_to_int_id", {}).get(hit.doc_id, -1)
                    if int_id != -1 and doc_ids:
                        idx = bisect.bisect_left(doc_ids, int_id)
                        if idx < len(doc_ids) and doc_ids[idx] == int_id:
                            tf = tfs[idx]

                if tf > 0:
                    matched_terms.append(term)
                    norm = tf + effective_k1 * (1.0 - effective_b + effective_b * doc_len / avgdl)
                    term_score = idf * (tf * (effective_k1 + 1.0)) / norm
                    breakdown.append({
                        "term": term,
                        "tf": tf,
                        "df": df,
                        "idf": round(idf, 4),
                        "score_contribution": round(term_score, 4),
                    })

            explained.append({
                "doc_id": hit.doc_id,
                "score": round(hit.score, 4),
                "rank": hit.rank,
                "matched_terms": matched_terms,
                "breakdown": breakdown,
            })

        return explained
