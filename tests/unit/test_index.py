import tempfile
from pathlib import Path

from search_engine.index.builder import InvertedIndex


def test_index_build_and_statistics() -> None:
    index = InvertedIndex()
    index.add_document("doc1", "apple banana cherry", title="Fruit Document 1")
    index.add_document("doc2", "banana orange cherry date", title="Fruit Document 2")

    assert index.corpus_size == 2
    assert index.get_document_frequency("banana") == 2
    assert index.get_document_frequency("apple") == 1
    assert index.get_document_frequency("date") == 1
    assert index.get_document_frequency("nonexistent") == 0


def test_index_save_and_load() -> None:
    index = InvertedIndex()
    index.add_document("d1", "distributed inverted index", title="Doc 1", url="http://d1")
    index.add_document("d2", "sharded query planner", title="Doc 2", url="http://d2")

    with tempfile.TemporaryDirectory() as tmpdir:
        index_file = Path(tmpdir) / "index.json"
        index.save(index_file)
        assert index_file.exists()

        loaded = InvertedIndex.load(index_file)
        assert loaded.corpus_size == 2
        assert loaded.get_document_frequency("index") == 1
        assert loaded.doc_metadata["d1"].title == "Doc 1"
        assert loaded.doc_metadata["d1"].url == "http://d1"
