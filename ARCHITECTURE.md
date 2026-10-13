# Architecture and Engineering Decisions

## 1. Runtime boundaries

Keep the search engine divided into five logical planes:

1. **Ingestion plane** — reads source records, validates schemas, normalizes text, deduplicates, and emits canonical documents.
2. **Build plane** — builds immutable index segments, computes corpus statistics, encodes postings, writes metadata and checksums, then publishes a manifest.
3. **Query plane** — validates queries, fans out to lexical/dense retrieval, fuses candidates, optionally reranks, and returns top-k.
4. **Control plane** — index version activation, shard status, safe reloads, and administrative operations.
5. **Observability plane** — metrics, structured logs, traces, quality evaluations, and benchmark artifacts.

Do not let the HTTP layer implement BM25 or read posting files directly. Route it through interfaces so retrieval can be unit-tested without running the API.

## 2. Index lifecycle

Use immutable index versions:

`raw corpus -> canonical documents -> segment build -> validate -> manifest -> activate`

A build must not overwrite the currently active index. Write to a temporary version directory, validate counts/checksums, fsync where appropriate, then atomically update the active manifest or pointer. Keep at least one previous valid version for rollback.

Suggested manifest fields:
- format version
- index version / build ID
- corpus ID and checksum
- document count and deleted-document count
- tokenizer and normalization version
- BM25 parameters
- segment file names, byte sizes, checksums
- vector model identifier and dimension, if applicable
- build timestamp and toolchain version

## 3. Retrieval interfaces

Define interfaces/protocols for:
- `LexicalRetriever.search(query, k, filters, deadline)`
- `DenseRetriever.search(query, k, filters, deadline)`
- `CandidateFusion.combine(lexical, dense, k)`
- `Reranker.rerank(query, candidates, deadline)`
- `ShardClient.search(shard_id, request, deadline)`

Each implementation must have bounded work and explicit failure behavior. The system should not wait indefinitely for a slow shard or a slow reranker.

## 4. Hybrid ranking

Start with BM25 as a reliable lexical baseline. Dense retrieval can find semantic matches but may underperform on exact identifiers, rare tokens, versions, and code symbols. Preserve lexical retrieval as an independently measurable path.

Recommended first fusion baseline: Reciprocal Rank Fusion (RRF). It combines ranks rather than raw scores, avoiding direct addition of incomparable BM25 and cosine-similarity scores. Tune the RRF constant on a held-out validation set; do not tune on the final test set. Evaluate:
- BM25 only
- dense only
- RRF
- calibrated weighted fusion
- fusion plus reranker

Use an offline qrels dataset and record per-query outcomes, not just one aggregate metric.

## 5. Sharding and replication

Choose a stable shard function such as `hash(doc_id) % shard_count` for the first version. Store the routing metadata in the index manifest. For a query, fan out concurrently to each relevant shard and merge top-k results.

Replica policy:
- select a healthy replica per shard
- use a bounded deadline and at most a small retry budget
- retry only operations safe to retry
- avoid retry storms when a shard is overloaded
- report `partial=true` when policy permits returning incomplete results
- expose failed shard IDs only in privileged diagnostics

Replication is not automatically high availability: test process death, network partitions, stale index versions, and correlated failures.

## 6. Performance model

Measure total latency as a sum of stages:
`validation + query encoding + fan-out + local retrieval + fusion + rerank + response serialization`

Parallel fan-out means end-to-end latency is often governed by the slowest participating shard plus coordination overhead. Record per-stage and per-shard histograms. Optimize the dominant measured component rather than assuming vector search or networking is the bottleneck.

## 7. Consistency and freshness

For a final-year project, begin with batch indexing and versioned snapshots. Add incremental ingestion only after snapshot builds and rollback are reliable. Clearly define:
- how frequently new documents become searchable
- whether updates are visible immediately or after a rebuild
- how deletes propagate to every replica
- how mixed index versions are prevented or detected

## 8. Failure matrix

| Failure | Expected behavior |
|---|---|
| One replica is down | Route to healthy replica; increment health/availability metric |
| One shard times out | Retry within deadline or return policy-approved partial results |
| Reranker unavailable | Return fused candidates and mark rerank fallback metric |
| New index checksum fails | Reject activation; retain previous active version |
| Embedding model unavailable | Continue lexical-only if mode/policy permits |
| Query exceeds limits | Return 4xx without expensive processing |
| All shards unavailable | Return controlled 503, not empty successful results |
| Index versions mismatch | Reject activation or flag shard unhealthy |
| Build worker crashes | Keep active version untouched; clean abandoned temporary build safely |

## 9. Decision records

Write an Architecture Decision Record (ADR) whenever a choice has meaningful trade-offs. Include context, options, decision, consequences, and how it will be revisited.
