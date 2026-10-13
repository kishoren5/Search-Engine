# Operations Runbook

## Service is unhealthy
1. Check liveness and readiness separately.
2. Inspect error rate, active index version, shard health, and recent deploy/build events.
3. Confirm disk space and process memory.
4. If the active index is corrupt or a rollout caused failures, switch to the last validated index version.
5. Preserve logs and benchmark artifacts before restarting.

## One shard is slow
1. Compare per-shard latency and queue depth.
2. Check CPU, RSS, page faults, disk latency, and model load.
3. Verify replica health and index-version consistency.
4. Apply the configured deadline/partial-result policy; do not increase retries blindly.
5. Capture a trace and reproduce with a fixed query set.

## Index build failed
1. Do not modify the active index.
2. Inspect build logs and temporary output.
3. Validate corpus checksum, free disk, schema, and manifest.
4. Remove abandoned temporary output only after confirming it is not active.
5. Re-run validation before activation.

## Release checklist
- CI and quality regression checks pass.
- Index manifest and checksums validate.
- Snapshot/rollback path tested.
- API compatibility reviewed.
- Dashboard and alerts checked.
- Release notes document index format/model changes.
