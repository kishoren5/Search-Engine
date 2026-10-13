import datetime
import json
from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from search_engine.index.compression import compress_postings
from search_engine.index.manifest import SegmentManifest, compute_sha256
from search_engine.retrieval.tokenizer import term_frequencies, tokenize


@dataclass(slots=True)
class DocRecord:
    doc_id: str
    title: str
    url: str
    snippet: str
    length: int
    metadata: dict[str, Any] = field(default_factory=dict)


class SegmentWriter:
    """Builds a compressed immutable index segment with delta/VByte postings and SHA-256 manifest."""

    def __init__(self, segment_id: str = "seg_001") -> None:
        self.segment_id = segment_id
        self.doc_records: list[DocRecord] = []
        # term -> list of (int_doc_id, tf)
        self.raw_postings: dict[str, list[tuple[int, int]]] = defaultdict(list)
        self.total_terms: int = 0

    def add_document(
        self,
        doc_id: str,
        text: str,
        title: str = "",
        url: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> int:
        """Add document and return internal integer doc ID."""
        int_doc_id = len(self.doc_records)
        meta_dict = metadata or {}
        # Incorporate key text attributes (e.g. ticker, doc_type) into indexed text
        extra_terms = " ".join(str(v) for k, v in meta_dict.items() if isinstance(v, str))
        tokens = tokenize(f"{title} {text} {extra_terms}")
        doc_len = len(tokens)
        tfs = term_frequencies(tokens)

        snippet = text[:180] + ("..." if len(text) > 180 else "")
        self.doc_records.append(
            DocRecord(
                doc_id=doc_id,
                title=title,
                url=url,
                snippet=snippet,
                length=doc_len,
                metadata=meta_dict,
            )
        )
        self.total_terms += doc_len

        for term, tf in tfs.items():
            self.raw_postings[term].append((int_doc_id, tf))

        return int_doc_id

    def build_from_iterable(self, documents: Iterable[Mapping[str, Any]]) -> int:
        count = 0
        for doc in documents:
            # Extract any extra fields as metadata
            meta = {k: v for k, v in doc.items() if k not in ["doc_id", "id", "text", "content", "body", "title", "url"]}
            self.add_document(
                doc_id=str(doc.get("doc_id", doc.get("id", f"doc_{count}"))),
                text=str(doc.get("text", doc.get("content", doc.get("body", "")))),
                title=str(doc.get("title", "")),
                url=str(doc.get("url", "")),
                metadata=meta,
            )
            count += 1
        return count

    def write(self, target_dir: str | Path) -> Path:
        """Serialize compressed segment to target directory."""
        seg_dir = Path(target_dir) / self.segment_id
        seg_dir.mkdir(parents=True, exist_ok=True)

        postings_bin_path = seg_dir / "postings.bin"
        lexicon_json_path = seg_dir / "lexicon.json"
        docs_json_path = seg_dir / "documents.json"
        manifest_json_path = seg_dir / "manifest.json"

        # 1. Compress postings and build lexicon
        lexicon: dict[str, dict[str, int]] = {}
        offset = 0

        with open(postings_bin_path, "wb") as f_postings:
            # Sort terms for deterministic layout
            for term in sorted(self.raw_postings.keys()):
                pairs = self.raw_postings[term]
                # Pairs are naturally sorted by int_doc_id
                doc_ids = [p[0] for p in pairs]
                tfs = [p[1] for p in pairs]

                compressed = compress_postings(doc_ids, tfs)
                f_postings.write(compressed)

                length = len(compressed)
                lexicon[term] = {
                    "df": len(doc_ids),
                    "offset": offset,
                    "length": length,
                }
                offset += length

        # 2. Write lexicon
        with open(lexicon_json_path, "w", encoding="utf-8") as f_lex:
            json.dump(lexicon, f_lex, ensure_ascii=False)

        # 3. Write document records
        docs_payload = [
            {
                "doc_id": r.doc_id,
                "title": r.title,
                "url": r.url,
                "snippet": r.snippet,
                "length": r.length,
                "metadata": r.metadata,
            }
            for r in self.doc_records
        ]
        with open(docs_json_path, "w", encoding="utf-8") as f_docs:
            json.dump(docs_payload, f_docs, ensure_ascii=False)

        # 4. Generate manifest with SHA-256 checksums
        corpus_size = len(self.doc_records)
        avgdl = (self.total_terms / corpus_size) if corpus_size > 0 else 0.0

        files_hash = {
            "postings.bin": compute_sha256(postings_bin_path),
            "lexicon.json": compute_sha256(lexicon_json_path),
            "documents.json": compute_sha256(docs_json_path),
        }

        manifest = SegmentManifest(
            version="1.0",
            segment_id=self.segment_id,
            corpus_size=corpus_size,
            total_terms=self.total_terms,
            avg_doc_length=avgdl,
            files=files_hash,
            created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )

        with open(manifest_json_path, "w", encoding="utf-8") as f_m:
            json.dump(manifest.__dict__, f_m, indent=2)

        return seg_dir
