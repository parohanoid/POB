"""Tests for session creation and journaling."""

import pytest

from parliament_of_bruce.db import Base, Seat, Session, get_engine, get_session
from parliament_of_bruce.services.session_service import SessionService


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
    ]
    for seat in seats:
        db_session.add(seat)
    db_session.commit()
    return db_session


def test_create_session(seeded_session):
    """Test creating a session."""
    service = SessionService(seeded_session)

    session_id = service.create_session(
        date="2025-12-19T10:00:00",
        session_type="daily",
        statements={
            "short_term": "Coffee and focus",
            "mid_term": "Complete project",
            "long_term": "Build skills",
            "purpose": "Growth and discipline",
            "ultimate": "Aligned with values",
        },
        final_policy="Stay consistent and healthy",
    )

    assert session_id is not None

    session_obj = seeded_session.query(Session).filter_by(id=session_id).first()
    assert session_obj is not None
    assert session_obj.session_type == "daily"
    assert session_obj.final_policy == "Stay consistent and healthy"


def test_emergency_keyword_detection(seeded_session):
    """Test emergency keyword detection."""
    service = SessionService(seeded_session)

    assert service.check_emergency_trigger("I want to kill myself") is True
    assert service.check_emergency_trigger("suicide is an option") is True
    assert service.check_emergency_trigger("I can't go on") is True
    assert service.check_emergency_trigger("Just a normal day") is False


def test_weekly_summary(seeded_session):
    """Test weekly summary generation."""
    service = SessionService(seeded_session)

    # Create multiple sessions
    for i in range(3):
        service.create_session(
            date=f"2025-12-{19+i}T10:00:00",
            session_type="daily",
            statements={
                "short_term": "Coffee and focus" * 5,
                "mid_term": "Complete project" * 3,
                "long_term": "Build skills" * 2,
                "purpose": "Growth",
                "ultimate": "Aligned",
            },
            final_policy="Stay consistent",
        )

    sessions = service.get_recent_sessions(count=10)
    summary = service.generate_weekly_summary(sessions)

    assert summary["total_sessions"] == 3
    assert "dominance_scores" in summary
    assert "warnings" in summary
