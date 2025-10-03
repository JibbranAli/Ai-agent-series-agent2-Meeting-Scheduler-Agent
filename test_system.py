#!/usr/bin/env python3
"""
Test Script for Custom AI Agent Meeting Scheduler
"""

import sys
import os
from datetime import datetime, timedelta

def check_dependencies():
    """Check if all required packages are installed"""
    print("Checking dependencies...")
    
    required_packages = [
        'pandas', 'sqlalchemy', 'dateutil', 'pytz', 
        'ipywidgets', 'IPython', 'rich', 'tabulate'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'dateutil':
                import dateutil
            else:
                __import__(package)
            print(f"   OK {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   MISSING {package}")
    
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        return False
    return True

def test_basic_functionality():
    """Test basic calendar agent functionality"""
    print("\nTesting basic functionality...")
    
    try:
        from meeting_scheduler import CalendarAgent, create_sample_data
        
        # Initialize agent
        agent = CalendarAgent()
        print("   OK Calendar agent initialized")
        
        # Create sample data
        create_sample_data()
        print("   OK Sample data created")
        
        # Test scheduling
        result = agent.schedule_meeting(
            title="Test Meeting",
            participants="Test User",
            start_time=datetime.now() + timedelta(hours=1),
            duration=30,
            location="Test Location"
        )
        
        if result['success']:
            print(f"   OK Test meeting scheduled: {result['meeting'].title}")
        else:
            print(f"   WARNING Test meeting failed: {result.get('error', 'Unknown error')}")
        
        # Test viewing schedule
        df = agent.view_schedule()
        print(f"   OK Schedule viewing works: {len(df)} meetings")
        
        return True, agent
        
    except Exception as e:
        print(f"   ERROR Basic functionality test failed: {e}")
        return False, None

def test_ai_agent():
    """Test advanced AI agent functionality"""
    print("\nTesting AI agent functionality...")
    
    try:
        from custom_ai_agent import ReasonableAgent, AgentMode
        
        # Initialize AI agent
        ai_agent = ReasonableAgent(
            user_id="test_user",
            mode=AgentMode.BALANCED
        )
        print("   OK AI agent initialized")
        
        # Test context analysis
        context = ai_agent.analyze_context()
        print(f"   OK Context analysis: {len(context)} factors analyzed")
        
        # Test autonomous scheduling
        result = ai_agent.autonomous_schedule("Schedule a test meeting next Tuesday")
        print(f"   OK AI scheduling: {result.get('agent_action', 'NO_ACTION')}")
        
        # Test recommendations
        insights = ai_agent.intelligent_recommendations()
        print(f"   OK AI recommendations: {len(insights)} categories available")
        
        return True, ai_agent
        
    except Exception as e:
        print(f"   ERROR AI agent test failed: {e}")
        return False, None

def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'meeting_scheduler.py',
        'custom_ai_agent.py', 
        'calendar_ui.py',
        'advanced_ai_ui.py',
        'requirements.txt',
        'Meeting_Scheduler_Agent.ipynb',
        'AI_Agent_Demo.ipynb',
        'README.md',
        'SETUP_GUIDE.md'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   OK {file}")
        else:
            missing_files.append(file)
            print(f"   MISSING {file}")
    
    if missing_files:
        print(f"Missing files: {', '.join(missing_files)}")
        return False
    return True

def main():
    """Main test function"""
    print("AI Agent Meeting Scheduler - System Test")
    print("=" * 50)
    
    # Step 1: Check file structure
    files_ok = test_file_structure()
    
    # Step 2: Check dependencies
    deps_ok = check_dependencies()
    
    # Step 3: Test basic functionality
    basic_works = False
    basic_agent = None
    if files_ok and deps_ok:
        basic_works, basic_agent = test_basic_functionality()
    
    # Step 4: Test AI agent
    ai_works = False
    ai_agent = None
    if basic_works:
        ai_works, ai_agent = test_ai_agent()
    
    # Summary
    print("\nTest Results Summary")
    print("=" * 30)
    print(f"Files: {'OK' if files_ok else 'FAILED'}")
    print(f"Dependencies: {'OK' if deps_ok else 'FAILED'}")
    print(f"Basic Agent: {'OK' if basic_works else 'FAILED'}")
    print(f"AI Agent: {'OK' if ai_works else 'FAILED'}")
    
    if files_ok and deps_ok and basic_works:
        print("\nSUCCESS: System is working!")
        
        if basic_agent:
            meetings = basic_agent.db_manager.get_meetings()
            print(f"Database: {len(meetings)} meetings")
            
        if ai_works:
            print("AI Features: Available")
            print("Next: Try the Jupyter notebooks!")
        else:
            print("AI Features: Basic mode only")
            
        # Show usage example
        print("\nQuick Usage Example:")
        print("from meeting_scheduler import CalendarAgent")
        print("agent = CalendarAgent()")
        print("result = agent.schedule_meeting(title='Meeting', participants='Team', start_time='2024-01-15 10:00', duration=60)")
        
    else:
        print("\nFAILED: System has issues")
        print("Check the errors above and fix them")
        
    return files_ok and deps_ok and basic_works

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\nReady to use!")
        else:
            print("\nFix issues and try again")
    except Exception as e:
        print(f"\nTest error: {e}")
        print("Refer to setup documentation for help")
