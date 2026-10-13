# Threat Model

## Assets
- Corpus contents and any user-provided documents
- Query data and access logs
- Index artifacts and model files
- Administrative controls and deployment secrets
- Availability and integrity of search results

## Threats and mitigations
- **Resource exhaustion:** cap query length, `k`, candidate depth, payload size, concurrency, and reranking budget; use deadlines and bounded queues.
- **Index path abuse:** never accept arbitrary filesystem paths from public requests; allow only validated manifest IDs.
- **Administrative misuse:** authenticate and authorize reload/status operations; audit index activation.
- **Sensitive query logging:** avoid raw query logging by default; apply retention and access controls.
- **Corrupt or poisoned corpus:** validate input schema, checksum artifacts, record source provenance, and test parser limits.
- **Dependency compromise:** pin dependencies, scan packages/container images, and update through reviewed changes.
- **Data exposure:** enforce access filters before returning results; ensure snippets do not bypass document permissions.
- **Model failure or latency:** isolate embedding/reranking behind timeouts and a lexical fallback.

## Out of scope unless added
Tenant isolation, document-level ACLs, regulatory compliance, and adversarial ranking resistance require explicit requirements and dedicated tests. Do not claim these protections without implementation evidence.
