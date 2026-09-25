"""Structured domain models shared by GroundWork components."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ResearchQuestion:
    question: str
    rationale: str = ""
    priority: int = 1
    status: str = "pending"

    def __post_init__(self) -> None:
        if not self.question.strip():
            raise ValueError("ResearchQuestion.question cannot be empty.")
        if self.priority < 1:
            raise ValueError("ResearchQuestion.priority must be >= 1.")


@dataclass
class Source:
    url: str
    title: str
    snippet: str = ""
    content: str = ""
    source_type: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.url.strip():
            raise ValueError("Source.url cannot be empty.")
        if not self.title.strip():
            raise ValueError("Source.title cannot be empty.")


@dataclass
class Claim:
    text: str
    source_url: str
    evidence: str
    confidence: float = 0.0
    question: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("Claim.text cannot be empty.")
        if not self.source_url.strip():
            raise ValueError("Claim.source_url cannot be empty.")
        if not self.evidence.strip():
            raise ValueError("Claim.evidence cannot be empty.")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Claim.confidence must be between 0 and 1.")


@dataclass
class ResearchState:
    """Mutable state passed between agents during a research run."""

    original_question: str
    subquestions: list[ResearchQuestion] = field(default_factory=list)
    sources: list[Source] = field(default_factory=list)
    claims: list[Claim] = field(default_factory=list)
    unresolved_questions: list[str] = field(default_factory=list)
    contradictions: list[str] = field(default_factory=list)
    research_round: int = 0

    def __post_init__(self) -> None:
        if not self.original_question.strip():
            raise ValueError("original_question cannot be empty.")

    @property
    def is_empty(self) -> bool:
        return not self.subquestions and not self.sources and not self.claims

    def summary(self) -> dict[str, int]:
        return {
            "subquestions": len(self.subquestions),
            "sources": len(self.sources),
            "claims": len(self.claims),
            "unresolved_questions": len(self.unresolved_questions),
            "contradictions": len(self.contradictions),
            "research_round": self.research_round,
        }
