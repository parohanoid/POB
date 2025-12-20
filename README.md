# 🏛️ Parliament of Bruce

A powerful command-line psychological journaling and decision-making system that helps you align all temporal aspects of your identity.

## 📖 Philosophy

The Parliament of Bruce recognizes that you are not one person, but a collection of temporal selves with different priorities, operating at different time horizons and with different values:

- **🟥 Short-Term Bruce — The Rebel / The Animal** (1 vote): **Now, today, tonight**
  - Body over mind. Nerves over plans. Wants relief, not reasons.
  - Pain feels urgent. Boredom is death. Discipline feels like a cage.
  - Speaks in cravings, anger, fear. Tells raw truth others hide.

- **🟨 Mid-Term Bruce — The Operator** (2 votes): **This week, this month**
  - Execution over emotion. Cares about momentum and small wins.
  - Systems beat willpower. Burnout is the real enemy.
  - Translates emotion into tasks. Asks: what's doable, not ideal?

- **🟦 Long-Term Bruce — The Architect** (3 votes): **Years ahead**
  - Structure over impulse. Thinks in systems and leverage.
  - Compounding is sacred. Designs environments, not days.
  - Sees emotions as data, not commands. Waste of potential is the real sin.

- **🟪 Purpose Bruce — The Dharma Bearer** (4 votes): **Lifetime**
  - Meaning over success. Guards the story of your life.
  - Power without meaning is hollow. Asks why before how.
  - Speaks softly but halts everything when values are betrayed.

- **⚫ Ultimate Bruce — The Judge** (5 votes): **Deathbed**
  - Legacy over everything. Immune to excuses.
  - Doesn't care how it felt, only what it became.
  - Sees your entire life as one object. Asks the final question.

Plus a **Reigning Bruce** (3 votes): Your current identity version that changes through life transitions, synthesizing all voices.

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
Conducts a full **rotating parliament session** where voices speak in rounds. Each voice appears with their full archetype description and activation cue—allowing you to **put on their mask** and speak from their frame:

1. **🟥 Short-Term Bruce** — The Rebel / The Animal
   - *Activation: What hurts right now, and what would make it stop?*
2. **🟨 Mid-Term Bruce** — The Operator
   - *Activation: What's the minimum action that moves this forward?*
3. **🟦 Long-Term Bruce** — The Architect
   - *Activation: Does this scale, compound, or rot?*
4. **🟪 Purpose Bruce** — The Dharma Bearer
   - *Activation: Is this worthy of the story we're living?*
5. **⚫ Ultimate Bruce** — The Judge
   - *Activation: When this is over… will we respect this choice?*
6. Any active Temporary Bruces (in order)
7. (After each round, choose to continue the discussion or proceed)
8. **Reigning Bruce** — Synthesis and final policy

The session supports **multi-round discussion** - after all voices speak once, you can choose to continue for additional rounds where any voice can offer new perspectives, or move directly to synthesis.

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

## 🗣️ Temporary Voices (New Feature!)

Beyond the five permanent seats and the Reigning Bruce, you can now add **temporary Bruce voices** to your parliament. These are context-specific perspectives that don't have voting rights but can participate in discussions.

### Add a Temporary Voice
```bash
pob add-voice "Anxiety Bruce" -d "The voice of worry and concern"
pob add-voice "Shadow Self" -d "What lies beneath my awareness"
pob add-voice "Critical Parent" -d "The internalized critic"
```

Each temporary voice:
- Has no voting rights (discussion only)
- Gets a unique ID for tracking
- Can speak during parliament sessions
- Persists across sessions until dismissed

### View Active Voices
```bash
pob voices
```
Lists all temporary Bruces currently in parliament with their:
- Name and description
- Unique ID
- Last statement

### Remove a Temporary Voice
```bash
pob remove-voice <voice_id>
```
Dismiss a temporary voice from the parliament. Example:
```bash
pob remove-voice a1b2c3d4
```

### Using Temporary Voices in Sessions

When you run `pob session daily`, temporary voices are included in the rotating discussion:
- They speak in order after the five permanent seats
- You can run multiple rounds where any voice (including temps) can offer additional thoughts
- Their responses are recorded in the journal entry but don't count toward voting decisions
- Perfect for exploring marginalized perspectives or temporary concerns

## Export Your Data
```bash
pob export --format markdown  # or json
```
Generates a complete export of:
- All Bruce identities
- All journal entries
- All decisions
- Complete timeline

## 💡 Usage Examples

### Morning Routine with Temporary Voices
```bash
# First time setup - add temporary perspectives you want to hear from
pob add-voice "Anxiety" -d "What are my worries?"
pob add-voice "Body" -d "What does my body need?"

# Conduct your session with rotating discussion
pob status        # Check yesterday's policy
pob session daily # Conduct today's session with all voices
#   → Rotate through: Short-Term, Mid-Term, Long-Term, Purpose, Ultimate, Anxiety, Body
#   → Choose to continue for Round 2 or proceed to Reigning synthesis
#   → Get final policy for the day
```

### Multi-Round Parliament Discussion
```bash
pob session daily
# Round 1: Each voice speaks once
#   Short-Term: "Coffee!"
#   Mid-Term: "Meetings scheduled"
#   Long-Term: "Project progression good"
#   Purpose: "Aligned with goals"
#   Ultimate: "Living authentically"
#   Anxiety: "Too many deadlines"
#   Body: "Need stretching"

# System asks: Continue discussion for another round? (y/n)
# If yes, goes to Round 2:
#   Short-Term: "Actually need a walk first"
#   [etc...]

# Then moves to final synthesis and policy
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

### Read a Specific Memory (with Temporary Voices)
```bash
pob read --date 2025-12-17 --full
# Now shows all permanent Bruce voices, Reigning synthesis, AND any temporary voices that spoke that day
```

### Major Decision
```bash
pob vote "Accept job offer in new city?"
# Each permanent seat votes based on their timeline
# Temporary voices don't vote but you can review their concerns
# Result shows whether parliament approves
```

### Manage Temporary Voices
```bash
pob voices                    # See all active temporary voices
pob remove-voice a1b2c3d4     # Remove voice when no longer needed

# Add new ones as needed for different life phases
pob add-voice "Grief" -d "Process loss from the relationship"
pob add-voice "Healer" -d "Recovery and resilience"
```

### Life Transition with Voices
```bash
# After a breakup - add context-specific voices
pob add-voice "Grief" -d "Mourning what was lost"
pob add-voice "Future Self" -d "Who will I become?"

pob rebirth
# Name: "Post-Sarah Bruce"
# Event: "Ended 3-year relationship, moving to new apartment"

# Creates exit report for previous Bruce
# New Bruce begins with clean slate but full memory
# Can keep or remove temporary voices as needed
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
- Response from each permanent seat
- Response from Reigning Bruce
- Final policy
- **Responses from any temporary Voices that spoke**
- Associated decisions

### Temporary Voice
Each temporary Bruce stores:
- Unique ID
- Name and description
- Creation date
- Last statement
- Active status

### Decision Record
Each vote stores:
- Topic
- Each permanent seat's vote (temporary voices don't vote)
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

## 🔄 Backward Compatibility

The new temporary voice feature is **fully backward compatible** with existing data:

- Old `parliament_data.json` files without the `temporary_bruces` field load automatically
- Existing journal entries without `temporary_bruce_entries` are preserved as-is
- No migration needed - the system adds missing fields on first load
- You can immediately start using temporary voices with your existing parliament

Simply run the new commands when you're ready to add temporary perspectives to your existing sessions.

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