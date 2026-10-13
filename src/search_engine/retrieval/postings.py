from dataclasses import dataclass, field


@dataclass(slots=True)
class Posting:
    """Represents an occurrence of a term in a document."""
    doc_id: str
    term_frequency: int


@dataclass
class PostingsList:
    """Collection of postings for a specific term."""
    term: str
    postings: list[Posting] = field(default_factory=list)

    @property
    def document_frequency(self) -> int:
        return len(self.postings)

    def add(self, doc_id: str, tf: int) -> None:
        self.postings.append(Posting(doc_id=doc_id, term_frequency=tf))
