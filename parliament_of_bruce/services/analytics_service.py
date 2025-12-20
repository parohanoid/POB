"""Analytics service for computing dominance scores and trends."""

from datetime import datetime, timedelta

from ..db import Decision, Session


class AnalyticsService:
    """Compute analytics on parliament activity."""

    def __init__(self, db_session):
        self.db = db_session

    def get_dominance_scores(self, days: int = 7) -> dict:
        """
        Compute seat dominance scores over last N days.
        Returns dict mapping seat name to dominance score.
        """
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()

        sessions = (
            self.db.query(Session)
            .filter(Session.date >= cutoff)
            .order_by(Session.date)
            .all()
        )

        dominance = {
            "short_term": 0,
            "mid_term": 0,
            "long_term": 0,
            "purpose": 0,
            "ultimate": 0,
        }

        for session in sessions:
            statements = session.statements or {}
            for key in dominance:
                if key in statements and statements[key]:
                    # Weight by length
                    dominance[key] += len(statements[key])

        return dominance

    def get_speaking_frequency(self, days: int = 7) -> dict:
        """
        Count how many sessions each seat spoke in (gave non-empty statements).
        """
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()

        sessions = (
            self.db.query(Session)
            .filter(Session.date >= cutoff)
            .order_by(Session.date)
            .all()
        )

        frequency = {
            "short_term": 0,
            "mid_term": 0,
            "long_term": 0,
            "purpose": 0,
            "ultimate": 0,
        }

        for session in sessions:
            statements = session.statements or {}
            for key in frequency:
                if key in statements and len(statements[key]) > 0:
                    frequency[key] += 1

        return frequency

    def get_voting_dominance(self, days: int = 7) -> dict:
        """
        Compute weighted voting power executed by each seat over N days.
        """
        from ..config import VOTE_WEIGHTS

        cutoff = (datetime.now() - timedelta(days=days)).isoformat()

        decisions = (
            self.db.query(Decision)
            .filter(Decision.passed_on >= cutoff)
            .order_by(Decision.passed_on)
            .all()
        )

        dominance = {}
        for seat in VOTE_WEIGHTS:
            dominance[seat] = 0

        for decision in decisions:
            votes = decision.votes or {}
            for seat, vote in votes.items():
                if vote.lower() in ["yes", "y", "1"] and seat in VOTE_WEIGHTS:
                    dominance[seat] += VOTE_WEIGHTS[seat]

        return dominance

    def get_trends(self, window_days: int = 7) -> dict:
        """
        Compare current period to previous period and return trend indicators.
        Returns dict with seat -> (trend_direction: 'up'|'down'|'stable', change: int)
        """
        current = self.get_dominance_scores(days=window_days)
        previous = self.get_dominance_scores(
            days=window_days * 2
        )  # Approximate previous period

        trends = {}
        for seat in current:
            current_val = current.get(seat, 0)
            previous_val = previous.get(seat, 0)

            if previous_val == 0:
                change = current_val
                direction = "up" if current_val > 0 else "stable"
            else:
                change = current_val - previous_val
                if change > 0:
                    direction = "up"
                elif change < 0:
                    direction = "down"
                else:
                    direction = "stable"

            trends[seat] = {
                "direction": direction,
                "change": change,
            }

        return trends

    def get_analytics_summary(self, days: int = 7) -> dict:
        """Generate a complete analytics summary."""
        return {
            "period_days": days,
            "dominance_scores": self.get_dominance_scores(days),
            "speaking_frequency": self.get_speaking_frequency(days),
            "voting_dominance": self.get_voting_dominance(days),
            "trends": self.get_trends(days),
        }
