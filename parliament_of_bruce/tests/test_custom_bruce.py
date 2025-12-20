"""Tests for custom Bruce lifecycle."""

import pytest

from parliament_of_bruce.db import Base, CustomBruce, get_engine, get_session
from parliament_of_bruce.services.custom_bruce_service import CustomBruceService


@pytest.fixture
def db_session(tmp_path):
    """Create an in-memory test database."""
    db_path = str(tmp_path / "test.db")
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)
    session = get_session(db_path)
    yield session
    session.close()


def test_create_custom_bruce(db_session):
    """Test creating a custom Bruce."""
    service = CustomBruceService(db_session)

    custom_id = service.create_custom_bruce(
        name="Project Bruce",
        primary_function="Focus on project delivery",
        problem_statement="Team needs clear direction",
        values="Clarity, efficiency, results",
        deliberately_ignore="Perfectionism",
        tone_of_voice="Direct and action-oriented",
        allowed_emotional_range="Confident to determined",
        decision_bias="Toward fast execution",
        votes=2,
        expiry_condition="time-based",
        expiry_value="14",
    )

    assert custom_id is not None

    custom = db_session.query(CustomBruce).filter_by(id=custom_id).first()
    assert custom is not None
    assert custom.name == "Project Bruce"
    assert custom.active is True


def test_max_two_custom_bruces(db_session):
    """Test that max 2 custom Bruces can be active."""
    service = CustomBruceService(db_session)

    # Create first custom Bruce
    service.create_custom_bruce(
        name="Project Bruce",
        primary_function="Focus",
        problem_statement="Clear direction",
        values="Clarity",
        deliberately_ignore="None",
        tone_of_voice="Direct",
        allowed_emotional_range="Confident",
        decision_bias="Fast execution",
        votes=2,
        expiry_condition="manual",
        expiry_value="",
    )

    # Create second custom Bruce
    service.create_custom_bruce(
        name="Creative Bruce",
        primary_function="Innovation",
        problem_statement="New ideas",
        values="Creativity",
        deliberately_ignore="Constraints",
        tone_of_voice="Playful",
        allowed_emotional_range="Curious",
        decision_bias="Exploration",
        votes=1,
        expiry_condition="manual",
        expiry_value="",
    )

    # Attempt to create third should fail
    with pytest.raises(ValueError):
        service.create_custom_bruce(
            name="Third Bruce",
            primary_function="Conflict",
            problem_statement="More",
            values="X",
            deliberately_ignore="Y",
            tone_of_voice="Z",
            allowed_emotional_range="A",
            decision_bias="B",
            votes=1,
            expiry_condition="manual",
            expiry_value="",
        )


def test_dismiss_custom_bruce(db_session):
    """Test dismissing a custom Bruce."""
    service = CustomBruceService(db_session)

    custom_id = service.create_custom_bruce(
        name="Project Bruce",
        primary_function="Focus",
        problem_statement="Clear direction",
        values="Clarity",
        deliberately_ignore="None",
        tone_of_voice="Direct",
        allowed_emotional_range="Confident",
        decision_bias="Fast execution",
        votes=2,
        expiry_condition="manual",
        expiry_value="",
    )

    service.dismiss_custom_bruce(custom_id)

    custom = db_session.query(CustomBruce).filter_by(id=custom_id).first()
    assert custom.active is False
