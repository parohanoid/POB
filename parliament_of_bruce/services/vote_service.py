"""Vote service for handling parliamentary votes and decisions."""

from datetime import datetime

from ..config import (
    EMERGENCY_THRESHOLD,
    EMERGENCY_WEIGHTS,
    PASSING_THRESHOLD,
    VOTE_WEIGHTS,
)
from ..db import Decision


class VoteService:
    """Handle voting logic and decision recording."""

    def __init__(self, db_session):
        self.db = db_session

    def calculate_vote_result(
        self, votes: dict, is_emergency: bool = False
    ) -> dict:
        """
        Calculate voting result with weights.
        
        Args:
            votes: dict mapping seat name to vote ('yes', 'no', 'abstain')
            is_emergency: if True, use emergency weights
        
        Returns:
            dict with total_yes, total_no, passed, breakdown
        """
        weights = EMERGENCY_WEIGHTS if is_emergency else VOTE_WEIGHTS
        threshold = EMERGENCY_THRESHOLD if is_emergency else PASSING_THRESHOLD

        breakdown = {}
        total_yes = 0
        total_no = 0
        total_abstain = 0

        for seat, vote in votes.items():
            weight = weights.get(seat, 0)
            breakdown[seat] = {
                "vote": vote.lower(),
                "weight": weight,
            }

            if vote.lower() in ["yes", "y", "1"]:
                total_yes += weight
            elif vote.lower() in ["no", "n", "0"]:
                total_no += weight
            else:
                total_abstain += weight

        passed = total_yes >= threshold
        ultimate_veto = (
            is_emergency
            and votes.get("Ultimate Bruce", "").lower() in ["no", "n", "0"]
        )

        if is_emergency and ultimate_veto:
            passed = False

        return {
            "total_yes": total_yes,
            "total_no": total_no,
            "total_abstain": total_abstain,
            "passed": passed,
            "breakdown": breakdown,
            "ultimate_veto": ultimate_veto if is_emergency else False,
        }

    def create_decision(
        self,
        topic: str,
        options: list,
        votes: dict,
        is_emergency: bool = False,
    ) -> int:
        """
        Create a decision record and return its ID.
        """
        result = self.calculate_vote_result(votes, is_emergency)

        decision = Decision(
            topic=topic,
            options=options,
            votes=votes,
            weighted_result=result["total_yes"],
            passed=result["passed"],
            passed_on=datetime.now().isoformat(),
        )

        self.db.add(decision)
        self.db.commit()

        return decision.id

    def get_decision(self, decision_id: int) -> Decision | None:
        """Retrieve a decision by ID."""
        return self.db.query(Decision).filter_by(id=decision_id).first()

    def list_decisions(self, limit: int = 10) -> list:
        """Get recent decisions."""
        return (
            self.db.query(Decision).order_by(Decision.id.desc()).limit(limit).all()
        )
