import os

DEFAULT_DB_PATH = os.path.expanduser("~/.parliament_of_bruce/parliament.db")
DEFAULT_DATA_DIR = os.path.expanduser("~/.parliament_of_bruce/")
DEFAULT_CONSTITUTION_PATH = os.path.join(
    os.path.dirname(__file__), "templates", "default_constitution.json"
)
DEFAULT_LOGS_DIR = os.path.expanduser("~/.parliament_of_bruce/logs/")
DEFAULT_JSON_PATH = os.path.expanduser("~/.parliament_of_bruce/parliament_data.json")

# Emergency keywords that trigger emergency mode
EMERGENCY_KEYWORDS = [
    "suicide",
    "kill",
    "end it",
    "can't go on",
    "can't take it",
    "want to die",
    "self-harm",
]

# Voting weights for permanent seats
VOTE_WEIGHTS = {
    "Short-Term Bruce": 1,
    "Mid-Term Bruce": 2,
    "Long-Term Bruce": 3,
    "Purpose Bruce": 4,
    "Ultimate Bruce": 5,
    "Reigning Bruce": 3,
}

PASSING_THRESHOLD = 10
MAX_SCORE = 18

# Emergency mode adjustments
EMERGENCY_WEIGHTS = {
    "Short-Term Bruce": 0,  # Cannot initiate
    "Mid-Term Bruce": 2,
    "Long-Term Bruce": 6,  # Doubled
    "Purpose Bruce": 4,
    "Ultimate Bruce": 5,  # Absolute veto
    "Reigning Bruce": 3,
}

EMERGENCY_THRESHOLD = 12  # Higher threshold in emergency
