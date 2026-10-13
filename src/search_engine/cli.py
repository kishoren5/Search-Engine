import argparse
import json
import sys
import time
from pathlib import Path

# Ensure src/ is on sys.path for direct script execution
_SRC_DIR = Path(__file__).resolve().parent.parent
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from search_engine.api.dependencies import set_global_index
from search_engine.index.builder import InvertedIndex
from search_engine.index.mmap_store import MMapIndexReader
from search_engine.ingestion.pipeline import IngestionPipeline
from search_engine.retrieval.bm25 import BM25Retriever


def load_index_auto(index_path: Path):
    """Load index automatically detecting whether it's an MMap segment or JSON index."""
    if index_path.is_dir() and (index_path / "manifest.json").exists():
        return MMapIndexReader(index_path)
    elif index_path.is_file():
        return InvertedIndex.load(index_path)
    else:
        # Check if parent is a segment dir or if a subdir exists
        if (index_path / "seg_001" / "manifest.json").exists():
            return MMapIndexReader(index_path / "seg_001")
        raise ValueError(f"Cannot identify index format at: {index_path}")


def cmd_index(args: argparse.Namespace) -> None:
    corpus_path = Path(args.corpus)
    if not corpus_path.exists():
        print(f"Error: Corpus file not found: {corpus_path}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output)

    if args.format == "segment":
        print(f"[*] Ingesting corpus from {corpus_path} into compressed binary segment...")
        pipeline = IngestionPipeline(segment_id=args.segment_id, enable_dedup=not args.no_dedup)
        output_dir = output_path if output_path.is_dir() or not output_path.suffix else output_path.parent

        seg_dir, stats = pipeline.ingest_file(
            corpus_path,
            output_dir,
            progress_callback=lambda idx, elap: print(
                f"[*] Ingested {idx:,} documents ({idx / max(elap, 0.001):.1f} docs/sec)..."
            ),
        )

        print(f"[+] Ingestion complete: {stats.indexed:,} documents indexed ({stats.total_terms:,} terms)")
        print(f"    - Duplicates skipped: {stats.duplicates_skipped:,}")
        print(f"    - Duration: {stats.duration_seconds:.2f}s ({stats.throughput_docs_sec:.1f} docs/sec)")
        print(f"    - Compressed segment written to: {seg_dir}")
    else:
        print(f"[*] Reading corpus from {corpus_path} into JSON index...")
        index = InvertedIndex()
        count = 0
        start_time = time.perf_counter()

        with open(corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                doc = json.loads(line)
                index.add_document(
                    doc_id=str(doc.get("doc_id", doc.get("id", f"doc-{count}"))),
                    text=str(doc.get("text", doc.get("content", doc.get("body", "")))),
                    title=str(doc.get("title", "")),
                    url=str(doc.get("url", "")),
                )
                count += 1
                if count % 10000 == 0:
                    print(f"[*] Indexed {count} documents...")

        duration = time.perf_counter() - start_time
        print(f"[+] Indexed {count} documents in {duration:.2f}s ({count / max(duration, 0.001):.1f} docs/sec)")
        print(f"[*] Saving JSON index to {output_path}...")
        index.save(output_path)
        print(f"[+] Successfully wrote index to {output_path}")


def cmd_search(args: argparse.Namespace) -> None:
    index_path = Path(args.index)
    if not index_path.exists():
        print(f"Error: Index path not found: {index_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Loading index from {index_path}...")
    t0 = time.perf_counter()
    index = load_index_auto(index_path)
    load_time = (time.perf_counter() - t0) * 1000.0
    print(f"[+] Loaded index ({index.corpus_size:,} docs) in {load_time:.2f}ms")

    retriever = BM25Retriever(index)
    t1 = time.perf_counter()
    hits = retriever.search(args.query, limit=args.k)
    search_time = (time.perf_counter() - t1) * 1000.0

    print(f"\n--- Search results for '{args.query}' ({len(hits)} hits, {search_time:.2f}ms) ---")
    for hit in hits:
        title, snippet = hit.doc_id, ""
        if hasattr(index, "doc_metadata"):
            meta = index.doc_metadata.get(hit.doc_id)
            if meta:
                title, snippet = meta.title or hit.doc_id, meta.snippet
        elif hasattr(index, "get_doc_metadata_by_id"):
            meta_dict = index.get_doc_metadata_by_id(hit.doc_id)
            if meta_dict:
                title = meta_dict.get("title") or hit.doc_id
                snippet = meta_dict.get("snippet", "")

        print(f"#{hit.rank} [{hit.score:.4f}] {title} (ID: {hit.doc_id})")
        if snippet:
            print(f"   {snippet}")
        print()


def cmd_serve(args: argparse.Namespace) -> None:
    import uvicorn
    from search_engine.api.app import app

    if args.index:
        index_path = Path(args.index)
        if index_path.exists():
            print(f"[*] Pre-loading index from {index_path}...")
            index = load_index_auto(index_path)
            set_global_index(index)
            print(f"[+] Index ready with {index.corpus_size:,} documents.")
        else:
            print(f"[!] Warning: Index path {index_path} does not exist. Starting empty.")

    uvicorn.run(app, host=args.host, port=args.port)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="search-engine",
        description="Flagship High-Performance Search Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # index
    p_index = subparsers.add_parser("index", help="Build an inverted index from JSONL/CSV corpus")
    p_index.add_argument("--corpus", "-c", required=True, help="Path to input corpus file")
    p_index.add_argument("--output", "-o", default="data/segments", help="Output path (dir or file)")
    p_index.add_argument("--format", choices=["segment", "json"], default="segment", help="Index format (segment=mmap binary)")
    p_index.add_argument("--segment-id", default="seg_001", help="Segment identifier")
    p_index.add_argument("--no-dedup", action="store_true", help="Disable document deduplication")
    p_index.set_defaults(func=cmd_index)

    # search
    p_search = subparsers.add_parser("search", help="Execute a BM25 search query from CLI")
    p_search.add_argument("--query", "-q", required=True, help="Query string")
    p_search.add_argument("--index", "-i", default="data/segments/seg_001", help="Path to index segment dir or JSON")
    p_search.add_argument("--k", type=int, default=10, help="Number of results to retrieve")
    p_search.set_defaults(func=cmd_search)

    # serve
    p_serve = subparsers.add_parser("serve", help="Start the FastAPI search server")
    p_serve.add_argument("--index", "-i", default="data/segments/seg_001", help="Path to index segment dir or JSON")
    p_serve.add_argument("--host", default="127.0.0.1", help="Host address to bind")
    p_serve.add_argument("--port", type=int, default=8000, help="Port to bind")
    p_serve.set_defaults(func=cmd_serve)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
