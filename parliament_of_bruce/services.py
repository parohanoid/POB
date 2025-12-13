from datetime import datetime
from typing import Dict, List, Tuple
from .models import Decision, JournalEntry, ReigningBruce, ParliamentState
from .storage import Storage


class ParliamentService:
    """Core business logic for parliament operations."""
    
    VOTE_WEIGHTS = {
        "ShortTerm": 1,
        "MidTerm": 2,
        "LongTerm": 3,
        "Purpose": 4,
        "Ultimate": 5,
        "Reigning": 3,
    }
    
    PASSING_THRESHOLD = 10
    MAX_SCORE = 18
    
    def __init__(self, storage: Storage):
        self.storage = storage
        self.state = storage.load()
    
    def save(self):
        """Save current state."""
        self.storage.save(self.state)
    
    def create_session(self, session_type: str, responses: Dict[str, str]) -> JournalEntry:
        """Create a new journal entry from session responses."""
        entry = JournalEntry(
            date=datetime.now().isoformat(),
            session_type=session_type,
            short_term=responses.get("short_term", ""),
            mid_term=responses.get("mid_term", ""),
            long_term=responses.get("long_term", ""),
            purpose=responses.get("purpose", ""),
            ultimate=responses.get("ultimate", ""),
            reigning=responses.get("reigning", ""),
            final_policy=responses.get("final_policy", ""),
            reigning_bruce_name=self.state.reigning_bruce.name if self.state.reigning_bruce else "None"
        )
        
        self.state.journal_entries.append(entry)
        
        if self.state.reigning_bruce:
            self.state.reigning_bruce.session_count += 1
        
        self.save()
        return entry
    
    def vote_on_decision(self, topic: str, options: List[str], votes: Dict[str, str]) -> Decision:
        """Process a vote and return the decision result."""
        scores_breakdown = {}
        total_yes = 0
        total_no = 0
        
        for seat, vote in votes.items():
            weight = self.VOTE_WEIGHTS.get(seat, 0)
            scores_breakdown[seat] = weight
            
            if vote.lower() in ["yes", "y", "1"]:
                total_yes += weight
            else:
                total_no += weight
        
        decision = Decision(
            topic=topic,
            options=options,
            votes=votes,
            total_score=self.MAX_SCORE,
            scores_breakdown=scores_breakdown,
            passed=total_yes >= self.PASSING_THRESHOLD,
            timestamp=datetime.now().isoformat()
        )
        
        self.state.decisions.append(decision)
        self.save()
        return decision
    
    def create_reigning_bruce(self, name: str, reason: str) -> ReigningBruce:
        """Create a new reigning Bruce identity."""
        # Archive current Bruce if exists
        if self.state.reigning_bruce:
            self.state.bruce_history.append(self.state.reigning_bruce)
        
        new_bruce = ReigningBruce(
            name=name,
            start_date=datetime.now().isoformat(),
            reason_born=reason
        )
        
        self.state.reigning_bruce = new_bruce
        self.save()
        return new_bruce
    
    def end_reigning_bruce(self, exit_report: str) -> None:
        """End the current Bruce's reign."""
        if self.state.reigning_bruce:
            self.state.reigning_bruce.end_date = datetime.now().isoformat()
            self.state.reigning_bruce.exit_report = exit_report
            self.state.bruce_history.append(self.state.reigning_bruce)
            self.state.reigning_bruce = None
            self.save()
    
    def get_recent_entries(self, count: int = 3) -> List[JournalEntry]:
        """Get most recent journal entries."""
        return self.state.journal_entries[-count:] if self.state.journal_entries else []
    
    def analyze_seat_dominance(self, days: int = 7) -> Dict[str, int]:
        """Analyze which seats have been most dominant recently."""
        # Simplified analysis - count non-empty responses
        recent = self.state.journal_entries[-days:] if len(self.state.journal_entries) >= days else self.state.journal_entries
        
        dominance = {
            "short_term": 0,
            "mid_term": 0,
            "long_term": 0,
            "purpose": 0,
            "ultimate": 0
        }
        
        for entry in recent:
            if len(entry.short_term) > 50:
                dominance["short_term"] += 1
            if len(entry.mid_term) > 50:
                dominance["mid_term"] += 1
            if len(entry.long_term) > 50:
                dominance["long_term"] += 1
            if len(entry.purpose) > 50:
                dominance["purpose"] += 1
            if len(entry.ultimate) > 50:
                dominance["ultimate"] += 1
        
        return dominance
    
    def generate_warnings(self) -> List[str]:
        """Generate behavioral warnings based on recent patterns."""
        warnings = []
        dominance = self.analyze_seat_dominance()
        
        total = sum(dominance.values())
        if total == 0:
            return ["⚠️  No recent parliament activity detected"]
        
        # Check for Short-Term dominance
        if dominance["short_term"] / total > 0.5:
            warnings.append("⚠️  Short-Term Bruce is dominating decisions. Consider long-term consequences.")
        
        # Check for Purpose silence
        if dominance["purpose"] / total < 0.1:
            warnings.append("⚠️  Purpose Bruce has been silent. Risk of existential drift.")
        
        # Check for Ultimate silence
        if dominance["ultimate"] / total < 0.05:
            warnings.append("⚠️  Ultimate Bruce is not being consulted. Death-aware wisdom is missing.")
        
        return warnings if warnings else ["✓ Parliament balance appears healthy"]
