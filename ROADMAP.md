# Flagship Project Roadmap

Build vertical slices, keep the main branch runnable, and publish evidence for each stage. The numbers below are goals to validate, not promises.

## Stage 0 — Baseline and reproducibility
- Freeze a corpus version and query/qrels set.
- Record hardware, OS, commit, build command, and current metrics.
- Add one-command index build, search, evaluation, and benchmark scripts.
- Acceptance: another person can reproduce a baseline report from a clean checkout.

## Stage 1 — Correct single-node lexical engine
- Canonical document schema and deterministic tokenizer.
- Inverted index with postings and corpus statistics.
- BM25 with stable top-k ordering.
- Unit/property tests against a simple reference implementation.
- Acceptance: deterministic results, correct edge-case behavior, quality baseline recorded.

## Stage 2 — Index durability and compression
- Immutable segments and versioned manifest.
- Delta-coded document IDs; benchmark variable-byte or bit-packed encoding.
- Memory-mapped read-only index where beneficial.
- Checksums, corruption detection, atomic activation, rollback.
- Acceptance: compressed size, peak RAM, build time, and query latency compared with baseline.

## Stage 3 — API and developer experience
- FastAPI endpoint, typed schemas, pagination/top-k cap, errors.
- Health/readiness endpoints and CLI.
- Docker image and local compose profile.
- Acceptance: API integration tests and a clean local quick start.

## Stage 4 — Hybrid retrieval
- Dense embeddings with explicit model/version metadata.
- ANN or exact vector baseline, depending on corpus size and latency budget.
- RRF fusion; configurable candidate depth.
- Optional cross-encoder reranking under strict timeout.
- Acceptance: fixed qrels report compares BM25, dense, fusion, and reranking.

## Stage 5 — Observability and load testing
- Request IDs, structured logs, latency histograms, error counters.
- OpenTelemetry spans for query stages and shard fan-out.
- Load-test profile with realistic query distribution and concurrency.
- Acceptance: p50/p95/p99, throughput, saturation point, and error rate documented.

## Stage 6 — Sharding and replicas
- Deterministic shard assignment and manifest-based routing.
- Parallel fan-out and deterministic top-k merge.
- Replica health, bounded retries, deadlines, partial-result policy.
- Fault injection for node loss, timeout, stale replica, and network failure.
- Acceptance: correctness against single-node results and documented degradation behavior.

## Stage 7 — Production hardening
- Authentication and authorization for admin operations.
- Rate limits, payload limits, dependency pinning, container scanning.
- Snapshot restore and rollback drill.
- Operational runbook and architecture threat model.
- Acceptance: CI green, recovery procedure exercised, and no secrets in repository.

## Stage 8 — Final-year demonstration
Demonstrate:
1. Query examples where lexical, semantic, and hybrid results differ.
2. Quality evaluation with qrels and per-query error analysis.
3. Memory/index-size comparison before and after compression.
4. Load-test dashboard with p50/p95/p99 and throughput.
5. A shard/replica failure and graceful degradation.
6. Index rebuild, atomic swap, and rollback.
7. Architecture diagram, ADRs, test report, and limitations.

## Prioritization if time is limited

**Must-have:** correct BM25, hybrid fusion, reproducible evaluation, immutable index versions, API, tests, Docker, metrics, load test.

**Strong differentiators:** memory mapping, compression study, shard fan-out, replica failover, fault injection, CI, runbook.

**Stretch goals:** incremental indexing, query rewriting, learning-to-rank, multilingual analysis, freshness SLAs, Kubernetes deployment, adaptive caching. Avoid these until the core is measured and stable.
