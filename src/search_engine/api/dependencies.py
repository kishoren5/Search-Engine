from typing import Any, Optional

from search_engine.retrieval.bm25 import BM25Retriever

_GLOBAL_INDEX: Optional[Any] = None
_GLOBAL_RETRIEVER: Optional[BM25Retriever] = None


def set_global_index(index: Any) -> None:
    global _GLOBAL_INDEX, _GLOBAL_RETRIEVER
    _GLOBAL_INDEX = index
    _GLOBAL_RETRIEVER = BM25Retriever(index)


def get_global_index() -> Optional[Any]:
    return _GLOBAL_INDEX


def get_global_retriever() -> Optional[BM25Retriever]:
    return _GLOBAL_RETRIEVER
