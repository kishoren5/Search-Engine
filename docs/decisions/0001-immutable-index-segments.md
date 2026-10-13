# ADR 0001: Immutable index segments

- Status: Proposed
- Context: In-place mutation makes rollback, validation, and concurrent query safety harder.
- Decision: Build a new immutable index version, validate it, and activate it atomically through a manifest/pointer.
- Consequences: Requires temporary disk space and version cleanup; simplifies rollback and reader safety.
- Revisit when: incremental indexing and update freshness requirements are defined.
