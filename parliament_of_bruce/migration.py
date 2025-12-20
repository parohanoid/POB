import json
import os

from .db import (
    Base,
    Decision,
    ReigningBruce,
    Session,
    get_engine,
    get_session,
    Seat,
)


def migrate_json_to_db(json_path: str, db_path: str):
    """
    Migrate old parliament_data.json to SQLite DB.
    Preserves all historical data and reigning bruce info.
    """
    if not os.path.exists(json_path):
        return

    with open(json_path, "r") as f:
        data = json.load(f)

    engine = get_engine(db_path)
    Base.metadata.create_all(engine)
    session = get_session(db_path)

    try:
        # Seats (permanent)
        for seat_name, seat in data.get("seats", {}).items():
            existing = session.query(Seat).filter_by(name=seat["name"]).first()
            if not existing:
                session.add(
                    Seat(
                        name=seat["name"],
                        votes=seat["votes"],
                        description=seat["description"],
                        active=seat.get("active", True),
                        is_permanent=True,
                    )
                )

        # Reigning Bruce (current)
        rb = data.get("reigning_bruce")
        if rb:
            session.add(
                ReigningBruce(
                    name=rb["name"],
                    start_date=rb["start_date"],
                    end_date=rb.get("end_date"),
                    reason_born=rb["reason_born"],
                    exit_report=rb.get("exit_report"),
                )
            )

        # Bruce history (past identities)
        for bruce in data.get("bruce_history", []):
            session.add(
                ReigningBruce(
                    name=bruce["name"],
                    start_date=bruce["start_date"],
                    end_date=bruce.get("end_date"),
                    reason_born=bruce["reason_born"],
                    exit_report=bruce.get("exit_report"),
                )
            )

        # Sessions (journal entries)
        for entry in data.get("journal_entries", []):
            session.add(
                Session(
                    date=entry["date"],
                    session_type=entry["session_type"],
                    statements={
                        "short_term": entry.get("short_term", ""),
                        "mid_term": entry.get("mid_term", ""),
                        "long_term": entry.get("long_term", ""),
                        "purpose": entry.get("purpose", ""),
                        "ultimate": entry.get("ultimate", ""),
                        "reigning": entry.get("reigning", ""),
                    },
                    final_policy=entry.get("final_policy", ""),
                    decisions_voted_on=[],
                )
            )

        # Decisions
        for dec in data.get("decisions", []):
            session.add(
                Decision(
                    topic=dec["topic"],
                    options=dec["options"],
                    votes=dec["votes"],
                    weighted_result=dec.get("total_score", 0),
                    passed=dec["passed"],
                    passed_on=dec["timestamp"],
                )
            )

        session.commit()
    finally:
        session.close()

    # Optionally rename the old JSON file to indicate it was imported
    if os.path.exists(json_path):
        backup_path = json_path + ".imported"
        os.rename(json_path, backup_path)
