# 🤖 Custom AI Agent - Complete Setup Guide

## Step-by-Step Installation & Usage Guide

This guide walks you through every component of the Custom AI Agent Meeting Scheduler system, explaining what each file does and how to set it up properly.

---

## 📁 Complete System Overview

### System Architecture
```
Custom AI Agent System
├── Core Engine Layer
    ├── meeting_scheduler.py      # Main scheduling engine
    ├── custom_ai_agent.py       # Advanced AI reasoning
├── User Interface Layer  
    ├── calendar_ui.py           # Basic interactive UI
    ├── advanced_ai_ui.py        # Advanced AI interface
├── Demonstration & Learning
    ├── Meeting_Scheduler_Agent.ipynb  # Complete feature demo
    ├── AI_Agent_Demo.ipynb           # AI-focused demo
├── Configuration
    ├── requirements.txt         # Python dependencies
    ├── README.md               # Main documentation
    └── SETUP_GUIDE.md         # This setup guide
```

---

## 🔧 Step 1: Environment Setup

### 1.1 Check Python Version
```bash
# Check Python version (3.8+ required)
python --version
```

### 1.2 Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv ai_agent_env

# Activate virtual environment
# Windows:
ai_agent_env\Scripts\activate
# macOS/Linux:
source ai_agent_env/bin/activate
```

### 1.3 Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Or install manually:
pip install pandas sqlalchemy python-dateutil pytz google-generativeai ipywidgets ipython rich tabulate requests pytest jupyter notebook
```

---

## 📖 Step 2: Understanding Each Component

### 2.1 Core Files Explained

#### 🧠 `meeting_scheduler.py` - The Foundation
**What it does:**
- Core scheduling engine with database management
- Basic calendar operations (create, read, update, delete meetings)
- Conflict detection and basic resolution
- Natural language processing integration (with Gemini AI)

**Key Classes:**
```python
DatabaseManager      # Handles SQLite database operations
GeminiIntegration    # Natural language processing
ConflictResolver     # Detects and suggests solutions for conflicts
CalendarAgent        # Main agent that orchestrates everything
```

**How to use:**
```python
from meeting_scheduler import CalendarAgent

agent = CalendarAgent()
result = agent.schedule_meeting(
    title="Team Meeting",
    participants="John, Sarah",
    start_time="2024-01-15 10:00",
    duration=60
)
```

#### 🤖 `custom_ai_agent.py` - The Intelligence
**What it does:**
- Advanced AI reasoning and decision-making
- Memory system for learning user patterns
- Autonomous operation capabilities
- Contextual analysis and insights
- Predictive conflict resolution

**Key Classes:**
```python
ReasonableAgent       # Main AI agent with reasoning
AgentMemory          # Persistent memory system
ContextualInsights   # Intelligent analysis data
AgentMode           # Different personality modes
```

**How to use:**
```python
from custom_ai_agent import ReasonableAgent, AgentMode

ai_agent = ReasonableAgent(
    user_id="your_name",
    mode=AgentMode.AUTONOMOUS
)

result = ai_agent.autonomous_schedule("Schedule urgent client call tomorrow")
```

#### 🎨 `calendar_ui.py` - Basic Interface
**What it does:**
- Simple Jupyter widget-based interface
- Meeting creation and management forms
- Schedule viewing with pandas DataFrames
- Natural language input handling

**How to use:**
```python
from calendar_ui import create_calendar_ui

ui, agent = create_calendar_ui()
```

#### 🚀 `advanced_ai_ui.py` - Premium Interface
**What it does:**
- Advanced AI control panel
- Agent mode selection and configuration
- Context analysis dashboard
- AI reasoning explanations
- Learning acceleration tools

**How to use:**
```python
from advanced_ai_ui import create_advanced_ai_ui

ui, agent = create_advanced_ai_ui(
    user_id="your_name",
    mode=AgentMode.AUTONOMOUS
)
```

---

## 🚀 Step 3: Running the System

### 3.1 Quick Start (Recommended)

#### Option A: Run the Complete Demo
```bash
# Start Jupyter notebook
jupyter notebook

# Open: Meeting_Scheduler_Agent.ipynb
# Follow the cells step by step
```

#### Option B: Run the AI-Focused Demo
```bash
# Start Jupyter notebook
jupyter notebook

# Open: AI_Agent_Demo.ipynb
# Experience advanced AI capabilities
```

### 3.2 Command Line Testing

#### Test Basic Functionality
```python
# Create test_agent.py
from meeting_scheduler import CalendarAgent, create_sample_data

# Initialize agent
agent = CalendarAgent()

# Create sample data
create_sample_data()

# Test scheduling
result = agent.schedule_meeting(
    title="Test Meeting",
    participants="John Doe",
    start_time="2024-01-15 10:00",
    duration=30,
    location="Office"
)

print(f"Success: {result['success']}")
if result['success']:
    print(f"Meeting: {result['meeting'].title}")
```

#### Test Advanced AI Agent
```python
# Create test_ai.py
from custom_ai_agent import ReasonableAgent, AgentMode

# Initialize AI agent
ai_agent = ReasonableAgent(
    user_id="test_user",
    mode=AgentMode.BALANCED
)

# Test autonomous scheduling
result = ai_agent.autonomous_schedule("Schedule a team meeting next Tuesday")

print(f"AI Action: {result.get('agent_action')}")
print(f"Success: {result['success']}")

if result['success']:
    meeting = result['meeting']
    print(f"Meeting: {meeting.title}")
    print(f"Time: {meeting.start_time}")
    print(f"Confidence: {result.get('confidence', 0):.1%}")
```

### 3.3 Interactive Interface Testing

#### Launch Basic Interface
```python
# Run in Jupyter notebook cell
from calendar_ui import create_calendar_ui, demo_ai_features

# Launch interface
ui, agent = create_calendar_ui()

# Show AI features demo
demo_ai_features()
```

#### Launch Advanced Interface
```python
# Run in Jupyter notebook cell
from advanced_ai_ui import create_advanced_ai_ui
from custom_ai_agent import AgentMode

# Launch advanced AI interface
ui, agent = create_advanced_ai_ui(
    user_id="your_name",
    mode=AgentMode.AUTONOMOUS
)
```

---

## ⚙️ Step 4: Configuration Options

### 4.1 AI Agent Modes

#### Understanding Each Mode
```python
from custom_ai_agent import AgentMode

# Conservative: Requires confirmation for all decisions
AgentMode.CONSERVATIVE

# Aggressive: Fast scheduling with minimal interaction
AgentMode.AUTONOMOUS   # Note: Previous line had typo, using AGGRESSIVE

# Balanced: Optimal balance of speed and accuracy
AgentMode.BALANCED

# Learning: Observes patterns and provides recommendations
AgentMode.LEARNING

# Autonomous: Fully independent AI decision-making
AgentMode.AUTONOMOUS
```

#### Mode Selection Guide
```python
# For beginners: Start conservative
agent = ReasonableAgent(user_id="beginner", mode=AgentMode.CONSERVATIVE)

# For regular use: Balanced approach
agent = ReasonableAgent(user_id="regular", mode=AgentMode.BALANCED)

# For advanced users: Autonomous operation
agent = ReasonableAgent(user_id="advanced", mode=AgentMode.AUTONOMOUS)
```

### 4.2 Gemini AI Setup (Optional Enhancement)

#### Get API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy the key

#### Configure Gemini Integration
```python
import os

# Set your Gemini API key
os.environ['GOOGLE_API_KEY'] = 'your_actual_api_key_here'

# When creating agents, they'll automatically use Gemini
agent = CalendarAgent(gemini_api_key=os.getenv('GOOGLE_API_KEY'))
ai_agent = ReasonableAgent(user_id="user", mode=AgentMode.AUTONOMOUS)
```

#### Enhanced Natural Language Processing
With Gemini enabled, you can use more complex requests:
- "Schedule a meeting with John when he's not busy next week"
- "Find the best time for our team standup considering everyone's schedule"
- "Intelligently reschedule Friday's meeting to avoid conflicts"

---

## 📊 Step 5: Understanding the Database

### 5.1 Database Schema
The system automatically creates `meeting_scheduler.db` with this structure:

```sql
-- Meetings table structure
CREATE TABLE meetings (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    participants TEXT,
    location TEXT,
    is_recurring BOOLEAN DEFAULT FALSE,
    recurring_pattern TEXT,
    recurrence_end_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 5.2 Custom AI Agent Memory Files
When using the AI agent, it creates memory files:
- `agent_memory_your_user_id.pkl` - Persistent memory data
- `agent_insights_your_user_id.json` - Analytics and patterns

### 5.3 Data Management
```python
# Export meetings
import pandas as pd
from meeting_scheduler import DatabaseManager

db = DatabaseManager("meeting_scheduler.db")
meetings = db.get_meetings()

data = []
for meeting in meetings:
    data.append({
        'title': meeting.title,
        'start_time': meeting.start_time,
        'participants': meeting.participants,
        'location': meeting.location
    })

df = pd.DataFrame(data)
df.to_csv('meetings_export.csv', index=False)
```

---

## 🧠 Step 6: Advanced AI Features

### 6.1 Context Analysis
```python
# Analyze current scheduling context
context = ai_agent.analyze_context()

print("Calendar Analysis:")
print(f"Stress Level: {context['calendar_stress_level']:.1%}")
print(f"Conflict Risk: {context['conflict_probability']:.1%}")
print(f"Optimal Timing: {context['optimal_timing']}")
```

### 6.2 Intelligent Recommendations
```python
# Get AI recommendations
insights = ai_agent.intelligent_recommendations()

print("AI Recommendations:")
for suggestion in insights['personalized_suggestions']:
    print(f"• {suggestion}")

print(f"\nCalendar Optimization:")
opt = insights['calendar_optimization']
print(f"Stress Level: {opt['stress_level']:.1%}")
print(f"Avg Duration: {opt['avg_meeting_duration']:.0f} minutes")
print(f"Conflict Risk: {opt['conflict_probability']:.1%}")
```

### 6.3 Proactive Conflict Resolution
```python
# Check for potential conflicts
alerts = ai_agent.proactive_conflict_resolution()

if alerts:
    print("⚠️ Potential Issues Detected:")
    for alert in alerts:
        print(f"• {alert['type']}: {alert['message']}")
        print(f"  Meeting: {alert['meeting'].title}")
else:
    print("✅ No conflicts detected")
```

### 6.4 Learning Acceleration
```python
# Provide feedback to help AI learn
learning_data = {
    'feedback': 'I prefer morning meetings for important discussions',
    'rating': 5
}

ai_agent.memory.scheduling_history.append({
    'timestamp': datetime.now(),
    'user_feedback_score': learning_data['rating'] / 5,  # Convert to 0-1 scale
    'context_snapshot': {'learning_feedback': learning_data['feedback']}
})

ai_agent.save_state()  # Persist learning
```

---

## 🔧 Step 7: Troubleshooting

### 7.1 Common Issues

#### Import Errors
```bash
# If you get import errors, check your Python environment
python -c "import pandas, sqlalchemy, ipywidgets"
```

#### Database Issues
```python
# If database issues occur, start fresh
import os
if os.path.exists("meeting_scheduler.db"):
    os.remove("meeting_scheduler.db")

# Reinitialize
from meeting_scheduler import CalendarAgent
agent = CalendarAgent()
```

#### Widget Issues in Jupyter
```python
# If widgets don't display properly
from IPython.display import display
import ipywidgets as widgets
widgets.Widget.close_all()  # Close any frozen widgets
```

### 7.2 Performance Optimization

#### For Large Datasets
```python
# If you have many meetings, optimize queries
from meeting_scheduler import DatabaseManager

db = DatabaseManager()

# Get meetings for specific date range only
import datetime
next_week = datetime.date.today() + datetime.timedelta(days=7)
meetings = db.get_meetings(datetime.date.today(), next_week)
```

#### Memory Management
```python
# Clear AI agent memory if needed
import os
user_id = "your_user_id"
for file in [f"agent_memory_{user_id}.pkl", f"agent_insights_{user_id}.json"]:
    if os.path.exists(file):
        os.remove(file)
```

---

## 📈 Step 8: Usage Patterns

### 8.1 Beginner Pattern
```python
# Start simple
from meeting_scheduler import CalendarAgent

agent = CalendarAgent()

# Schedule basic meetings
result = agent.schedule_meeting(
    title="Team Standup",
    participants="Team Members",
    start_time="2024-01-15 09:00",
    duration=30
)

# View schedule
df = agent.view_schedule()
print(df)
```

### 8.2 Intermediate Pattern
```python
# Use AI features
from custom_ai_agent import ReasonableAgent, AgentMode

ai_agent = ReasonableAgent(user_id="intermediate", mode=AgentMode.BALANCED)

# Natural language scheduling
result = ai_agent.autonomous_schedule("Schedule meeting with John tomorrow")
print(f"AI Decision: {result['agent_action']}")

# Get insights
insights = ai_agent.intelligent_recommendations()
```

### 8.3 Advanced Pattern
```python
# Full AI autonomy
from custom_ai_agent import ReasonableAgent, AgentMode
from advanced_ai_ui import create_advanced_ai_ui

# Create autonomous AI agent
ai_agent = ReasonableAgent(user_id="advanced", mode=AgentMode.AUTONOMOUS)

# Launch advanced interface
ui, agent = create_advanced_ai_ui(
    user_id="advanced",
    mode=AgentMode.AUTONOMOUS
)

# Use all AI features
context = ai_agent.analyze_context()
alerts = ai_agent.proactive_conflict_resolution()
insights = ai_agent.intelligent_recommendations()
```

---

## 🎯 Step 9: Practical Examples

### 9.1 Daily Meeting Management
```python
# Morning routine: Check today's schedule
from datetime import datetime
from meeting_scheduler import CalendarAgent

agent = CalendarAgent()
today = datetime.now().date()

# Get today's meetings
meetings = agent.db_manager.get_meetings(today, today)
print(f"You have {len(meetings)} meetings today")

for meeting in meetings:
    time_remaining = meeting.start_time - datetime.now()
    if time_remaining.total_seconds() > 0:
        print(f"⏰ {meeting.title} in {int(time_remaining.total_seconds()/3600)} hours")
```

### 9.2 Weekly Planning
```python
# AI-powered weekly planning
from custom_ai_agent import ReasonableAgent, AgentMode
from datetime import datetime, timedelta

ai_agent = ReasonableAgent(user_id="planner", mode=AgentMode.AUTONOMOUS)

# Get weekly recommendations
insights = ai_agent.intelligent_recommendations()

# Schedule optimal meetings for next week
requests = [
    "Schedule team standup for every morning next week",
    "Book planning session on Wednesday optimizing for productivity",
    "Find best time for client review meeting"
]

for request in requests:
    result = ai_agent.autonomous_schedule(request)
    if result['success']:
        print(f"✅ Scheduled: {result['meeting'].title}")
    else:
        print(f"❌ Couldn't schedule: {request}")

# Check for conflicts
alerts = ai_agent.proactive_conflict_resolution()
if alerts:
    print("⚠️ Conflicts detected for next week")
```

### 9.3 Smart Conflict Resolution
```python
# Intelligent conflict handling
from custom_agent import ReasonableAgent, AgentMode

ai_agent = ReasonableAgent(user_id="scheduler", mode=AgentMode.AUTONOMOUS)

# Simulate scheduling conflict
try:
    result = ai_agent.autonomous_schedule("Schedule urgent client call tomorrow at 2 PM")
    
    if not result['success'] and 'conflicts' in result:
        print("🔍 Conflicts detected:")
        for conf_meeting, desc in result['conflicts']:
            print(f"• {desc}")
        
        print("\n💡 AI Suggestions:")
        for i, suggestion in enumerate(result['suggestions'][:3], 1):
            print(f"{i}. {suggestion.strftime('%Y-%m-%d %H:%M')}")
            
        # Automatically pick best alternative
        if result['suggestions']:
            # Let AI make the decision
            new_result = ai_agent.autonomous_schedule(
                f"Reschedule to {result['suggestions'][0].strftime('%Y-%m-%d %H:%M')}"
            )
            print(f"✅ Rescheduled: {new_result['meeting'].title}")
    
except Exception as e:
    print(f"Error: {e}")
```

---

## 📊 Step 10: Monitoring & Analytics

### 10.1 AI Performance Tracking
```python
# Monitor AI agent performance
from custom_ai_agent import ReasonableAgent

ai_agent = ReasonableAgent(user_id="analyst", mode=AgentMode.AUTONOMOUS)

# Get comprehensive report
report = ai_agent.get_agent_report()

print("📊 AI Agent Performance Report")
print("=" * 40)
print(f"Success Rate: {report['insights']['success_rate']:.1%}")
print(f"Total Interactions: {report['memory_stats']['total_interactions']}")
print(f"Calendar Stress: {report['insights']['calendar_stress']:.1%}")
print(f"Agent Mode: {report['agent_info']['mode']}")

# Learning progress
memory_data = ai_agent.memory.learning_data
if memory_data:
    print(f"Learning Patterns: {len(memory_data)} categories")
    for category, count in memory_data.items():
        print(f"  {category}: {count} interactions")
```

### 10.2 Custom Analytics
```python
# Create custom analytics
import pandas as pd
from datetime import datetime, timedelta
from meeting_scheduler import CalendarAgent

agent = CalendarAgent()

# Analyze meeting patterns
meetings = agent.db_manager.get_meetings()

if meetings:
    # Create analysis dataframe
    analysis_data = []
    for meeting in meetings:
        analysis_data.append({
            'day_of_week': meeting.start_time.strftime('%A'),
            'hour': meeting.start_time.hour,
            'duration_minutes': (meeting.end_time - meeting.start_time).total_seconds() / 60,
            'has_location': bool(meeting.location),
            'is_recurring': meeting.is_recurring,
            'participants_count': len(meeting.participants.split(',')) if meeting.participants else 0
        })
    
    df = pd.DataFrame(analysis_data)
    
    print("📈 Meeting Analytics")
    print("=" * 25)
    print(f"Most common day: {df['day_of_week'].mode()[0]}")
    print(f"Preferred hour: {df['hour'].mode()[0]}:00")
    print(f"Average duration: {df['duration_minutes'].mean():.1f} minutes")
    print(f"Recurring meetings: {df['is_recurring'].sum()}/{len(df)}")
    
    # Detailed breakdown
    print("\n📅 Day Distribution:")
    day_counts = df['day_of_week'].value_counts()
    for day, count in day_counts.items():
        print(f"  {day}: {count} meetings")
    
    print("\n⏰ Time Distribution:")
    hour_counts = df['hour'].value_counts().sort_index()
    for hour, count in hour_counts.items():
        print(f"  {hour:02d}:00: {count} meetings")
```

---

## 🎯 Quick Reference Commands

### Essential Commands
```python
# Import statements
from meeting_scheduler import CalendarAgent
from custom_ai_agent import ReasonableAgent, AgentMode
from calendar_ui import create_calendar_ui
from advanced_ai_ui import create_advanced_ai_ui

# Basic setup
agent = CalendarAgent()
ai_agent = ReasonableAgent(user_id="user", mode=AgentMode.BALANCED)

# Schedule meetings
result = agent.schedule_meeting(title="Meeting", participants="Team", start_time="2024-01-15 10:00", duration=60)
result = ai_agent.autonomous_schedule("Schedule team meeting tomorrow")

# View schedule
df = agent.view_schedule()

# AI analysis
context = ai_agent.analyze_context()
insights = ai_agent.intelligent_recommendations()
alerts = ai_agent.proactive_conflict_resolution()

# Interfaces
ui_basic = create_calendar_ui()
ui_advanced = create_advanced_ai_ui(user_id="user", mode=AgentMode.AUTONOMOUS)
```

### Configuration Options
```python
# Agent modes
AgentMode.CONSERVATIVE   # Cautious decisions
AgentMode.BALANCED       # Balanced approach  
AgentMode.AUTONOMOUS     # Independent decisions
AgentMode.LEARNING       # Observation mode
AgentMode.AUTONOMOUS       # Aggressive scheduling

# Database paths
"meeting_scheduler.db"           # Main database
"agent_memory_user.pkl"          # AI memory
"agent_insights_user.json"       # AI insights

# API keys (optional)
os.environ['GOOGLE_API_KEY'] = 'your_gemini_key'
```

---

## 🚀 You're Ready!

Your Custom AI Agent Meeting Scheduler is now fully set up and ready to use! 

**Start with:**
1. **Meeting_Scheduler_Agent.ipynb** for full feature exploration
2. **AI_Agent_Demo.ipynb** for advanced AI capabilities
3. Experiment with different agent modes
4. Configure Gemini AI for enhanced natural language processing

**Remember:**
- Start in BALANCED mode for beginners
- Move to AUTONOMOUS mode as you gain confidence
- Provide feedback to help the AI learn
- Monitor performance through analytics

🤖 **Your intelligent calendar assistant is ready to serve!**
