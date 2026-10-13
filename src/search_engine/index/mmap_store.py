import json
import mmap
from pathlib import Path
from typing import Any

from search_engine.index.compression import decompress_postings
from search_engine.index.manifest import verify_manifest


class MMapIndexReader:
    """Zero-copy memory-mapped index reader for compressed segments."""

    def __init__(self, segment_dir: str | Path) -> None:
        self.segment_dir = Path(segment_dir)
        manifest_path = self.segment_dir / "manifest.json"
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found in {self.segment_dir}")

        with open(manifest_path, "r", encoding="utf-8") as f:
            self.manifest = json.load(f)

        self.corpus_size: int = self.manifest["corpus_size"]
        self.total_terms: int = self.manifest["total_terms"]
        self.average_document_length: float = self.manifest["avg_doc_length"]

        # Load lexicon (term -> {df, offset, length})
        lexicon_path = self.segment_dir / "lexicon.json"
        with open(lexicon_path, "r", encoding="utf-8") as f:
            self.lexicon: dict[str, dict[str, int]] = json.load(f)

        # Load documents metadata
        docs_path = self.segment_dir / "documents.json"
        with open(docs_path, "r", encoding="utf-8") as f:
            self.documents: list[dict[str, Any]] = json.load(f)

        self._meta_by_id: dict[str, dict[str, Any]] = {d["doc_id"]: d for d in self.documents}
        self._doc_id_to_int_id: dict[str, int] = {d["doc_id"]: i for i, d in enumerate(self.documents)}
        self._dynamic_postings: dict[str, list[tuple[int, int]]] = {}

        # Document lengths cache for fast O(1) BM25 scoring
        self.doc_lengths: list[int] = [d.get("length", 0) for d in self.documents]

        # Memory-map the postings.bin file
        self.postings_path = self.segment_dir / "postings.bin"
        self._file_obj = open(self.postings_path, "rb")
        file_size = self.postings_path.stat().st_size
        if file_size > 0:
            self._mmap = mmap.mmap(self._file_obj.fileno(), 0, access=mmap.ACCESS_READ)
        else:
            self._mmap = None

    def get_document_frequency(self, term: str) -> int:
        entry = self.lexicon.get(term)
        return entry["df"] if entry else 0

    def get_postings(self, term: str) -> tuple[list[int], list[int]]:
        """Retrieve and decompress postings for term: returns (int_doc_ids, term_frequencies)."""
        mmap_doc_ids: list[int] = []
        mmap_tfs: list[int] = []

        if self._mmap is not None:
            entry = self.lexicon.get(term)
            if entry and entry.get("length", 0) > 0:
                offset = entry["offset"]
                length = entry["length"]
                compressed_bytes = self._mmap[offset : offset + length]
                mmap_doc_ids, mmap_tfs = decompress_postings(compressed_bytes)

        if term in self._dynamic_postings:
            dyn_pairs = self._dynamic_postings[term]
            for d_id, tf in dyn_pairs:
                mmap_doc_ids.append(d_id)
                mmap_tfs.append(tf)

        return mmap_doc_ids, mmap_tfs

    def add_document_in_memory(self, doc_dict: dict[str, Any]) -> str:
        """Dynamically ingest a document into the active reader without re-serializing segment."""
        from collections import Counter
        from search_engine.retrieval.tokenizer import tokenize

        doc_id = doc_dict.get("doc_id") or f"DYN-{len(self.documents) + 1:06d}"
        doc_dict["doc_id"] = doc_id

        full_text = f"{doc_dict.get('title', '')} {doc_dict.get('snippet', '')}"
        tokens = tokenize(full_text)
        doc_len = len(tokens)
        doc_dict["length"] = doc_len

        int_id = len(self.documents)
        self.documents.append(doc_dict)
        self._meta_by_id[doc_id] = doc_dict
        self._doc_id_to_int_id[doc_id] = int_id
        self.doc_lengths.append(doc_len)

        # Update corpus size and avgdl
        prev_total = self.corpus_size * self.average_document_length
        self.corpus_size += 1
        self.average_document_length = (prev_total + doc_len) / self.corpus_size

        counts = Counter(tokens)
        for term, tf in counts.items():
            if term not in self._dynamic_postings:
                self._dynamic_postings[term] = []
            self._dynamic_postings[term].append((int_id, tf))
            if term not in self.lexicon:
                self.lexicon[term] = {"df": 1, "offset": 0, "length": 0}
                self.total_terms += 1
            else:
                self.lexicon[term]["df"] += 1

        return doc_id

    def get_doc_metadata(self, int_doc_id: int) -> dict[str, Any] | None:
        if 0 <= int_doc_id < len(self.documents):
            return self.documents[int_doc_id]
        return None

    def get_doc_metadata_by_id(self, doc_id: str) -> dict[str, Any] | None:
        return self._meta_by_id.get(doc_id)

    def close(self) -> None:
        if self._mmap is not None:
            self._mmap.close()
            self._mmap = None
        if self._file_obj is not None:
            self._file_obj.close()
            self._file_obj = None

    def __enter__(self) -> "MMapIndexReader":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
