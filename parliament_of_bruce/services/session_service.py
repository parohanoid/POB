"""Session service for conducting parliamentary sessions and journaling."""

import json
import os
from datetime import datetime

from ..config import DEFAULT_LOGS_DIR, EMERGENCY_KEYWORDS
from ..db import EmergencyLog, Session


class SessionService:
    """Handle session creation, storage, and emergency detection."""

    def __init__(self, db_session):
        self.db = db_session
        self._ensure_logs_dir()

    @staticmethod
    def _ensure_logs_dir():
        os.makedirs(DEFAULT_LOGS_DIR, exist_ok=True)

    def create_session(
        self,
        date: str,
        session_type: str,
        statements: dict,
        final_policy: str,
        reigning_bruce_id: int | None = None,
    ) -> int:
        """
        Create a new session record.
        Returns session ID.
        """
        session = Session(
            date=date,
            session_type=session_type,
            statements=statements,
            final_policy=final_policy,
            decisions_voted_on=[],
            reigning_bruce_id=reigning_bruce_id,
        )
        self.db.add(session)
        self.db.commit()
        return session.id

    def check_emergency_trigger(self, text: str) -> bool:
        """
        Check if emergency keywords appear in text.
        """
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in EMERGENCY_KEYWORDS)

    def log_emergency(
        self, trigger_text: str, actions_taken: str, who_initiated: str
    ):
        """Log an emergency event (immutable append-only)."""
        log_entry = EmergencyLog(
            timestamp=datetime.now().isoformat(),
            trigger_text=trigger_text,
            actions_taken=actions_taken,
            who_initiated=who_initiated,
        )
        self.db.add(log_entry)
        self.db.commit()

        # Also write to file log
        log_file = os.path.join(DEFAULT_LOGS_DIR, "emergency.jsonl")
        with open(log_file, "a") as f:
            f.write(
                json.dumps(
                    {
                        "timestamp": log_entry.timestamp,
                        "trigger_text": trigger_text,
                        "actions_taken": actions_taken,
                        "who_initiated": who_initiated,
                    }
                )
                + "\n"
            )

    def get_recent_sessions(self, count: int = 3) -> list:
        """Get the most recent N sessions."""
        return self.db.query(Session).order_by(Session.id.desc()).limit(count).all()

    def generate_weekly_summary(self, sessions: list) -> dict:
        """Generate analytics for a week of sessions."""
        if not sessions:
            return {
                "total_sessions": 0,
                "dominance_scores": {},
                "warnings": [],
            }

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
                if key in statements and len(statements[key]) > 50:
                    dominance[key] += 1

        total = sum(dominance.values())
        warnings = []

        if total == 0:
            warnings.append("⚠️  No significant parliament activity detected")
        else:
            # Check for dominance patterns
            if dominance["short_term"] / total > 0.5:
                warnings.append(
                    "⚠️  Short-Term Bruce dominance. Consider long-term consequences."
                )
            if dominance["purpose"] / total < 0.1:
                warnings.append("⚠️  Purpose Bruce silence. Risk of existential drift.")
            if dominance["ultimate"] / total < 0.05:
                warnings.append("⚠️  Ultimate Bruce not consulted. Lacking death-aware wisdom.")

        return {
            "total_sessions": len(sessions),
            "dominance_scores": dominance,
            "warnings": warnings if warnings else ["✓ Parliament balance appears healthy"],
        }
