import hashlib


class Deduplicator:
    """Detects duplicate and near-duplicate documents via 64-bit content fingerprints."""

    def __init__(self) -> None:
        self.seen_hashes: set[int] = set()
        self.duplicates_count: int = 0

    def compute_fingerprint(self, text: str) -> int:
        """Compute 64-bit integer hash of normalized text."""
        h = hashlib.sha256(text.encode("utf-8")).digest()
        # Take first 8 bytes as unsigned 64-bit int
        return int.from_bytes(h[:8], byteorder="big")

    def is_duplicate(self, text: str) -> bool:
        """Check if document text has been seen before; if not, marks it as seen."""
        fp = self.compute_fingerprint(text)
        if fp in self.seen_hashes:
            self.duplicates_count += 1
            return True
        self.seen_hashes.add(fp)
        return False

    def reset(self) -> None:
        self.seen_hashes.clear()
        self.duplicates_count = 0
