import tempfile
from pathlib import Path

from search_engine.index.manifest import verify_manifest
from search_engine.index.mmap_store import MMapIndexReader
from search_engine.ingestion.pipeline import IngestionPipeline
from search_engine.retrieval.bm25 import BM25Retriever


def test_pipeline_with_deduplication() -> None:
    sample_docs = [
        {"doc_id": "1", "title": "First", "text": "Operating systems manage hardware and process scheduling."},
        {"doc_id": "2", "title": "Duplicate", "text": "Operating systems manage hardware and process scheduling."},  # Exact duplicate text
        {"doc_id": "3", "title": "Second", "text": "Computer networks route packets using the TCP/IP protocol stack."},
    ]

    pipeline = IngestionPipeline(segment_id="test_seg", enable_dedup=True)
    stats = pipeline.ingest_stream(iter(sample_docs))

    assert stats.total_read == 3
    assert stats.indexed == 2
    assert stats.duplicates_skipped == 1

    with tempfile.TemporaryDirectory() as tmpdir:
        seg_dir = pipeline.writer.write(tmpdir)
        assert verify_manifest(seg_dir / "manifest.json") is True

        with MMapIndexReader(seg_dir) as reader:
            assert reader.corpus_size == 2
            retriever = BM25Retriever(reader)
            hits = retriever.search("packets route", limit=5)
            assert len(hits) == 1
            assert hits[0].doc_id == "3"
