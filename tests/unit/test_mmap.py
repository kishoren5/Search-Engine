import tempfile
from pathlib import Path

from search_engine.index.manifest import verify_manifest
from search_engine.index.mmap_store import MMapIndexReader
from search_engine.index.segments import SegmentWriter
from search_engine.retrieval.bm25 import BM25Retriever


def test_segment_writer_and_mmap_reader() -> None:
    docs = [
        {"doc_id": "doc1", "title": "Database Indexing", "text": "B-Tree and inverted index structures for query optimization"},
        {"doc_id": "doc2", "title": "Distributed Systems", "text": "Consensus and replication across partitioned clusters"},
        {"doc_id": "doc3", "title": "Information Retrieval", "text": "BM25 scoring and postings list compression algorithms"},
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        writer = SegmentWriter(segment_id="seg_test")
        writer.build_from_iterable(docs)
        seg_dir = writer.write(tmpdir)

        # 1. Verify manifest
        assert verify_manifest(seg_dir / "manifest.json") is True

        # 2. Open via MMapIndexReader
        with MMapIndexReader(seg_dir) as reader:
            assert reader.corpus_size == 3
            assert reader.get_document_frequency("indexing") == 1
            assert reader.get_document_frequency("and") == 0  # Stop words filtered
            assert reader.get_document_frequency("compression") == 1

            # 3. Retrieve postings
            doc_ids, tfs = reader.get_postings("compression")
            assert len(doc_ids) == 1
            assert len(tfs) == 1
            assert reader.get_doc_metadata(doc_ids[0])["doc_id"] == "doc3"

            # 4. Search via BM25Retriever
            retriever = BM25Retriever(reader)
            hits = retriever.search("inverted index structures", limit=5)
            assert len(hits) >= 1
            assert hits[0].doc_id == "doc1"
            assert hits[0].rank == 1
