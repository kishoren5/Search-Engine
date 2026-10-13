import csv
import gzip
import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any


def stream_jsonl(filepath: str | Path) -> Iterator[dict[str, Any]]:
    """Stream documents line-by-line from uncompressed or gzipped JSONL files."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Corpus file not found: {path}")

    opener = gzip.open if path.suffix == ".gz" else open

    with opener(path, "rt", encoding="utf-8", errors="replace") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                record["doc_id"] = str(record.get("doc_id", record.get("id", f"doc_{line_num}")))
                record["title"] = str(record.get("title", ""))
                record["text"] = str(record.get("text", record.get("content", record.get("body", ""))))
                record["url"] = str(record.get("url", ""))
                yield record
            except json.JSONDecodeError:
                continue


def stream_csv(
    filepath: str | Path,
    id_col: str = "doc_id",
    text_col: str = "text",
    title_col: str = "title",
    url_col: str = "url",
) -> Iterator[dict[str, Any]]:
    """Stream documents row-by-row from CSV file."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Corpus file not found: {path}")

    opener = gzip.open if path.suffix == ".gz" else open

    with opener(path, "rt", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=1):
            yield {
                "doc_id": str(row.get(id_col, f"doc_{row_num}")),
                "title": str(row.get(title_col, "")),
                "text": str(row.get(text_col, "")),
                "url": str(row.get(url_col, "")),
            }
