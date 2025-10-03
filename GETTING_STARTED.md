# 🚀 Getting Started - Custom AI Agent Meeting Scheduler

## Quick Setup Guide (5 minutes to running!)

This guide gets you up and running with the AI agent system in just a few steps.

---

## ⚡ Step 1: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

**What this installs:**
- `pandas` - Data manipulation
- `sqlalchemy` - Database operations  
- `python-dateutil` - Date/time parsing
- `pytz` - Timezone handling
- `google-generativeai` - AI natural language (optional)
- `ipywidgets` - Interactive interface
- `rich` - Beautiful console output

---

## 🧪 Step 2: Quick Test

```bash
# Test that everything works
python quick_start.py
```

**What this does:**
- Checks all dependencies
- Tests basic calendar functionality
- Tests AI agent capabilities
- Shows usage examples
- Launches an interactive demo

---

## 📚 Step 3: Explore the Demo Notebooks

### Option A: Complete Feature Demo
```bash
jupyter notebook
# Open: Meeting_Scheduler_Agent.ipynb
```

**What you'll see:**
- Complete system overview
- Basic scheduling operations
- Conflict detection demo
- Natural language processing
- Advanced database operations

### Option B: AI-Focused Demo  
```
jupyter notebook
# Open: AI_Agent_Demo.ipynb
```

**What you'll experience:**
- Advanced AI reasoning
- Autonomous decision making
- Context analysis
- Learning capabilities
- Performance analytics

---

## 🤖 Step 4: Basic Usage

### Simple Calendar Scheduling
```python
from meeting_scheduler import CalendarAgent

# Create agent
agent = CalendarAgent()

# Schedule a meeting
result = agent.schedule_meeting(
    title="Team Standup",
    participants="John, Sarah, Mike",
    start_time="2024-01-15 10:00",
    duration=30,
    location="Conference Room A"
)

print(f"Success: {result['success']}")
if result['success']:
    print(f"Meeting: {result['meeting'].title}")
```

### Advanced AI Scheduling
```python
from custom_ai_agent import ReasonableAgent, AgentMode

# Create AI agent
ai_agent = ReasonableAgent(
    user_id="your_name",
    mode=AgentMode.BALANCED
)

# AI-powered scheduling
result = ai_agent.autonomous_schedule(
    "Schedule an urgent client call for tomorrow morning"
)

print(f"AI Decision: {result.get('agent_action')}")
print(f"Confidence: {result.get('confidence', 0):.1%}")
```

---

## 🎨 Step 5: Launch Interactive Interface

### Basic Interface
```python
from calendar_ui import create_calendar_ui

# Launch basic interface (run in Jupyter)
ui, agent = create_calendar_ui()
```

### Advanced AI Interface
```python
from advanced_ai_ui import create_advanced_ai_ui
from custom_ai_agent import AgentMode

# Launch advanced interface (run in Jupyter)
ui, agent = create_advanced_ai_ui(
    user_id="your_name",
    mode=AgentMode.AUTONOMOUS
)
```

---

## 🎯 Common Use Cases

### 1. Quick Meeting Scheduling
```python
from meeting_scheduler import CalendarAgent

# Check today's schedule
agent = CalendarAgent()
df = agent.view_schedule()
print(df.head())

# Schedule new meeting
result = agent.schedule_meeting(
    title="Quick Sync",
    participants="John",
    start_time="2024-01-15 14:00",
    duration=30
)
```

### 2. Intelligent Scheduling
```python
from custom_ai_agent import ReasonableAgent, AgentMode

# Get AI recommendations
ai_agent = ReasonableAgent(user_id="you", mode=AgentMode.BALANCED)
insights = ai_agent.intelligent_recommendations()

print("AI Suggestions:")
for suggestion in insights['personalized_suggestions']:
    print(f"• {suggestion}")
```

### 3. Conflict Detection
```python
# Smart conflict detection
from custom_ai_agent import ReasonableAgent
ai_agent = ReasonableAgent(user_id="you")

# Let AI analyze conflicts
result = ai_agent.autonomous_schedule(
    "Schedule team meeting tomorrow at 2 PM"
)

if not result['success']:
    print("Conflicts detected!")
    for conflict in result.get('conflicts', []):
        print(f"Conflict: {conflict[1]}")  # Description
    
    if 'suggestions' in result:
        print("Suggested alternatives:")
        for suggestion in result['suggestions'][:3]:
            print(f"• {suggestion}")
```

---

## 🔧 Configuration Options

### Agent Modes
```python
from custom_ai_agent import AgentMode

# Choose your mode:
AgentMode.CONSERVATIVE  # Cautious, asks for confirmation
AgentMode.BALANCED      # Recommended for most users
AgentMode.AUTONOMOUS    # AI makes independent decisions
AgentMode.LEARNING      # Observes your patterns
AgentMode.AUTONOMOUS      # Fast scheduling, minimal confirmation
```

### Enable AI Enhancement (Optional)
```python
import os

# Set your Gemini API key for enhanced NLP
os.environ['GOOGLE_API_KEY'] = 'your_gemini_api_key_here'

# More advanced natural language processing:
ai_agent = ReasonableAgent(user_id="you", mode=AgentMode.AUTONOMOUS)

# Now you can use complex requests:
ai_agent.autonomous_schedule(
    "Book a 30-minute brainstorming session with Sarah sometime next week when she's not busy with client calls"
)
```

---

## 💡 Pro Tips

### 1. Start Simple, Then Advance
```python
# Beginner: Basic agent
agent = CalendarAgent()

# Intermediate: AI agent with guidance
ai_agent = ReasonableAgent(user_id="you", mode=AgentMode.BALANCED)

# Advanced: Full autonomy
ai_agent = ReasonableAgent(user_id="you", mode=AgentMode.AUTONOMOUS)
```

### 2. Help AI Learn
```python
# Provide feedback to improve AI
result = ai_agent.autonomous_schedule("Schedule call with client")

# Give feedback (improves performance)
ai_agent.memory.scheduling_history.append({
    'timestamp': datetime.now(),
    'user_feedback_score': 0.9,  # High satisfaction
    'context_snapshot': {'preferred_time': 'morning'}
})

ai_agent.save_state()  # Save learning
```

### 3. Monitor Performance
```python
# Get AI performance report
report = ai_agent.get_agent_report()
print(f"Success Rate: {report['insights']['success_rate']:.1%}")
print(f"Interactions: {report['memory_stats']['total_interactions']}")
```

## 🎉 You're Ready!

Your Custom AI Agent is now set up and ready to intelligently manage your calendar!

**Next Steps:**
1. ✅ Explore the Jupyter notebooks for detailed features
2. ✅ Try different agent modes to find what works best
3. ✅ Experiment with natural language scheduling
4. ✅ Provide feedback to help the AI learn your preferences

🤖 **Enjoy your intelligent calendar assistant!**
