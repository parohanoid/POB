import os

from .config import DEFAULT_DB_PATH, DEFAULT_JSON_PATH
from .migration import migrate_json_to_db


def ensure_data_dir():
    """Ensure data directory exists."""
    data_dir = os.path.dirname(DEFAULT_DB_PATH)
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(
        os.path.dirname(DEFAULT_JSON_PATH).replace(".json", ""), exist_ok=True
    )


def check_and_migrate_json(db_path: str = DEFAULT_DB_PATH):
    """
    If parliament_data.json exists and DB does not, migrate data.
    """
    ensure_data_dir()
    if os.path.exists(DEFAULT_JSON_PATH) and not os.path.exists(db_path):
        migrate_json_to_db(DEFAULT_JSON_PATH, db_path)


def get_db_path(db_path: str | None = None) -> str:
    """Get the database path, expanding user home if needed."""
    if db_path:
        return os.path.expanduser(db_path)
    return DEFAULT_DB_PATH
