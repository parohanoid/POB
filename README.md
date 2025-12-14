# 🏛️ Parliament of Bruce

A powerful command-line psychological journaling and decision-making system that helps you align all temporal aspects of your identity.

## 📖 Philosophy

The Parliament of Bruce recognizes that you are not one person, but a collection of temporal selves with different priorities:

- **Short-Term Bruce** (1 vote): Immediate needs, pleasure, survival
- **Mid-Term Bruce** (2 votes): Weekly/monthly planning, relationships, career
- **Long-Term Bruce** (3 votes): Years-ahead vision, legacy, strategy
- **Purpose Bruce** (4 votes): Life meaning, values, existential direction
- **Ultimate Bruce** (5 votes): Death-aware wisdom, final truth

Plus a **Reigning Bruce** (3 votes): Your current identity version that changes through life transitions.

Total voting power: 18 votes. Decisions pass with ≥10 votes.

## 🚀 Installation

### Quick Install

```bash
# Clone or download the files
cd parliament-of-bruce

# Install dependencies
pip install typer rich pydantic

# Install the package
pip install -e .

# Initialize your parliament
pob init
```

### Alternative: Run Without Installation

```bash
# Install dependencies
pip install typer rich pydantic

# Run directly
python -m parliament_of_bruce.cli init
```

## 📁 File Structure

```
parliament-of-bruce/
├── setup.py
├── README.md
└── parliament_of_bruce/
    ├── __init__.py
    ├── models.py      # Data structures
    ├── storage.py     # Persistence layer
    ├── services.py    # Business logic
    └── cli.py         # Command interface
```

Data is stored in: `~/.parliament_of_bruce/`

## 🎯 Commands

### Initialize Parliament
```bash
pob init
```
Creates the five permanent seats. Run this once.

### Create Your First Bruce
```bash
pob reign new
```
You'll be asked:
- Name for this Bruce (e.g., "Post-Breakup Bruce", "Entrepreneur Bruce")
- Reason for this identity's birth

### Daily Parliament Session
```bash
pob session daily
```
Conducts a full parliament session where each seat speaks:
1. Short-Term voice
2. Mid-Term voice
3. Long-Term voice
4. Purpose voice
5. Ultimate voice
6. Reigning Bruce synthesis
7. Final policy for the day

### Weekly Review
```bash
pob session weekly
```
Same structure but for weekly reflection.

### Vote on Major Decisions
```bash
pob vote "Should I quit my job?"
```
Each seat votes YES or NO. Weighted voting determines outcome:
- Passing threshold: 10/18 votes
- You'll see which perspective won

### View Identity Timeline
```bash
pob timeline
```
See all Bruce identities you've lived through:
- When each began/ended
- Birth reasons
- Exit reports
- Session counts

### Identity Transitions

**Rebirth** (major life event):
```bash
pob rebirth
```
For catastrophic identity shifts (breakup, job loss, crisis). Creates exit report for current Bruce and births a new one.

**Renunciation** (voluntary ending):
```bash
pob renounce
```
Consciously end current Bruce without external crisis.

**New Reign** (soft transition):
```bash
pob reign new
```
Create new Bruce while keeping continuity.

### Export Your Data
```bash
pob export --format markdown  # or json
```
Generates a complete export of:
- All Bruce identities
- All journal entries
- All decisions
- Complete timeline

## 💡 Usage Examples

### Morning Routine
```bash
pob status        # Check yesterday's policy
pob session daily # Conduct today's session
```

### Review Your Week
```bash
pob read --count 7 --full  # Read last 7 entries in detail
pob stats                  # See your activity stats
pob session weekly         # Conduct weekly reflection
```

### Find Patterns
```bash
pob search "anxious"               # When did you feel anxious?
pob search "breakthrough"          # Find your breakthrough moments
pob search "career" --seat purpose # What did Purpose say about career?
```

### Read a Specific Memory
```bash
pob read --date 2025-12-01 --full  # Revisit December 1st
pob read --date latest --full      # Read your latest entry
```

### Major Decision
```bash
pob vote "Accept job offer in new city?"
# Each seat votes based on their timeline
# Result shows whether parliament approves
```

### Life Transition
```bash
# After a breakup
pob rebirth
# Name: "Post-Sarah Bruce"
# Event: "Ended 3-year relationship, moving to new apartment"

# Creates exit report for previous Bruce
# New Bruce begins with clean slate but full memory
```

### Weekly Review
```bash
pob session weekly
# Reflect on the week
# Identify patterns
# Set next week's direction
```

## 🧠 Psychological Benefits

1. **Prevents short-term thinking dominance**: Ultimate Bruce can veto impulses
2. **Maintains purpose alignment**: Purpose Bruce keeps you on track
3. **Honors all timelines**: No self is ignored
4. **Documents growth**: See how you evolve through Bruces
5. **Makes decisions transparent**: Know why you chose what you chose
6. **Catches warning signs**: System alerts you to imbalances

## ⚠️ Behavioral Warnings

The system monitors patterns and warns you:

- **Short-Term dominance**: "Consider long-term consequences"
- **Purpose silence**: "Risk of existential drift"
- **Ultimate silence**: "Death-aware wisdom is missing"
- **Imbalanced voting**: Tracks which seats are being ignored

## 📊 Data Structure

### Journal Entry
Each session stores:
- Date and type
- Response from each seat
- Reigning Bruce synthesis
- Final policy
- Associated decisions

### Decision Record
Each vote stores:
- Topic
- Each seat's vote
- Score breakdown
- Pass/fail result
- Timestamp

### Bruce Identity
Each version stores:
- Name
- Birth date and reason
- End date (if ended)
- Exit report
- Session count

## 🔒 Privacy

- All data stored locally in `~/.parliament_of_bruce/`
- No cloud sync (add your own if desired)
- Plain JSON format for portability
- Export anytime to Markdown or JSON

## 🎨 Customization

### Change Vote Weights
Edit `parliament_of_bruce/services.py`:
```python
VOTE_WEIGHTS = {
    "ShortTerm": 1,
    "MidTerm": 2,
    "LongTerm": 3,
    "Purpose": 5,    # Give Purpose more power
    "Ultimate": 4,   # Adjust as needed
    "Reigning": 3,
}
```

### Add Custom Session Types
```bash
pob session monthly
pob session quarterly
pob session "life-review"
```

### Modify Seat Descriptions
Edit initial state in `storage.py`.

## 🚨 Emergency Commands

### Reset Everything
```bash
rm -rf ~/.parliament_of_bruce
pob init
```

### Backup Your Data
```bash
cp -r ~/.parliament_of_bruce ~/parliament_backup_$(date +%Y%m%d)
```

### View Raw Data
```bash
cat ~/.parliament_of_bruce/parliament_data.json | python -m json.tool
```

## 🤝 Contributing

This is a personal psychological tool, but improvements welcome:
- Better analysis algorithms
- Visualization features
- Integration with other tools
- Mobile companion app

## 📝 License

MIT License - Use however helps you grow.

## 🙏 Credits

Designed for Bruce, by Bruce, to optimize Bruce.

Built with: Python, Typer, Rich, Pydantic

---

## Quick Start Guide

```bash
# 1. Install
pip install typer rich pydantic
pip install -e .

# 2. Initialize
pob init

# 3. Create your first identity
pob reign new

# 4. Start journaling
pob session daily

# 5. Check your status
pob status

# 6. Read your entries
pob read --full

# 7. See your stats
pob stats

# 8. Search your entries
pob search "important topic"

# 9. Make a big decision
pob vote "Your important question?"

# 10. Export when needed
pob export
```

**You are now running Parliament of Bruce. Your temporal selves are aligned.**