import time
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from search_engine.index.segments import SegmentWriter
from search_engine.ingestion.deduplicate import Deduplicator
from search_engine.ingestion.normalize import clean_text
from search_engine.ingestion.readers import stream_csv, stream_jsonl


@dataclass
class IngestionStats:
    total_read: int
    indexed: int
    duplicates_skipped: int
    duration_seconds: float
    throughput_docs_sec: float
    total_terms: int


class IngestionPipeline:
    """Scalable streaming ingestion pipeline with deduplication, normalization, and segment writing."""

    def __init__(
        self,
        segment_id: str = "seg_001",
        enable_dedup: bool = True,
        strip_html: bool = True,
    ) -> None:
        self.writer = SegmentWriter(segment_id=segment_id)
        self.deduplicator = Deduplicator() if enable_dedup else None
        self.strip_html = strip_html

    def ingest_stream(
        self,
        doc_stream: Iterator[dict[str, Any]],
        progress_callback: Callable[[int, float], None] | None = None,
        progress_interval: int = 5000,
    ) -> IngestionStats:
        """Stream documents through the pipeline into the segment writer."""
        total_read = 0
        indexed = 0
        duplicates = 0
        start_time = time.perf_counter()

        for doc in doc_stream:
            total_read += 1
            raw_text = doc.get("text", "")
            cleaned_text = clean_text(raw_text, strip_html=self.strip_html)

            if not cleaned_text:
                continue

            if self.deduplicator and self.deduplicator.is_duplicate(cleaned_text):
                duplicates += 1
                continue

            cleaned_title = clean_text(doc.get("title", ""), strip_html=self.strip_html)
            meta = {k: v for k, v in doc.items() if k not in ["doc_id", "id", "text", "content", "body", "title", "url"]}

            self.writer.add_document(
                doc_id=doc.get("doc_id", f"doc_{indexed}"),
                text=cleaned_text,
                title=cleaned_title,
                url=doc.get("url", ""),
                metadata=meta,
            )
            indexed += 1

            if progress_callback and indexed % progress_interval == 0:
                elapsed = time.perf_counter() - start_time
                progress_callback(indexed, elapsed)

        duration = max(time.perf_counter() - start_time, 0.0001)
        throughput = indexed / duration

        return IngestionStats(
            total_read=total_read,
            indexed=indexed,
            duplicates_skipped=duplicates,
            duration_seconds=round(duration, 3),
            throughput_docs_sec=round(throughput, 1),
            total_terms=self.writer.total_terms,
        )

    def ingest_file(
        self,
        filepath: str | Path,
        output_dir: str | Path,
        progress_callback: Callable[[int, float], None] | None = None,
    ) -> tuple[Path, IngestionStats]:
        """Ingest a file (JSONL or CSV) and write the compressed segment to disk."""
        path = Path(filepath)
        if path.suffix in [".jsonl", ".json", ".gz"]:
            stream = stream_jsonl(path)
        elif path.suffix in [".csv"]:
            stream = stream_csv(path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")

        stats = self.ingest_stream(stream, progress_callback=progress_callback)
        seg_dir = self.writer.write(output_dir)
        return seg_dir, stats
