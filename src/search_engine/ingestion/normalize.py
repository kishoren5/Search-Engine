import re
import unicodedata

HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
WHITESPACE_PATTERN = re.compile(r"\s+")


def clean_text(raw_text: str, strip_html: bool = True) -> str:
    """Normalize text: strip HTML tags, normalize unicode to NFKC, collapse whitespace."""
    if not raw_text:
        return ""

    text = raw_text
    if strip_html:
        text = HTML_TAG_PATTERN.sub(" ", text)

    # Unicode NFKC normalization
    text = unicodedata.normalize("NFKC", text)

    # Collapse multiple whitespaces and trim
    text = WHITESPACE_PATTERN.sub(" ", text).strip()
    return text
