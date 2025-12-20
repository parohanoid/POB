# Parliament of Bruce - Setup & Configuration Guide

## ✅ Environment Setup Complete

All dependencies have been successfully installed and configured.

### Python Environment

- **Python Version**: 3.14.0
- **Location**: `/home/parohanoid/Documents/projects/POB/venv`
- **Virtual Environment**: ✅ Activated

### Installed Dependencies

All dependencies from `requirements.txt` have been installed:

```
✓ typer >= 0.9.0              (CLI Framework)
✓ rich >= 13.0.0              (Styled Console Output)
✓ sqlalchemy >= 2.0.0          (Database ORM)
✓ pydantic >= 1.10.0, < 2.0.0  (Data Validation - Termux compatible)
✓ pytest >= 7.0.0              (Testing)
✓ black >= 23.0.0              (Code Formatter)
✓ ruff >= 0.1.0                (Linter)
✓ isort >= 5.12.0              (Import Sorter)
✓ click == 8.3.1               (CLI Utilities)
```

### Test Results

**All 9 tests pass successfully:**

```
✓ test_create_custom_bruce         PASSED
✓ test_max_two_custom_bruces       PASSED
✓ test_dismiss_custom_bruce        PASSED
✓ test_create_session              PASSED
✓ test_emergency_keyword_detection PASSED
✓ test_weekly_summary              PASSED
✓ test_vote_passes                 PASSED
✓ test_vote_fails                  PASSED
✓ test_create_decision             PASSED
```

## Quick Start

### 1. Activate Virtual Environment

```bash
cd /home/parohanoid/Documents/projects/POB
source venv/bin/activate
```

### 2. Initialize the System

```bash
python -m parliament_of_bruce.cli init
```

This will:
- Create `~/.parliament_of_bruce/` directory
- Initialize SQLite database
- Create 6 permanent parliament seats
- Load default constitution

### 3. Create Your First Reigning Bruce

```bash
python -m parliament_of_bruce.cli reign-new \
  --name "Initial" \
  --reason "First identity version"
```

### 4. Conduct a Session

```bash
python -m parliament_of_bruce.cli session-cmd daily
```

Interactive prompts will guide you through:
- Short-Term Bruce perspective
- Mid-Term Bruce perspective
- Long-Term Bruce perspective
- Purpose Bruce perspective
- Ultimate Bruce perspective
- Reigning Bruce synthesis
- Final governing policy

### 5. Check Status

```bash
python -m parliament_of_bruce.cli status
```

Shows current reigning identity and recent sessions.

### 6. Run All Tests

```bash
pytest parliament_of_bruce/tests/ -v
```

## Available Commands

```
init              Initialize the Parliament of Bruce system
status            Show current parliament status
timeline          Display timeline of all Bruce identities
reign-new         Create a new Reigning Bruce
session-cmd       Conduct a parliament session (daily/weekly)
vote              Conduct a vote on a decision
rebirth           Trigger a rebirth (major identity shift)
renounce          Voluntarily renounce the current Reigning Bruce
emergency         Trigger emergency mode
custom-create     Create a custom Bruce
custom-list       List active custom Bruces
custom-dismiss    Dismiss a custom Bruce
analytics         Show analytics and dominance scores
```

## Directory Structure

### Data Storage

```
~/.parliament_of_bruce/
├── parliament.db                    # SQLite database
├── parliament_data.json.imported    # Old JSON (if migrated)
└── emergency_logs/
    └── emergency_YYYY-MM-DD.jsonl   # Emergency logs
```

### Project Structure

```
/home/parohanoid/Documents/projects/POB/
├── venv/                            # Virtual environment
├── parliament_of_bruce/
│   ├── cli.py                       # Main CLI module
│   ├── config.py                    # Configuration
│   ├── models.py                    # Data models
│   ├── db.py                        # Database layer
│   ├── storage.py                   # Storage utilities
│   ├── migration.py                 # JSON migration
│   ├── services/                    # Business logic
│   ├── ui/                          # User interface
│   ├── templates/                   # Constitutional template
│   └── tests/                       # Test suite
├── pyproject.toml                   # Project config
├── requirements.txt                 # Dependencies
└── README.md                        # Documentation
```

## Database Schema

### Tables Created

1. **Seat** - Parliament seats (votes, descriptions)
2. **ReigningBruce** - Identity versions (start/end dates)
3. **Session** - Journal sessions (daily/weekly)
4. **Decision** - Voting outcomes
5. **Law** - Bill management
6. **Constitution** - Core values & rules
7. **CustomBruce** - Custom psychological identities
8. **EmergencyLog** - Emergency records

## Voting System

### Permanent Seats & Weights

| Seat | Votes | Focus |
|------|-------|-------|
| Short-Term Bruce | 1 | Immediate needs |
| Mid-Term Bruce | 2 | Weeks/months |
| Long-Term Bruce | 3 | Years ahead |
| Purpose Bruce | 4 | Life meaning |
| Ultimate Bruce | 5 | Death-aware wisdom |
| Reigning Bruce | 3 | Executive |
| **Total** | **18** | --- |

### Passing Threshold
- **Standard**: 10/18 votes (55%)
- **Emergency**: 12/18 votes (67%)

### Emergency Mode

Triggered by keywords in sessions or manual activation:

- Short-Term weight unchanged (1)
- Mid-Term weight unchanged (2)
- Long-Term weight doubled (3 → 6)
- Purpose Bruce weight unchanged (4)
- Ultimate Bruce maintains veto power (5)
- Reigning Bruce weight unchanged (3)

## Configuration

### Vote Weights (`config.py`)

```python
VOTE_WEIGHTS = {
    "Short-Term Bruce": 1,
    "Mid-Term Bruce": 2,
    "Long-Term Bruce": 3,
    "Purpose Bruce": 4,
    "Ultimate Bruce": 5,
    "Reigning Bruce": 3,
}

PASSING_THRESHOLD = 10  # out of 18 total
EMERGENCY_THRESHOLD = 12

EMERGENCY_KEYWORDS = [
    "crisis",
    "emergency",
    "urgent",
    "panic",
    "danger",
    # ... more keywords
]
```

### Emergency Settings (`config.py`)

```python
EMERGENCY_WEIGHTS = {
    "Short-Term Bruce": 0,      # Can't initiate
    "Mid-Term Bruce": 2,
    "Long-Term Bruce": 6,       # Doubled
    "Purpose Bruce": 4,
    "Ultimate Bruce": 5,        # Veto power
    "Reigning Bruce": 3,
}
```

## Backward Compatibility

### Auto-Migration from JSON

If you have an old `parliament_data.json`:

1. Place it in `~/.parliament_of_bruce/parliament_data.json`
2. Run `pob init`
3. System automatically migrates all data to SQLite
4. Original JSON renamed to `.imported`

All session history, reigning Bruce records, and decisions are preserved.

## Troubleshooting

### Virtual Environment Issues

```bash
# Reactivate venv
source venv/bin/activate

# Verify Python
which python
python --version

# Check pip
pip list
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Verify imports
python -c "import typer; import sqlalchemy; print('✓ OK')"
```

### Database Errors

```bash
# Check database location
ls ~/.parliament_of_bruce/

# Reinitialize (WARNING: deletes existing DB)
rm ~/.parliament_of_bruce/parliament.db
pob init
```

### Test Failures

```bash
# Run tests with verbose output
pytest parliament_of_bruce/tests/ -v -s

# Run specific test
pytest parliament_of_bruce/tests/test_session.py -v
```

## Development Workflow

### Code Quality

```bash
# Lint with ruff
ruff check parliament_of_bruce/

# Format with black
black parliament_of_bruce/

# Sort imports with isort
isort parliament_of_bruce/

# Run all checks
black --check parliament_of_bruce/
ruff check parliament_of_bruce/
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=parliament_of_bruce

# Run specific test file
pytest parliament_of_bruce/tests/test_session.py

# Run single test
pytest parliament_of_bruce/tests/test_session.py::test_create_session
```

## Dependency Management

### Adding New Packages

```bash
# Activate venv
source venv/bin/activate

# Install package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt
```

### Updating Packages

```bash
# Update specific package
pip install --upgrade package-name

# Update all packages
pip install --upgrade -r requirements.txt

# Check for outdated packages
pip list --outdated
```

## Production Deployment

### Creating Standalone Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile parliament_of_bruce/cli.py
```

### Docker Containerization

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python", "-m", "parliament_of_bruce.cli"]
```

Build and run:

```bash
docker build -t parliament-of-bruce .
docker run -it -v ~/.parliament_of_bruce:/root/.parliament_of_bruce parliament-of-bruce init
```

## Next Steps

1. ✅ Initialize system: `pob init`
2. ✅ Create Reigning Bruce: `pob reign-new --name "X" --reason "Y"`
3. ✅ Run daily session: `pob session-cmd daily`
4. ✅ Check status: `pob status`
5. ✅ View analytics: `pob analytics`

## Support

For issues or feature requests, check:
- `README.md` - User documentation
- `IMPLEMENTATION_COMPLETE.md` - Implementation details
- Test files - Usage examples
- Source code docstrings - Technical details

## License

MIT License - See LICENSE file
