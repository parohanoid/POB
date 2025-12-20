# Parliament of Bruce - Quick Reference

## 🚀 Startup

```bash
cd /home/parohanoid/Documents/projects/POB
source venv/bin/activate
```

## 🎯 Common Commands

### System Management
```bash
# Initialize system (first time)
pob init

# Check system status
pob status

# View decision timeline
pob timeline
```

### Parliament Operations
```bash
# Create new Reigning Bruce
pob reign-new --name "Name" --reason "Reason"

# Run a session
pob session-cmd daily       # Daily
pob session-cmd weekly      # Weekly
pob session-cmd quarterly   # Quarterly
pob session-cmd annual      # Annual

# Vote on a decision
pob vote --decision-id ID --seat SEAT --value yes|no

# View/manage laws
pob law-list
pob law-propose "Law title"
pob law-pass ID
```

### Emergency Mode
```bash
# Trigger emergency (uses emergency keywords)
pob emergency --keyword "trigger"
```

### Custom Bruces
```bash
# Create custom identity
pob custom-create --name "Custom" --power-level LEVEL

# List custom Bruces
pob custom-list

# Dismiss custom Bruce
pob custom-dismiss --name "Custom"
```

### Analytics
```bash
# View analytics
pob analytics --type dominance
pob analytics --type speaking-frequency
```

## 🧪 Testing & Development

```bash
# Run all tests
pytest parliament_of_bruce/tests/ -v

# Run specific test
pytest parliament_of_bruce/tests/test_vote.py -v

# Run with coverage
pytest parliament_of_bruce/tests/ --cov=parliament_of_bruce

# Format code
black parliament_of_bruce/

# Lint code
ruff check parliament_of_bruce/

# Sort imports
isort parliament_of_bruce/
```

## 📊 Voting System

- **Total Votes:** 18
- **Threshold:** 10+ votes needed
- **Vote Weights:**
  - ST (Short Term) = 1 vote
  - MT (Medium Term) = 2 votes
  - LT (Long Term) = 3 votes
  - PB (Primary Bruce) = 4 votes
  - UB (Upper Bruce) = 5 votes
  - RB (Reigning Bruce) = 3 votes

## 🗂️ Database Locations

```
Database:     ~/.parliament_of_bruce/parliament.db (48KB)
Project:      /home/parohanoid/Documents/projects/POB
Virtual Env:  /home/parohanoid/Documents/projects/POB/venv
```

## 📚 Documentation

- **FINAL_SETUP_SUMMARY.md** - Complete setup guide
- **SETUP_GUIDE.md** - Detailed configuration
- **IMPLEMENTATION_COMPLETE.md** - Architecture details
- **README.md** - User guide

## ⚡ Shortcuts

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
alias pob_on='cd /home/parohanoid/Documents/projects/POB && source venv/bin/activate'
alias pob_test='cd /home/parohanoid/Documents/projects/POB && source venv/bin/activate && pytest parliament_of_bruce/tests/ -v'
alias pob_format='cd /home/parohanoid/Documents/projects/POB && source venv/bin/activate && black parliament_of_bruce/'
```

## 🔍 Verification

```bash
# Quick verify everything works
bash verify_setup.sh

# Check imports
python -c "from parliament_of_bruce import cli; print('✅ CLI loads')"

# Check database
python -c "from parliament_of_bruce.db import Base; print('✅ Database ORM works')"

# Check services
python -c "from parliament_of_bruce.services import vote_service; print('✅ Services load')"
```

## 🛑 Troubleshooting

### Commands not found
```bash
# Reinstall package
pip install -e .
```

### Tests failing
```bash
# Check Python path
python -m pytest parliament_of_bruce/tests/ -v
```

### Database issues
```bash
# Reset database (WARNING: loses all data)
rm -rf ~/.parliament_of_bruce
python -m parliament_of_bruce.cli init
```

### Import errors
```bash
# Verify all dependencies
pip install -r requirements.txt
pip install -e .
```

## 📞 Help

```bash
# Show help for any command
pob --help              # Overall help
pob vote --help         # Specific command help
```

## ✅ System Status

- Python: 3.14.0 ✅
- Virtual Env: Active ✅
- Dependencies: 22/22 installed ✅
- Database: 48KB, initialized ✅
- Tests: 9/9 passing ✅
- CLI: 13 commands ready ✅

---

**Ready to use! Start with:** `source venv/bin/activate && python -m parliament_of_bruce.cli status`
