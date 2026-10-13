# Benchmark Methodology

## Purpose

This document defines the minimum evidence required for every published latency, throughput, indexing, memory, compression, and relevance claim.

## Required metadata

- Commit SHA and dirty/clean working tree
- Corpus identifier, version, document count, raw bytes, processed bytes
- Query set version and qrels version
- CPU model, physical/logical cores, RAM, storage type, OS/kernel, compiler and flags
- Python and dependency versions
- Index build configuration and BM25/vector model parameters
- Cold or warm cache; whether model loading is included
- Number of warm-up queries, repetitions, concurrency, run duration
- Timeout, error, and retry policy

## Performance metrics

Report p50, p95, and p99 latency; throughput; error/timeout rate; CPU; resident memory; disk reads; index build wall-clock time; peak build memory; and final index bytes. Include both client-observed and server-side latency where possible.

Run a baseline and candidate under the same conditions. Avoid comparing different corpora, hardware, warm-up policies, or query mixes without explicit caveats. Keep raw per-request results in a machine-readable artifact and summarize them in a versioned report.

## Relevance metrics

Use a fixed held-out query set with graded relevance judgments:
- nDCG@10
- MRR@10
- Recall@100
- Precision@10

Report overall and by query class (exact identifier, rare term, natural-language, multi-term, no-result). Record the evaluation script version and the number of judged queries. Tune parameters on validation data, not the final test set.

## Measured Scale Benchmark Results

| Run | Corpus | Doc Count | Terms | Ingestion Speed | MMap Startup | p50 Latency | p95 Latency | p99 Latency | QPS | Total Index Size | Postings Size |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **10k Run** | Technical CS | 9,939 | 428,023 | 12,878 docs/sec | 28.5 ms | 7.31 ms | 15.47 ms | 17.62 ms | 131.3 | 3.96 MB | 0.66 MB |
| **25k Run** | Technical CS | 24,551 | 1,057,028 | 11,894 docs/sec | 63.2 ms | 18.86 ms | 40.34 ms | 43.88 ms | 50.9 | 9.78 MB | 1.63 MB |

*Tested on Python 3.13 / Windows 11 with Variable-Byte & Delta compressed postings and zero-copy `mmap` reading.*
