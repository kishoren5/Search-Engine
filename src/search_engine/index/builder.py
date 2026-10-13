import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from search_engine.retrieval.postings import Posting, PostingsList
from search_engine.retrieval.tokenizer import term_frequencies, tokenize


@dataclass
class DocumentMetadata:
    doc_id: str
    title: str = ""
    url: str = ""
    snippet: str = ""
    length: int = 0


class InvertedIndex:
    """In-memory inverted index with full corpus statistics and serialization."""

    def __init__(self) -> None:
        self.postings: dict[str, PostingsList] = {}
        self.doc_metadata: dict[str, DocumentMetadata] = {}
        self.total_terms: int = 0

    @property
    def corpus_size(self) -> int:
        return len(self.doc_metadata)

    @property
    def average_document_length(self) -> float:
        if not self.doc_metadata:
            return 0.0
        return self.total_terms / len(self.doc_metadata)

    def add_document(
        self,
        doc_id: str,
        text: str,
        title: str = "",
        url: str = "",
    ) -> None:
        """Add a single document to the index."""
        tokens = tokenize(f"{title} {text}")
        doc_len = len(tokens)
        tfs = term_frequencies(tokens)

        # Generate simple snippet (first 160 characters of text)
        snippet = text[:160] + ("..." if len(text) > 160 else "")

        self.doc_metadata[doc_id] = DocumentMetadata(
            doc_id=doc_id,
            title=title,
            url=url,
            snippet=snippet,
            length=doc_len,
        )
        self.total_terms += doc_len

        for term, tf in tfs.items():
            if term not in self.postings:
                self.postings[term] = PostingsList(term=term)
            self.postings[term].add(doc_id=doc_id, tf=tf)

    def build_from_documents(self, documents: Iterable[Mapping[str, Any]]) -> None:
        """Batch index an iterable of documents."""
        for doc in documents:
            self.add_document(
                doc_id=str(doc.get("doc_id", doc.get("id", ""))),
                text=str(doc.get("text", doc.get("content", doc.get("body", "")))),
                title=str(doc.get("title", "")),
                url=str(doc.get("url", "")),
            )

    def get_document_frequency(self, term: str) -> int:
        posting = self.postings.get(term)
        return posting.document_frequency if posting else 0

    def get_postings(self, term: str) -> list[Posting]:
        posting = self.postings.get(term)
        return posting.postings if posting else []

    def save(self, filepath: str | Path) -> None:
        """Serialize index to JSON format."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "version": "1.0",
            "total_terms": self.total_terms,
            "doc_metadata": {
                doc_id: {
                    "doc_id": m.doc_id,
                    "title": m.title,
                    "url": m.url,
                    "snippet": m.snippet,
                    "length": m.length,
                }
                for doc_id, m in self.doc_metadata.items()
            },
            "postings": {
                term: [{"doc_id": p.doc_id, "tf": p.term_frequency} for p in plist.postings]
                for term, plist in self.postings.items()
            },
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    @classmethod
    def load(cls, filepath: str | Path) -> "InvertedIndex":
        """Load index from JSON format."""
        path = Path(filepath)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        index = cls()
        index.total_terms = data.get("total_terms", 0)

        for doc_id, m in data.get("doc_metadata", {}).items():
            index.doc_metadata[doc_id] = DocumentMetadata(
                doc_id=m["doc_id"],
                title=m.get("title", ""),
                url=m.get("url", ""),
                snippet=m.get("snippet", ""),
                length=m.get("length", 0),
            )

        for term, raw_plist in data.get("postings", {}).items():
            plist = PostingsList(term=term)
            for p in raw_plist:
                plist.add(doc_id=p["doc_id"], tf=p["tf"])
            index.postings[term] = plist

        return index
