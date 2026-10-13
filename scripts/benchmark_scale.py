import json
import os
import random
import sys
import time
from pathlib import Path

# Ensure src/ is on sys.path
_SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

try:
    import psutil
except ImportError:
    psutil = None

from search_engine.index.builder import InvertedIndex
from search_engine.index.mmap_store import MMapIndexReader
from search_engine.ingestion.pipeline import IngestionPipeline
from search_engine.retrieval.bm25 import BM25Retriever

# Vocabulary banks for generating realistic technical text
DOMAINS = [
    ("Distributed Systems", ["consensus", "raft", "paxos", "byzantine", "replication", "partition", "cap theorem", "quorum", "fault tolerance", "eventual consistency"]),
    ("Database Internals", ["b-tree", "lsm-tree", "wal", "write-ahead log", "acid", "mvcc", "transaction", "index scan", "buffer pool", "page cache"]),
    ("Information Retrieval", ["inverted index", "bm25", "postings list", "tf-idf", "tokenization", "stemming", "rrf", "relevance", "ranking", "ndcg"]),
    ("Operating Systems", ["kernel", "virtual memory", "paging", "mmap", "syscall", "context switch", "thread pool", "concurrency", "mutex", "deadlock"]),
    ("Machine Learning", ["neural network", "transformer", "attention mechanism", "gradient descent", "backpropagation", "loss function", "embeddings", "vector search", "fine-tuning", "inference"]),
    ("Cloud & Networking", ["tcp/ip", "congestion control", "latency", "throughput", "dns", "load balancer", "gateway", "microservices", "kubernetes", "service mesh"]),
]

TEMPLATES = [
    "In the domain of {domain}, {t1} and {t2} play an essential role in system architecture. When handling {t3}, engineers optimize for high throughput and bounded latency.",
    "A comprehensive study on {domain} demonstrates that {t1} outperforms legacy approaches when applied to {t2}. Furthermore, {t3} guarantees strict correctness.",
    "Implementing {t1} within modern {domain} environments requires careful memory management. By leveraging {t2} alongside {t3}, developers mitigate performance bottlenecks.",
    "Recent advances in {domain} reveal that {t1} can be effectively combined with {t2}. This hybrid methodology enhances {t3} under heavy concurrent workloads.",
    "Scalability in {domain} is heavily influenced by how {t1} is structured. Evaluating {t2} reveals that {t3} reduces resource contention and system overhead.",
]


def generate_synthetic_corpus(output_path: Path, num_docs: int = 10000) -> None:
    """Generate a realistic synthetic corpus in JSONL format."""
    print(f"[*] Generating {num_docs:,} technical documents for scale testing at {output_path}...")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    random.seed(42)
    start = time.perf_counter()

    with open(output_path, "w", encoding="utf-8") as f:
        for i in range(num_docs):
            domain, terms = random.choice(DOMAINS)
            selected_terms = random.sample(terms, 3)
            template = random.choice(TEMPLATES)
            body = template.format(domain=domain, t1=selected_terms[0], t2=selected_terms[1], t3=selected_terms[2])

            # Add extra paragraphs for realistic document lengths
            extra_domain, extra_terms = random.choice(DOMAINS)
            extra_body = random.choice(TEMPLATES).format(
                domain=extra_domain,
                t1=extra_terms[0],
                t2=extra_terms[1],
                t3=extra_terms[2],
            )
            full_text = f"{body} {extra_body}"
            title = f"{domain}: Analysis of {selected_terms[0].title()} and {selected_terms[1].title()}"

            doc = {
                "doc_id": f"doc_{i+1:06d}",
                "title": title,
                "text": full_text,
                "url": f"https://example.org/docs/{i+1}",
            }
            f.write(json.dumps(doc) + "\n")

    elapsed = time.perf_counter() - start
    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"[+] Generated {num_docs:,} documents ({size_mb:.2f} MB) in {elapsed:.2f}s")


def get_current_rss_mb() -> float:
    if psutil:
        return psutil.Process().memory_info().rss / (1024 * 1024)
    return 0.0


def benchmark_ingestion_and_retrieval(corpus_path: Path, num_queries: int = 500) -> None:
    print("\n" + "=" * 65)
    print("       FLAGSHIP SEARCH ENGINE SCALE & COMPRESSION BENCHMARK      ")
    print("=" * 65)

    rss_baseline = get_current_rss_mb()
    raw_size_mb = corpus_path.stat().st_size / (1024 * 1024)

    # 1. Ingest via Scalable Ingestion Pipeline (Compressed Segment)
    seg_dir_parent = Path("data/bench_segments")
    pipeline = IngestionPipeline(segment_id="scale_seg_001", enable_dedup=True)

    print(f"\n[1/3] Ingesting corpus into Compressed Binary Segment...")
    t0 = time.perf_counter()
    seg_dir, stats = pipeline.ingest_file(
        corpus_path,
        seg_dir_parent,
        progress_callback=lambda idx, elap: print(
            f"      - Ingested {idx:,} docs ({idx / max(elap, 0.001):.1f} docs/sec)"
        ),
    )
    ingest_time = time.perf_counter() - t0
    rss_after_ingest = get_current_rss_mb()

    # Calculate compressed segment size
    seg_size_bytes = sum(f.stat().st_size for f in seg_dir.glob("*") if f.is_file())
    seg_size_mb = seg_size_bytes / (1024 * 1024)
    postings_size_mb = (seg_dir / "postings.bin").stat().st_size / (1024 * 1024)

    print(f"[+] Ingestion Finished:")
    print(f"    - Documents Indexed: {stats.indexed:,}")
    print(f"    - Terms Processed:   {stats.total_terms:,}")
    print(f"    - Ingestion Speed:   {stats.throughput_docs_sec:,.1f} docs/sec")
    print(f"    - Raw Corpus Size:   {raw_size_mb:.2f} MB")
    print(f"    - Postings Size:     {postings_size_mb:.2f} MB")
    print(f"    - Total Seg Size:    {seg_size_mb:.2f} MB (Compression ratio: {raw_size_mb / max(seg_size_mb, 0.001):.2f}x)")

    # 2. Test MMap Cold & Warm Startup
    print(f"\n[2/3] Testing Zero-Copy MMap Initialization...")
    t_mmap_start = time.perf_counter()
    reader = MMapIndexReader(seg_dir)
    mmap_load_time_ms = (time.perf_counter() - t_mmap_start) * 1000.0
    rss_mmap_loaded = get_current_rss_mb()
    print(f"[+] Memory-mapped reader initialized in {mmap_load_time_ms:.3f} ms!")
    print(f"    - Resident Memory (RSS): {rss_mmap_loaded:.1f} MB (Delta: +{rss_mmap_loaded - rss_baseline:.1f} MB)")

    # 3. Query Benchmark
    print(f"\n[3/3] Running {num_queries} queries through BM25Retriever...")
    retriever = BM25Retriever(reader)

    query_pool = [
        "distributed consensus raft",
        "inverted index bm25 ranking",
        "virtual memory paging mmap",
        "neural network transformer attention",
        "database b-tree lsm-tree transaction",
        "tcp/ip latency throughput congestion",
        "paxos byzantine fault tolerance",
        "postings list compression variable byte",
        "vector search embeddings inference",
        "concurrency mutex deadlock scheduling",
    ]

    latencies_ms: list[float] = []

    # Warmup
    for q in query_pool:
        _ = retriever.search(q, limit=10)

    t_queries_start = time.perf_counter()
    for _ in range(num_queries):
        q = random.choice(query_pool)
        t_q0 = time.perf_counter()
        hits = retriever.search(q, limit=10)
        t_q1 = time.perf_counter()
        latencies_ms.append((t_q1 - t_q0) * 1000.0)

    total_query_time = time.perf_counter() - t_queries_start
    qps = num_queries / total_query_time

    latencies_ms.sort()
    p50 = latencies_ms[int(len(latencies_ms) * 0.50)]
    p95 = latencies_ms[int(len(latencies_ms) * 0.95)]
    p99 = latencies_ms[int(len(latencies_ms) * 0.99)]
    avg_latency = sum(latencies_ms) / len(latencies_ms)

    reader.close()

    print("\n" + "=" * 65)
    print("                    PERFORMANCE BENCHMARK RESULTS                ")
    print("=" * 65)
    print(f" Corpos Scale:       {stats.indexed:,} documents ({stats.total_terms:,} terms)")
    print(f" Raw Text Size:      {raw_size_mb:.2f} MB")
    print(f" Binary Index Size:  {seg_size_mb:.2f} MB")
    print(f" Storage Reduction:  {raw_size_mb / max(seg_size_mb, 0.001):.2f}x smaller")
    print(f" Index Ingestion:    {stats.throughput_docs_sec:,.1f} docs/sec ({stats.duration_seconds:.2f}s total)")
    print(f" MMap Startup Time:  {mmap_load_time_ms:.3f} ms")
    print(f" Query Throughput:   {qps:,.1f} QPS (Queries Per Second)")
    print(f" Average Latency:    {avg_latency:.3f} ms")
    print(f" p50 Latency:        {p50:.3f} ms")
    print(f" p95 Latency:        {p95:.3f} ms")
    print(f" p99 Latency:        {p99:.3f} ms")
    print("=" * 65)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Scale Ingestion & Performance Benchmark")
    parser.add_argument("--docs", type=int, default=10000, help="Number of documents to generate & ingest")
    parser.add_argument("--queries", type=int, default=500, help="Number of benchmark queries to execute")
    parser.add_argument("--corpus", type=str, default="", help="Optional existing corpus path")
    args = parser.parse_args()

    num_docs = args.docs
    corpus_path = Path(args.corpus) if args.corpus else Path(f"data/raw/benchmark_{num_docs // 1000}k.jsonl")

    if not corpus_path.exists():
        generate_synthetic_corpus(corpus_path, num_docs=num_docs)

    benchmark_ingestion_and_retrieval(corpus_path, num_queries=args.queries)


if __name__ == "__main__":
    main()
