from datetime import datetime
from typing import Dict, List, Tuple, Optional
import uuid
from .models import Decision, JournalEntry, ReigningBruce, ParliamentState, TemporaryBruce
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
    
    def create_session(self, session_type: str, responses: Dict[str, str], temp_bruce_responses: Optional[Dict[str, str]] = None) -> JournalEntry:
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
            reigning_bruce_name=self.state.reigning_bruce.name if self.state.reigning_bruce else "None",
            temporary_bruce_entries=temp_bruce_responses or {}
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
    
    def add_temporary_bruce(self, name: str, description: str) -> TemporaryBruce:
        """Add a temporary Bruce to the parliament."""
        temp_id = str(uuid.uuid4())[:8]
        temp_bruce = TemporaryBruce(
            id=temp_id,
            name=name,
            description=description
        )
        self.state.temporary_bruces[temp_id] = temp_bruce
        self.save()
        return temp_bruce
    
    def dismiss_temporary_bruce(self, temp_id: str) -> bool:
        """Remove a temporary Bruce from parliament."""
        if temp_id in self.state.temporary_bruces:
            del self.state.temporary_bruces[temp_id]
            self.save()
            return True
        return False
    
    def get_active_temporary_bruces(self) -> List[Tuple[str, TemporaryBruce]]:
        """Get all active temporary bruces."""
        return [(temp_id, bruce) for temp_id, bruce in self.state.temporary_bruces.items() if bruce.active]
    
    def get_all_parliament_seats(self) -> Dict[str, Dict]:
        """Get all permanent seats and temporary bruces for parliament."""
        seats = {}
        
        # Add permanent seats
        permanent = [
            ("ShortTerm", "Short-Term Bruce", "What does your immediate self need?"),
            ("MidTerm", "Mid-Term Bruce", "What should you focus on this week/month?"),
            ("LongTerm", "Long-Term Bruce", "What moves you toward your 5-year vision?"),
            ("Purpose", "Purpose Bruce", "How does today align with your deepest values?"),
            ("Ultimate", "Ultimate Bruce", "What truth must be spoken from the end of your life?"),
        ]
        
        for key, name, prompt in permanent:
            seats[key] = {
                "type": "permanent",
                "name": name,
                "prompt": prompt,
                "has_votes": True
            }
        
        # Add reigning bruce
        if self.state.reigning_bruce:
            seats["Reigning"] = {
                "type": "reigning",
                "name": self.state.reigning_bruce.name,
                "prompt": "Synthesize the parliament's wisdom",
                "has_votes": True
            }
        
        # Add temporary bruces
        for temp_id, temp_bruce in self.get_active_temporary_bruces():
            seats[temp_id] = {
                "type": "temporary",
                "name": temp_bruce.name,
                "prompt": f"[{temp_bruce.description}] What do you say?",
                "has_votes": False,
                "id": temp_id
            }
        
        return seats
    
    def update_temporary_bruce_statement(self, temp_id: str, statement: str) -> bool:
        """Update the last statement of a temporary bruce."""
        if temp_id in self.state.temporary_bruces:
            self.state.temporary_bruces[temp_id].last_statement = statement
            self.save()
            return True
        return False
    
    def collect_rotating_session_responses(self, session_type: str, collect_callback) -> Tuple[Dict[str, str], Dict[str, str]]:
        """
        Collect responses using a rotating discussion format.
        
        Args:
            session_type: Type of session (daily, weekly, etc.)
            collect_callback: Async callback function that takes (seat_key, seat_name, prompt, round_num) and returns response or None to stop
        
        Returns:
            Tuple of (permanent_responses, temporary_responses)
        """
        permanent_responses = {
            "short_term": "",
            "mid_term": "",
            "long_term": "",
            "purpose": "",
            "ultimate": "",
            "reigning": ""
        }
        temporary_responses = {}
        
        # Get all parliament seats
        all_seats = self.get_all_parliament_seats()
        permanent_order = ["ShortTerm", "MidTerm", "LongTerm", "Purpose", "Ultimate", "Reigning"]
        
        # Round-based discussion
        round_num = 1
        while True:
            round_responses_collected = False
            
            # Go through permanent seats in order
            for seat_key in permanent_order:
                if seat_key not in all_seats:
                    continue
                
                seat_info = all_seats[seat_key]
                response = collect_callback(
                    seat_key=seat_key,
                    seat_name=seat_info["name"],
                    prompt=seat_info["prompt"],
                    round_num=round_num,
                    is_first_round=(round_num == 1)
                )
                
                # None return means user wants to stop
                if response is None:
                    break
                
                # Empty string is valid response
                if response is not None:
                    if seat_key == "Reigning":
                        permanent_responses["reigning"] = response
                    else:
                        perm_key = seat_key[0].lower() + seat_key[1:].replace("Term", "_term")
                        if perm_key in permanent_responses:
                            if round_num == 1:
                                permanent_responses[perm_key] = response
                            else:
                                permanent_responses[perm_key] += f"\n\n[Round {round_num}] {response}"
                    round_responses_collected = True
            
            # Go through temporary bruces
            temp_seats = [(k, v) for k, v in all_seats.items() if v.get("type") == "temporary"]
            for temp_key, temp_info in temp_seats:
                response = collect_callback(
                    seat_key=temp_key,
                    seat_name=temp_info["name"],
                    prompt=temp_info["prompt"],
                    round_num=round_num,
                    is_first_round=(round_num == 1)
                )
                
                if response is None:
                    break
                
                if response is not None:
                    if temp_key not in temporary_responses:
                        temporary_responses[temp_key] = response
                    else:
                        temporary_responses[temp_key] += f"\n\n[Round {round_num}] {response}"
                    round_responses_collected = True
            
            # If user chose to stop or no responses collected, break
            if response is None or not round_responses_collected:
                break
            
            round_num += 1
        
        return permanent_responses, temporary_responses
