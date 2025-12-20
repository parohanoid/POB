"""Law service for managing parliament laws and amendments."""

from datetime import datetime

from ..db import Law


class LawService:
    """Handle law lifecycle: propose, amend, repeal, and expiry."""

    def __init__(self, db_session):
        self.db = db_session

    def propose_law(
        self,
        name: str,
        law_type: str = "standing",
        proposer: str = "Parliament",
        expiry_date: str | None = None,
    ) -> int:
        """
        Create a law proposal (status: Pending).
        Returns law ID.
        """
        law = Law(
            name=name,
            type=law_type,
            proposer=proposer,
            created_on=datetime.now().isoformat(),
            status="Pending",
            votes_history=[],
            expiry_date=expiry_date,
        )
        self.db.add(law)
        self.db.commit()
        return law.id

    def pass_law(self, law_id: int, vote_record: dict) -> bool:
        """
        Pass a law (status: Active).
        """
        law = self.db.query(Law).filter_by(id=law_id).first()
        if not law:
            return False

        law.status = "Active"
        law.votes_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "action": "passed",
                "votes": vote_record,
            }
        )
        self.db.commit()
        return True

    def repeal_law(self, law_id: int, reason: str = "") -> bool:
        """
        Repeal a law (status: Repealed).
        """
        law = self.db.query(Law).filter_by(id=law_id).first()
        if not law:
            return False

        law.status = "Repealed"
        law.votes_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "action": "repealed",
                "reason": reason,
            }
        )
        self.db.commit()
        return True

    def amend_law(self, law_id: int, amendment_text: str, vote_record: dict) -> bool:
        """
        Amend a law (log the amendment and update votes).
        """
        law = self.db.query(Law).filter_by(id=law_id).first()
        if not law:
            return False

        law.votes_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "action": "amended",
                "amendment": amendment_text,
                "votes": vote_record,
            }
        )
        self.db.commit()
        return True

    def expire_law(self, law_id: int):
        """Expire a law (status: Expired)."""
        law = self.db.query(Law).filter_by(id=law_id).first()
        if law:
            law.status = "Expired"
            law.votes_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "action": "expired",
                }
            )
            self.db.commit()

    def list_laws(self, status: str | None = None) -> list:
        """List laws, optionally filtered by status."""
        query = self.db.query(Law)
        if status:
            query = query.filter_by(status=status)
        return query.all()

    def get_law(self, law_id: int) -> Law | None:
        """Get a law by ID."""
        return self.db.query(Law).filter_by(id=law_id).first()

    def check_expiries(self):
        """
        Check for laws that have reached their expiry date and expire them.
        """
        now = datetime.now().isoformat()
        laws = self.db.query(Law).filter(
            Law.status == "Active", Law.expiry_date is not None
        )
        for law in laws:
            if law.expiry_date and law.expiry_date < now:
                self.expire_law(law.id)
