"""Custom Bruce service for managing temporary extraordinary seats."""

from datetime import datetime

from ..db import CustomBruce


class CustomBruceService:
    """Handle custom Bruce creation, expiry, and rules enforcement."""

    def __init__(self, db_session):
        self.db = db_session

    def create_custom_bruce(
        self,
        name: str,
        primary_function: str,
        problem_statement: str,
        values: str,
        deliberately_ignore: str,
        tone_of_voice: str,
        allowed_emotional_range: str,
        decision_bias: str,
        votes: int,
        expiry_condition: str,
        expiry_value: str,
    ) -> int:
        """
        Create a custom Bruce.
        Returns custom Bruce ID.
        """
        # Check max 2 active custom seats
        active_count = (
            self.db.query(CustomBruce).filter_by(active=True).count()
        )
        if active_count >= 2:
            raise ValueError("Maximum 2 custom Bruces can be active simultaneously")

        # Check combined voting power <= 3
        total_votes = votes
        other_customs = self.db.query(CustomBruce).filter_by(active=True).all()
        for other in other_customs:
            total_votes += other.votes

        if total_votes > 3:
            raise ValueError("Combined custom voting power cannot exceed 3")

        custom_bruce = CustomBruce(
            name=name,
            primary_function=primary_function,
            problem_statement=problem_statement,
            values=values,
            deliberately_ignore=deliberately_ignore,
            tone_of_voice=tone_of_voice,
            allowed_emotional_range=allowed_emotional_range,
            decision_bias=decision_bias,
            votes=votes,
            expiry_condition=expiry_condition,
            expiry_value=expiry_value,
            created_at=datetime.now().isoformat(),
            active=True,
        )

        self.db.add(custom_bruce)
        self.db.commit()
        return custom_bruce.id

    def dismiss_custom_bruce(self, custom_id: int, reason: str = "") -> bool:
        """Dismiss a custom Bruce."""
        custom = self.db.query(CustomBruce).filter_by(id=custom_id).first()
        if custom:
            custom.active = False
            self.db.commit()
            return True
        return False

    def dismiss_by_name(self, name: str, reason: str = "") -> bool:
        """Dismiss a custom Bruce by name."""
        custom = self.db.query(CustomBruce).filter_by(name=name).first()
        if custom:
            return self.dismiss_custom_bruce(custom.id, reason)
        return False

    def extend_custom_bruce(self, custom_id: int, new_expiry_value: str) -> bool:
        """Extend a custom Bruce's expiry."""
        custom = self.db.query(CustomBruce).filter_by(id=custom_id).first()
        if custom:
            custom.expiry_value = new_expiry_value
            self.db.commit()
            return True
        return False

    def list_active_customs(self) -> list:
        """Get all active custom Bruces."""
        return self.db.query(CustomBruce).filter_by(active=True).all()

    def get_custom_bruce(self, custom_id: int) -> CustomBruce | None:
        """Get a custom Bruce by ID."""
        return self.db.query(CustomBruce).filter_by(id=custom_id).first()

    def check_expiries(self):
        """
        Check for custom Bruces that should expire and deactivate them.
        Expiry conditions: 'manual', 'time-based', 'event-based', 'decision-based'.
        """
        now = datetime.now()
        customs = self.list_active_customs()

        for custom in customs:
            should_expire = False

            if custom.expiry_condition == "time-based":
                # expiry_value is expected to be something like "14" (days)
                try:
                    days = int(custom.expiry_value)
                    created = datetime.fromisoformat(custom.created_at)
                    if (now - created).days >= days:
                        should_expire = True
                except (ValueError, TypeError):
                    pass

            if should_expire:
                self.dismiss_custom_bruce(
                    custom.id, f"Auto-expired: {custom.expiry_condition}"
                )
