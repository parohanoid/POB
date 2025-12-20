from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# Pydantic models for validation and serialization

class SeatModel(BaseModel):
    id: Optional[int] = None
    name: str
    votes: int
    description: str
    created_at: Optional[datetime] = None
    active: bool = True
    is_permanent: bool = True

    class Config:
        from_attributes = True


class ReigningBruceModel(BaseModel):
    id: Optional[int] = None
    name: str
    start_date: str
    end_date: Optional[str] = None
    reason_born: str
    exit_report: Optional[str] = None

    class Config:
        from_attributes = True


class SessionModel(BaseModel):
    id: Optional[int] = None
    date: str
    session_type: str
    statements: Dict[str, str]
    final_policy: str
    decisions_voted_on: List[int] = Field(default_factory=list)
    reigning_bruce_id: Optional[int] = None

    class Config:
        from_attributes = True


class DecisionModel(BaseModel):
    id: Optional[int] = None
    topic: str
    options: List[str]
    votes: Dict[str, str]
    weighted_result: int
    passed: bool
    passed_on: str

    class Config:
        from_attributes = True


class LawModel(BaseModel):
    id: Optional[int] = None
    name: str
    type: str
    proposer: str
    created_on: str
    status: str
    votes_history: List[Dict[str, Any]] = Field(default_factory=list)
    expiry_date: Optional[str] = None

    class Config:
        from_attributes = True


class ConstitutionModel(BaseModel):
    core_values: List[str]
    rights: Dict[str, str]
    prohibited_actions: List[str]
    amendment_rules: Dict[str, Any]
    emergency_powers: Dict[str, Any]


class CustomBruceModel(BaseModel):
    id: Optional[int] = None
    name: str
    primary_function: str
    problem_statement: str
    values: str
    deliberately_ignore: str
    tone_of_voice: str
    allowed_emotional_range: str
    decision_bias: str
    votes: int
    expiry_condition: str
    expiry_value: str
    created_at: Optional[str] = None
    active: bool = True

    class Config:
        from_attributes = True


class EmergencyLogModel(BaseModel):
    id: Optional[int] = None
    timestamp: str
    trigger_text: str
    actions_taken: str
    who_initiated: str

    class Config:
        from_attributes = True


# Legacy models for backward compatibility with JSON import
class Seat(BaseModel):
    """Represents a permanent parliament seat."""
    name: str
    votes: int
    description: str
    last_statement: str = ""
    active: bool = True


class ReigningBruce(BaseModel):
    """Represents the current identity version."""
    name: str
    start_date: str
    reason_born: str
    end_date: Optional[str] = None
    exit_report: Optional[str] = None
    session_count: int = 0


class Decision(BaseModel):
    """Represents a voted-upon decision."""
    topic: str
    options: List[str]
    votes: Dict[str, str]
    total_score: int
    scores_breakdown: Dict[str, int]
    passed: bool
    timestamp: str


class JournalEntry(BaseModel):
    """Represents a parliament session entry."""
    date: str
    session_type: str
    short_term: str
    mid_term: str
    long_term: str
    purpose: str
    ultimate: str
    reigning: str
    final_policy: str
    decisions_voted_on: List[Decision] = Field(default_factory=list)
    reigning_bruce_name: str = ""


class ParliamentState(BaseModel):
    """Complete state of the parliament system."""
    seats: Dict[str, Seat]
    reigning_bruce: Optional[ReigningBruce] = None
    bruce_history: List[ReigningBruce] = Field(default_factory=list)
    journal_entries: List[JournalEntry] = Field(default_factory=list)
    decisions: List[Decision] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
