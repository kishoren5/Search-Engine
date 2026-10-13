import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class SegmentManifest:
    version: str
    segment_id: str
    corpus_size: int
    total_terms: int
    avg_doc_length: float
    files: dict[str, str]  # filename -> sha256
    created_at: str


def compute_sha256(filepath: str | Path) -> str:
    """Compute hex-encoded SHA-256 checksum of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def verify_manifest(manifest_path: str | Path) -> bool:
    """Verify that all files listed in manifest exist and match their SHA-256 checksums."""
    path = Path(manifest_path)
    if not path.exists():
        return False

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    segment_dir = path.parent
    for fname, expected_hash in data.get("files", {}).items():
        file_path = segment_dir / fname
        if not file_path.exists():
            return False
        if compute_sha256(file_path) != expected_hash:
            return False

    return True
