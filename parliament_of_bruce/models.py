from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class Seat(BaseModel):
    """Represents a permanent parliament seat."""
    name: str
    votes: int
    description: str
    last_statement: str = ""
    active: bool = True


class TemporaryBruce(BaseModel):
    """Represents a temporary Bruce voice in parliament - no voting rights."""
    id: str
    name: str
    description: str
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
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
    temporary_bruce_entries: Dict[str, str] = Field(default_factory=dict)  # {temp_bruce_id: response}


class ParliamentState(BaseModel):
    """Complete state of the parliament system."""
    seats: Dict[str, Seat]
    reigning_bruce: Optional[ReigningBruce] = None
    bruce_history: List[ReigningBruce] = Field(default_factory=list)
    journal_entries: List[JournalEntry] = Field(default_factory=list)
    decisions: List[Decision] = Field(default_factory=list)
    temporary_bruces: Dict[str, TemporaryBruce] = Field(default_factory=dict)  # {id: TemporaryBruce}
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
