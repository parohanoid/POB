"""Tests for voting and decision-making."""

import pytest

from parliament_of_bruce.db import Base, Seat, get_engine, get_session
from parliament_of_bruce.services.vote_service import VoteService


@pytest.fixture
def db_session(tmp_path):
    """Create an in-memory test database."""
    db_path = str(tmp_path / "test.db")
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)
    session = get_session(db_path)
    yield session
    session.close()


@pytest.fixture
def seeded_session(db_session):
    """Seed with default seats."""
    seats = [
        Seat(name="Short-Term Bruce", votes=1, description="Short", is_permanent=True),
        Seat(name="Mid-Term Bruce", votes=2, description="Mid", is_permanent=True),
        Seat(name="Long-Term Bruce", votes=3, description="Long", is_permanent=True),
        Seat(name="Purpose Bruce", votes=4, description="Purpose", is_permanent=True),
        Seat(name="Ultimate Bruce", votes=5, description="Ultimate", is_permanent=True),
        Seat(name="Reigning Bruce", votes=3, description="Reigning", is_permanent=True),
    ]
    for seat in seats:
        db_session.add(seat)
    db_session.commit()
    return db_session


def test_vote_passes(seeded_session):
    """Test a vote that passes."""
    service = VoteService(seeded_session)

    votes = {
        "Short-Term Bruce": "yes",
        "Mid-Term Bruce": "yes",
        "Long-Term Bruce": "yes",
        "Purpose Bruce": "yes",
        "Ultimate Bruce": "yes",
        "Reigning Bruce": "no",
    }

    result = service.calculate_vote_result(votes)

    # 1 + 2 + 3 + 4 + 5 = 15 yes
    assert result["total_yes"] == 15
    assert result["total_no"] == 3
    assert result["passed"] is True


def test_vote_fails(seeded_session):
    """Test a vote that fails."""
    service = VoteService(seeded_session)

    votes = {
        "Short-Term Bruce": "yes",
        "Mid-Term Bruce": "no",
        "Long-Term Bruce": "no",
        "Purpose Bruce": "no",
        "Ultimate Bruce": "no",
        "Reigning Bruce": "no",
    }

    result = service.calculate_vote_result(votes)

    # 1 yes = < 10 threshold
    assert result["total_yes"] == 1
    assert result["passed"] is False


def test_create_decision(seeded_session):
    """Test creating a decision record."""
    service = VoteService(seeded_session)

    votes = {
        "Short-Term Bruce": "yes",
        "Mid-Term Bruce": "yes",
        "Long-Term Bruce": "yes",
        "Purpose Bruce": "yes",
        "Ultimate Bruce": "yes",
        "Reigning Bruce": "yes",
    }

    decision_id = service.create_decision(
        topic="Accept new job offer",
        options=["yes", "no"],
        votes=votes,
    )

    assert decision_id is not None

    decision = service.get_decision(decision_id)
    assert decision is not None
    assert decision.topic == "Accept new job offer"
    assert decision.passed is True
