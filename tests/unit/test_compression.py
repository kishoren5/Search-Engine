import pytest
from search_engine.index.compression import (
    compress_postings,
    decompress_postings,
    delta_decode,
    delta_encode,
    vbyte_decode,
    vbyte_encode,
)


def test_delta_roundtrip() -> None:
    original = [4, 12, 19, 50, 1000, 1000000]
    deltas = delta_encode(original)
    decoded = delta_decode(deltas)
    assert decoded == original


def test_vbyte_roundtrip() -> None:
    numbers = [0, 1, 127, 128, 255, 16383, 16384, 10000000]
    encoded = vbyte_encode(numbers)
    decoded = vbyte_decode(encoded)
    assert decoded == numbers


def test_compress_postings_roundtrip() -> None:
    doc_ids = [10, 25, 30, 105, 500, 10000]
    tfs = [1, 3, 2, 5, 1, 4]

    compressed = compress_postings(doc_ids, tfs)
    assert len(compressed) > 0

    dec_doc_ids, dec_tfs = decompress_postings(compressed)
    assert dec_doc_ids == doc_ids
    assert dec_tfs == tfs


def test_compress_postings_empty() -> None:
    compressed = compress_postings([], [])
    dec_doc_ids, dec_tfs = decompress_postings(compressed)
    assert dec_doc_ids == []
    assert dec_tfs == []
