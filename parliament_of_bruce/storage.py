import json
from pathlib import Path
from typing import Optional
from .models import ParliamentState, Seat, ReigningBruce


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
                name="Short-Term Bruce",
                votes=1,
                description="Focused on immediate needs, pleasure, survival instincts"
            ),
            "MidTerm": Seat(
                name="Mid-Term Bruce",
                votes=2,
                description="Planning weeks/months ahead, career moves, relationships"
            ),
            "LongTerm": Seat(
                name="Long-Term Bruce",
                votes=3,
                description="Years-ahead vision, legacy building, strategic positioning"
            ),
            "Purpose": Seat(
                name="Purpose Bruce",
                votes=4,
                description="Life meaning, values alignment, existential direction"
            ),
            "Ultimate": Seat(
                name="Ultimate Bruce",
                votes=5,
                description="Death-aware wisdom, final chapter perspective, truth above all"
            ),
        }
        
        return ParliamentState(seats=seats)
