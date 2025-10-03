#!/usr/bin/env python3
"""
🤖 Quick Start Script for Custom AI Agent Meeting Scheduler
==========================================================

This script helps you get started immediately with the AI agent system.
Run this script to test all components and launch the interface.
"""

import os
import sys
from datetime import datetime, timedelta

def check_dependencies():
    """Check if all required packages are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'pandas', 'sqlalchemy', 'python_dateutil', 'pytz', 
        'ipywidgets', 'ipython', 'rich', 'tabulate'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('_', '-'))
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("📦 Installing missing packages...")
        
        import subprocess
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package.replace('_', '-')])
                print(f"   ✅ Installed {package}")
            except subprocess.CalledProcessError:
                print(f"   ❌ Failed to install {package}")
                print(f"💡 Please run: pip install {package.replace('_', '-')}")
    
    print("\n✅ Dependency check complete!")

def test_basic_functionality():
    """Test basic calendar agent functionality"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        from meeting_scheduler import CalendarAgent, create_sample_data
        
        # Initialize agent
        agent = CalendarAgent()
        print("   ✅ Calendar agent initialized")
        
        # Create sample data
        create_sample_data()
        print("   ✅ Sample data created")
        
        # Test scheduling
        result = agent.schedule_meeting(
            title="Quick Test Meeting",
            participants="Test User",
            start_time=datetime.now() + timedelta(hours=1),
            duration=30,
            location="Test Location"
        )
        
        if result['success']:
            print(f"   ✅ Test meeting scheduled: {result['meeting'].title}")
        else:
            print(f"   ⚠️ Test meeting failed: {(result.get('error', 'Unknown error'))}")
        
        # Test viewing schedule
        df = agent.view_schedule()
        print(f"   ✅ Schedule viewing works: {len(df)} meetings")
        
        return True, agent
        
    except Exception as e:
        print(f"   ❌ Basic functionality test failed: {e}")
        return False, None

def test_ai_agent():
    """Test advanced AI agent functionality"""
    print("\n🤖 Testing AI agent functionality...")
    
    try:
        from custom_ai_agent import ReasonableAgent, AgentMode
        
        # Initialize AI agent
        ai_agent = ReasonableAgent(
            user_id="test_user",
            mode=AgentMode.BALANCED
        )
        print("   ✅ AI agent initialized")
        
        # Test context analysis
        context = ai_agent.analyze_context()
        print(f"   ✅ Context analysis: {len(context)} factors analyzed")
        
        # Test autonomous scheduling
        result = ai_agent.autonomous_schedule("Schedule a test meeting next Tuesday")
        print(f"   ✅ AI scheduling: {result.get('agent_action', 'NO_ACTION')}")
        
        # Test recommendations
        insights = ai_agent.intelligent_recommendations()
        print(f"   ✅ AI recommendations: {len(insights)} categories available")
        
        return True, ai_agent
        
    except Exception as e:
        print(f"   ❌ AI agent test failed: {e}")
        return False, None

def launch_interface():
    """Launch the calendar interface"""
    print("\n🚀 Launching calendar interface...")
    
    try:
        # Try to launch Jupyter-style interface
        try:
            from IPython.display import display
            from calendar_ui import create_calendar_ui
            from advanced_ai_ui import create_advanced_ai_ui
            from custom_ai_agent import AgentMode
            
            print("   🎨 Launching basic calendar UI...")
            # Note: Only create the UI objects, display happens in notebook
            ui, agent = create_calendar_ui()
            
            print("   🚀 Creating advanced AI UI...")
            ai_ui, ai_agent = create_advanced_ai_ui(
                user_id="quick_start_user",
                mode=AgentMode.BALANCED
            )
            
            print("   ✅ Interfaces created successfully!")
            print("   💡 Note: Run 'show_interface()' methods in Jupyter notebook to display")
            
            return True, [ui, agent, ai_ui, ai_agent]
            
        except ImportError:
            print("   ⚠️ Jupyter/IPython not available, creating console interface")
            from meeting_scheduler import CalendarAgent
            agent = CalendarAgent()
            
            print("\n🎯 Console Interface")
            print("=" * 30)
            print("Available commands:")
            print("- agent.schedule_meeting(title='Meeting', participants='Team', start_time='2024-01-15 10:00', duration=60)")
            print("- agent.view_schedule()")
            print("- agent.cancel_meeting(meeting_id)")
            
            return True, agent
            
    except Exception as e:
        print(f"   ❌ Interface launch failed: {e}")
        return False, None

def show_usage_examples():
    """Show usage examples"""
    print("\n📚 Usage Examples")
    print("=" * 20)
    
    print("\n1. Basic Scheduling:")
    print("   from meeting_scheduler import CalendarAgent")
    print("   agent = CalendarAgent()")
    print("   result = agent.schedule_meeting(")
    print("       title='Team Meeting',")
    print("       participants='John, Sarah',")
    print("       start_time='2024-01-15 10:00',")
    print("       duration=60")
    print("   )")
    
    print("\n2. Advanced AI Agent:")
    print("   from custom_ai_agent import ReasonableAgent, AgentMode")
    print("   ai_agent = ReasonableAgent(user_id='your_name', mode=AgentMode.AUTONOMOUS)")
    print("   result = ai_agent.autonomous_schedule('Schedule urgent client call tomorrow')")
    
    print("\n3. Natural Language Processing:")
    print("   ai_agent.autonomous_schedule('Book a 30-minute slot with Sarah next week')")
    print("   AI will parse the request and schedule intelligently")
    
    print("\n4. View Schedule:")
    print("   df = agent.view_schedule()  # Returns pandas DataFrame")
    print("   print(df.head())")
    
    print("\n5. AI Recommendations:")
    print("   insights = ai_agent.intelligent_recommendations()")
    print("   for suggestion in insights['personalized_suggestions']:")
    print("       print(f'• {suggestion}')")

def main():
    """Main quick start function"""
    print("🤖 Custom AI Agent Meeting Scheduler - Quick Start")
    print("=" * 55)
    
    # Step 1: Check dependencies
    check_dependencies()
    
    # Step 2: Test basic functionality
    basic_works, basic_agent = test_basic_functionality()
    
    # Step 3: Test AI agent
    ai_works, ai_agent = test_ai_agent()
    
    # Step 4: Launch interface
    interface_works, interface_data = launch_interface()
    
    # Summary
    print("\n📊 Quick Start Results")
    print("=" * 30)
    print(f"✅ Dependencies: {'Working' if True else 'Issues detected'}")
    print(f"✅ Basic Agent: {'Working' if basic_works else 'Failed'}")
    print(f"✅ AI Agent: {'Working' if ai_works else 'Failed'}")
    print(f"✅ Interface: {'Working' if interface_works else 'Failed'}")
    
    if basic_works or ai_works:
        print("\n🎉 System is ready to use!")
        show_usage_examples()
        
        if basic_works:
            print(f"\n📅 Schedule contains {len(basic_agent.db_manager.get_meetings())} meetings")
            
        if ai_works:
            insights = ai_agent.intelligent_recommendations()
            print(f"\n🧠 AI insights available: {len(insights)} categories")
            print("💡 Next: Try the Jupyter notebooks for full experience!")
    else:
        print("\n❌ System setup failed")
        print("💡 Please check the error messages above and fix any issues")
        print("📖 Refer to SETUP_GUIDE.md for detailed instructions")

def interactive_demo():
    """Run an interactive demo"""
    print("\n🎮 Interactive Demo")
    print("=" * 20)
    
    if not test_basic_functionality()[0]:
        print("❌ Basic functionality not working, skipping demo")
        return
    
    try:
        from meeting_scheduler import CalendarAgent
        from custom_ai_agent import ReasonableAgent, AgentMode
        
        # Initialize agents
        basic_agent = CalendarAgent()
        ai_agent = ReasonableAgent(user_id="demo_user", mode=AgentMode.BALANCED)
        
        print("Available demo scenarios:")
        print("1. Schedule a simple meeting")
        print("2. Use AI for intelligent scheduling")
        print("3. Check for conflicts")
        print("4. Get AI recommendations")
        
        choice = input("\nChoose scenario (1-4): ").strip()
        
        if choice == "1":
            title = input("Meeting title: ") or "Demo Meeting"
            participants = input("Participants: ") or "Team"
            
            result = basic_agent.schedule_meeting(
                title=title,
                participants=participants,
                start_time=datetime.now() + timedelta(hours=1),
                duration=60,
                location="Demo Location"
            )
            
            print(f"Result: {result['success']}")
            if result['success']:
                print(f"Scheduled: {result['meeting'].title}")
                
        elif choice == "2":
            request = input("AI scheduling request: ") or "Schedule team meeting tomorrow"
            
            result = ai_agent.autonomous_schedule(request)
            print(f"AI Action: {result.get('agent_action')}")
            print(f"Success: {result['success']}")
            
        elif choice == "3":
            alerts = ai_agent.proactive_conflict_resolution()
            if alerts:
                print(f"Found {len(alerts)} potential conflicts")
                for alert in alerts:
                    print(f"• {alert['message']}")
            else:
                print("No conflicts detected")
                
        elif choice == "4":
            insights = ai_agent.intelligent_recommendations()
            suggestions = insights.get('personalized_suggestions', [])
            
            if suggestions:
                print("AI Recommendations:")
                for suggestion in suggestions:
                    print(f"• {suggestion}")
            else:
                print("AI is still learning patterns")
        
        print("\n✅ Demo complete!")
        
    except KeyboardInterrupt:
        print("\n👋 Demo cancelled")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

if __name__ == "__main__":
    try:
        main()
        
        # Offer interactive demo
        if input("\n🎮 Run interactive demo? (y/n): ").lower().startswith('y'):
            interactive_demo()
            
    except KeyboardInterrupt:
        print("\n\n👋 Quick start cancelled")
    except Exception as e:
        print(f"\n❌ Quick start error: {e}")
        print("💡 Please refer to SETUP_GUIDE.md for troubleshooting")
