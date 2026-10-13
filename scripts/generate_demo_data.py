import json
from pathlib import Path

DEMO_DOCUMENTS = [
    {
        "doc_id": "doc-001",
        "title": "Inverted Index and Postings Lists in Information Retrieval",
        "text": "An inverted index is the fundamental data structure used in modern search engines. It maps each term or word to a postings list containing document identifiers where the term occurs, along with term frequencies and positions. Efficient compression techniques such as Delta Encoding and Variable-Byte encoding reduce index size on disk significantly.",
        "url": "https://en.wikipedia.org/wiki/Inverted_index",
    },
    {
        "doc_id": "doc-002",
        "title": "Okapi BM25 Ranking Function",
        "text": "BM25 is a probabilistic retrieval framework that ranks documents based on the query terms appearing in each document, regardless of the inter-relationship between query terms within a document. It incorporates term frequency saturation via parameter k1 and document length normalization via parameter b, outperforming naive TF-IDF in most benchmarks.",
        "url": "https://en.wikipedia.org/wiki/Okapi_BM25",
    },
    {
        "doc_id": "doc-003",
        "title": "Reciprocal Rank Fusion for Hybrid Search",
        "text": "Reciprocal Rank Fusion (RRF) is an unsupervised ranking fusion method that combines the ranked results of multiple information retrieval systems, such as lexical BM25 and dense neural vector search. Because different search engines produce scores on non-calibrated scales, RRF uses positional ranks instead of raw numerical scores, guaranteeing robust fusion performance.",
        "url": "https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf",
    },
    {
        "doc_id": "doc-004",
        "title": "Dense Vector Embeddings and Semantic Retrieval",
        "text": "Dense retrieval utilizes deep neural network representations (embeddings) from models such as BERT, RoBERTa, and Sentence-BERT to map queries and documents into a shared continuous semantic vector space. Approximate Nearest Neighbor (ANN) search algorithms like HNSW and ScaNN enable sub-millisecond similarity queries across millions of dense vectors.",
        "url": "https://arxiv.org/abs/1908.10084",
    },
    {
        "doc_id": "doc-005",
        "title": "Distributed Sharding and Query Fan-out",
        "text": "In large-scale search architectures, documents are partitioned across multiple logical shards using document identifier hashing. A query planner broadcasts the search request to all shards concurrently via asynchronous fan-out. Each shard retrieves its local top-k candidates, and the coordinator merges these candidates into a global top-k result list.",
        "url": "https://en.wikipedia.org/wiki/Shard_(database_architecture)",
    },
    {
        "doc_id": "doc-006",
        "title": "High-Throughput Variable-Byte Integer Compression",
        "text": "Variable-byte encoding encodes positive integers into byte streams where the highest bit of each byte serves as a continuation flag. When combined with delta-encoding on sorted document ID lists in search engine postings, variable byte compression achieves fast decompression speeds while reducing index memory footprints by over 70 percent.",
        "url": "https://en.wikipedia.org/wiki/Variable-byte_encoding",
    },
    {
        "doc_id": "doc-007",
        "title": "Memory-Mapped Files (mmap) for Zero-Copy I/O",
        "text": "Memory mapping (mmap) maps file contents directly into the process virtual address space. This allows the search engine to read massive inverted index files directly from the operating system page cache without copying data into user-space buffers, maximizing memory efficiency and enabling instant cold-start queries.",
        "url": "https://en.wikipedia.org/wiki/Mmap",
    },
    {
        "doc_id": "doc-008",
        "title": "Cross-Encoder Re-ranking and Two-Stage Retrieval",
        "text": "Modern search engines employ two-stage retrieval architectures. The first stage retrieves hundreds of candidates using fast lexical (BM25) and dense vector retrievers. The second stage applies a computationally expensive cross-encoder model that scores full query-document interactions, improving precision and nDCG metrics.",
        "url": "https://arxiv.org/abs/2010.06467",
    },
    {
        "doc_id": "doc-009",
        "title": "Fault Tolerance, Deadlines, and Graceful Degradation",
        "text": "Distributed search systems must handle shard timeouts and node failures gracefully. By attaching deadline budgets to query fan-out requests, slow shards can be abandoned after a predetermined threshold. The search engine returns partial results with a partial flag set, ensuring high system availability and predictable p99 latency.",
        "url": "https://en.wikipedia.org/wiki/Fault_tolerance",
    },
    {
        "doc_id": "doc-010",
        "title": "Evaluation Metrics: nDCG, MRR, and Recall",
        "text": "Information retrieval systems are evaluated using standard offline relevance metrics. Normalized Discounted Cumulative Gain (nDCG) accounts for graded relevance judgments, Mean Reciprocal Rank (MRR) measures the position of the first relevant document, and Recall@k evaluates the fraction of all relevant documents captured in top-k results.",
        "url": "https://en.wikipedia.org/wiki/Discounted_cumulative_gain",
    },
]


def main() -> None:
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "demo_corpus.jsonl"

    print(f"[*] Generating demo corpus at {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        for doc in DEMO_DOCUMENTS:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")

    print(f"[+] Successfully wrote {len(DEMO_DOCUMENTS)} documents to {output_path}")


if __name__ == "__main__":
    main()
