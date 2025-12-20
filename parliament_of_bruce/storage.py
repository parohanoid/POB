import json
from pathlib import Path
from typing import Optional
from .models import ParliamentState, Seat, ReigningBruce, TemporaryBruce


class Storage:
    """Handles persistence of parliament data."""
    
    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            data_dir = Path.home() / ".parliament_of_bruce"
        
        self.data_dir = data_dir
        self.data_file = data_dir / "parliament_data.json"
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def load(self) -> ParliamentState:
        """Load parliament state from disk."""
        if not self.data_file.exists():
            return self._create_initial_state()
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            # Backward compatibility: ensure temporary_bruces key exists
            if "temporary_bruces" not in data:
                data["temporary_bruces"] = {}
            
            # Backward compatibility: ensure temporary_bruce_entries in journal entries
            if "journal_entries" in data:
                for entry in data["journal_entries"]:
                    if "temporary_bruce_entries" not in entry:
                        entry["temporary_bruce_entries"] = {}
            
            return ParliamentState(**data)
        except Exception as e:
            print(f"Error loading data: {e}")
            return self._create_initial_state()
    
    def save(self, state: ParliamentState) -> None:
        """Save parliament state to disk."""
        with open(self.data_file, 'w') as f:
            json.dump(state.dict(), f, indent=2)
    
    def _create_initial_state(self) -> ParliamentState:
        """Create initial parliament state with permanent seats."""
        seats = {
            "ShortTerm": Seat(
                name="Short-Term Bruce — The Rebel / The Animal",
                votes=1,
                description="Time: now, today, tonight\nBody over mind. Nerves over plans.\n\n'I want relief, not reasons. Pain feels urgent and personal. Boredom is death. Discipline feels like a cage. I don't care about later. I speak in cravings, anger, fear. If ignored, I sabotage. I tell the raw truth others hide.'\n\nActivation: What hurts right now, and what would make it stop?"
            ),
            "MidTerm": Seat(
                name="Mid-Term Bruce — The Operator",
                votes=2,
                description="Time: this week, this month\nExecution over emotion.\n\n'I care about momentum. Small wins beat grand visions. Systems beat willpower. Burnout is my enemy. Chaos wastes energy. I translate emotion into tasks. I ask: what's doable, not ideal. Consistency is power.'\n\nActivation: What's the minimum action that moves this forward?"
            ),
            "LongTerm": Seat(
                name="Long-Term Bruce — The Architect",
                votes=3,
                description="Time: years ahead\nStructure over impulse.\n\n'I think in systems and leverage. Compounding is sacred. Short-term pleasure is expensive. I sacrifice now to own later. I care about trajectory, not mood. Emotions are data, not commands. I design environments, not days. Waste of potential is the real sin.'\n\nActivation: Does this scale, compound, or rot?"
            ),
            "Purpose": Seat(
                name="Purpose Bruce — The Dharma Bearer",
                votes=4,
                description="Time: lifetime\nMeaning over success.\n\n'I guard the story of your life. Power without meaning is hollow. Pain must become purpose. I ask why before how. Betraying values costs more than failure. I see patterns across incarnations of you. I don't rush, I judge alignment. I speak softly but halt everything.'\n\nActivation: Is this worthy of the story we're living?"
            ),
            "Ultimate": Seat(
                name="Ultimate Bruce — The Judge",
                votes=5,
                description="Time: deathbed\nLegacy over everything.\n\n'I am immune to excuses. I don't care how it felt, only what it became. Regret is my metric. I veto actions you'll have to live with forever. Comfort now can mean shame later. I see your entire life as one object. I end arguments.'\n\nActivation: When this is over… will we respect this choice?"
            ),
        }
        
        return ParliamentState(seats=seats)
