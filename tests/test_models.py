from groundwork.models import Claim, ResearchQuestion, ResearchState, Source


def test_research_state_starts_empty():
    state = ResearchState("What is the impact of remote work?")
    assert state.is_empty
    assert state.summary()["research_round"] == 0


def test_claim_accepts_valid_confidence():
    claim = Claim(
        text="Remote work changed office demand.",
        source_url="https://example.com/source",
        evidence="The report observed a change in office demand.",
        confidence=0.9,
    )
    assert claim.confidence == 0.9


def test_models_can_be_added_to_state():
    state = ResearchState("Research topic")
    state.subquestions.append(ResearchQuestion("What changed?", priority=1))
    state.sources.append(Source("https://example.com", "Example"))
    state.claims.append(
        Claim("A claim", "https://example.com", "Supporting evidence", 0.8)
    )
    assert state.summary()["subquestions"] == 1
    assert state.summary()["sources"] == 1
    assert state.summary()["claims"] == 1
