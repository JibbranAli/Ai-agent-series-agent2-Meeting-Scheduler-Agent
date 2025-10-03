# 🚀 CLI Quick Reference Guide

## Essential Commands

### Getting Started
```bash
python cli.py --help          # Show all commands
python cli.py --config       # Show current settings
python test_system.py        # Test installation
```

### Viewing Schedule
```bash
python cli.py view           # View incoming 7 days
python cli.py view --days 14 # View 14 days
python cli.py stats          # Show statistics
```

### AI Scheduling
```bash
python cli.py ai-schedule "meeting tomorrow"              # Get recommendations
python cli.py ai-schedule-auto "team standup next week"  # Auto-book
```

### Basic Scheduling
```bash
python cli.py schedule "Client Call" --participants "John, Sarah" --start-time "2025-01-15 14:00" --duration 60
```

### Analysis & Management
```bash
python cli.py analyze        # AI analysis
python cli.py cancel 1       # Cancel meeting #1
python cli.py demo           # Demo with sample data
```

## Agent Mode Settings

### Quick Mode Changes
```bash
# In config.env file, change:
DEFAULT_AGENT_MODE=AUTONOMOUS     # Full autonomy
DEFAULT_AGENT_MODE=BALANCED       # Default (recommended)
DEFAULT_AGENT_MODE=CONSERVATIVE   # Maximum safety
DEFAULT_AGENT_MODE=LEARNING       # Adaptive learning
```

### Mode Comparison
| Mode | Behavior | Best For |
|------|----------|----------|
| CONSERVATIVE | Always asks confirmation | Beginners |
| BALANCED | Recommends, asks approval | Most users |
| AUTONOMOUS | Auto-books high confidence | Experts |
| LEARNING | Learns & adapts patterns | Long-term use |

## Natural Language Examples
```bash
# Time expressions
"tomorrow at 2pm"
"next Tuesday morning" 
"Friday afternoon after 3pm"
"this week before Thursday"

# Context scheduling
"urgent client call avoiding lunch"
"project review with team"
"find time for catch-up"
"schedule around conflicts"
```

## Troubleshooting Quick Fixes
```bash
# Reset AI learning
del .ai_agent_insights.json

# Reset schedule database
del meeting_scheduler.db && python cli.py demo

# Check system status
python test_system.py

# Verbose logging
# In config.env: LOG_LEVEL=DEBUG
```
