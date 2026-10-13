from search_engine.retrieval.tokenizer import term_frequencies, tokenize


def test_tokenize_basic() -> None:
    text = "Information Retrieval with Okapi BM25 and Inverted-Indexes!"
    tokens = tokenize(text, remove_stopwords=False)
    assert "information" in tokens
    assert "retrieval" in tokens
    assert "okapi" in tokens
    assert "bm25" in tokens
    assert "inverted" in tokens
    assert "indexes" in tokens


def test_tokenize_stopwords() -> None:
    text = "This is a document about search and retrieval"
    tokens = tokenize(text, remove_stopwords=True)
    assert "document" in tokens
    assert "search" in tokens
    assert "retrieval" in tokens
    assert "this" not in tokens
    assert "is" not in tokens
    assert "a" not in tokens


def test_term_frequencies() -> None:
    tokens = ["search", "engine", "search", "index", "search"]
    tfs = term_frequencies(tokens)
    assert tfs["search"] == 3
    assert tfs["engine"] == 1
    assert tfs["index"] == 1
