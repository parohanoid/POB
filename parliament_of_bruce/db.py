from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    JSON,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

from .config import DEFAULT_DB_PATH

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False)


def get_engine(db_path: str = DEFAULT_DB_PATH):
    """Create and return a SQLAlchemy engine."""
    return create_engine(
        f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
    )


def get_session(db_path: str = DEFAULT_DB_PATH):
    """Get a new database session."""
    engine = get_engine(db_path)
    SessionLocal.configure(bind=engine)
    return SessionLocal()


# --- SQLAlchemy ORM Models ---


class Seat(Base):
    __tablename__ = "seats"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    votes = Column(Integer, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    active = Column(Boolean, default=True)
    is_permanent = Column(Boolean, default=True)


class ReigningBruce(Base):
    __tablename__ = "reigning_bruces"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String)
    reason_born = Column(Text)
    exit_report = Column(Text)


class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    session_type = Column(String, nullable=False)
    statements = Column(JSON)
    final_policy = Column(Text)
    decisions_voted_on = Column(JSON, default=[])
    reigning_bruce_id = Column(Integer)


class Decision(Base):
    __tablename__ = "decisions"
    id = Column(Integer, primary_key=True)
    topic = Column(String, nullable=False)
    options = Column(JSON)
    votes = Column(JSON)
    weighted_result = Column(Integer)
    passed = Column(Boolean)
    passed_on = Column(String)


class Law(Base):
    __tablename__ = "laws"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String)
    proposer = Column(String)
    created_on = Column(String)
    status = Column(String)
    votes_history = Column(JSON)
    expiry_date = Column(String)


class Constitution(Base):
    __tablename__ = "constitution"
    id = Column(Integer, primary_key=True)
    core_values = Column(JSON)
    rights = Column(JSON)
    prohibited_actions = Column(JSON)
    amendment_rules = Column(JSON)
    emergency_powers = Column(JSON)


class CustomBruce(Base):
    __tablename__ = "custom_bruces"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    primary_function = Column(String)
    problem_statement = Column(String)
    values = Column(String)
    deliberately_ignore = Column(String)
    tone_of_voice = Column(String)
    allowed_emotional_range = Column(String)
    decision_bias = Column(String)
    votes = Column(Integer)
    expiry_condition = Column(String)
    expiry_value = Column(String)
    created_at = Column(String)
    active = Column(Boolean, default=True)


class EmergencyLog(Base):
    __tablename__ = "emergency_logs"
    id = Column(Integer, primary_key=True)
    timestamp = Column(String)
    trigger_text = Column(Text)
    actions_taken = Column(Text)
    who_initiated = Column(String)
