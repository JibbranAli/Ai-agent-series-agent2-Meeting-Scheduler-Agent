#!/usr/bin/env python3
"""
Command Line Interface for Custom AI Agent Meeting Scheduler
"""

import sys
import os
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from meeting_scheduler import CalendarAgent, create_sample_data
from custom_ai_agent import ReasonableAgent, AgentMode
from config import config

class MeetingSchedulerCLI:
    """Command Line Interface for the AI Meeting Scheduler"""
    
    def __init__(self):
        self.basic_agent = None
        self.ai_agent = None
        self.current_user = config.get_user_id()
        
    def initialize_agents(self):
        """Initialize the calendar and AI agents"""
        # Initialize basic agent
        self.basic_agent = CalendarAgent()
        
        # Initialize AI agent
        api_key = config.get_api_key()
        agent_mode = AgentMode[self.get_agent_mode()]
        
        # Set Gemini API key in environment if available
        if api_key:
            os.environ['GOOGLE_API_KEY'] = api_key
        
        # Always set the hardcoded API key environment
        os.environ['GOOGLE_API_KEY'] = "AIzaSyA5w6gUBNgab_q04cQ6mh3KQjcwSvylwtc"
        
        self.ai_agent = ReasonableAgent(
            user_id=self.current_user,
            mode=agent_mode
        )
        
        print(f"AI Agent initialized in {agent_mode.value.upper()} mode")
        if api_key:
            print("Enhanced AI features enabled with Gemini")
        else:
            print("Basic AI features (Gemini API key not configured)")
    
    def get_agent_mode(self) -> str:
        """Get agent mode from config"""
        mode = config.get_agent_mode().upper()
        valid_modes = ['CONSERVATIVE', 'BALANCED', 'AUTONOMOUS', 'LEARNING']
        if mode in valid_modes:
            return mode
        return 'BALANCED'
    
    def schedule_meeting(self, title: str, participants: str = "", 
                        start_time: str = "", duration: int = 60, 
                        location: str = "", use_ai: bool = False) -> bool:
        """Schedule a meeting"""
        if use_ai and self.ai_agent:
            # AI-powered scheduling
            request = f"Schedule {title}"
            if participants:
                request += f" with {participants}"
            if start_time:
                request += f" at {start_time}"
            if duration != 60:
                request += f" for {duration} minutes"
            if location:
                request += f" at {location}"
                
            result = self.ai_agent.autonomous_schedule(request)
            
            if result['success']:
                meeting = result['meeting']
                print(f"AI scheduled: {meeting.title}")
                print(f"Time: {meeting.start_time.strftime('%Y-%m-%d %H:%M')}")
                print(f"Participants: {meeting.participants or 'TBD'}")
                print(f"Confidence: {result.get('confidence', 0):.1%}")
                return True
            else:
                print(f"AI scheduling failed: {result.get('error', 'Unknown error')}")
                if 'recommendations' in result:
                    print("AI Recommendations:")
                    for i, rec in enumerate(result['recommendations'][:3], 1):
                        reasoning = rec.get('reasoning', 'Good alternative')
                        print(f"  {i}. {rec['time'].strftime('%Y-%m-%d %H:%M')}")
                        print(f"     {reasoning}")
                return False
        else:
            # Basic scheduling
            try:
                if start_time:
                    start_dt = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
                else:
                    start_dt = datetime.now() + timedelta(hours=1)
                
                result = self.basic_agent.schedule_meeting(
                    title=title,
                    participants=participants,
                    start_time=start_dt,
                    duration=duration,
                    location=location
                )
                
                if result['success']:
                    meeting = result['meeting']
                    print(f"Meeting scheduled: {meeting.title}")
                    print(f"Time: {meeting.start_time.strftime('%Y-%m-%d %H:%M')}")
                    print(f"Duration: {duration} minutes")
                    return True
                else:
                    print(f"Scheduling failed: {result.get('error', 'Unknown error')}")
                    if 'conflicts' in result:
                        print("Conflicts detected:")
                        for _, desc in result['conflicts']:
                            print(f"  - {desc}")
                    return False
                    
            except ValueError:
                print("Invalid start_time format. Use: YYYY-MM-DD HH:MM")
                return False
    
    def view_schedule(self, days_ahead: int = 7) -> None:
        """View upcoming schedule"""
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=days_ahead)
        
        df = self.basic_agent.view_schedule(start_date, end_date)
        
        if df.empty:
            print(f"No meetings scheduled for the next {days_ahead} days")
            return
        
        print(f"\nUpcoming Schedule (next {days_ahead} days):")
        print("=" * 60)
        
        for _, row in df.iterrows():
            start_time = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M')
            end_time = datetime.strptime(row['End Time'], '%Y-%m-%d %H:%M')
            
            duration = int((end_time - start_time).total_seconds() / 60)
            
            print(f"\nMeeting #{row['ID']}: {row['Title']}")
            print(f"  Time: {start_time.strftime('%A, %B %d, %Y at %H:%M')}")
            print(f"  Duration: {duration} minutes")
            if row['Participants']:
                print(f"  Participants: {row['Participants']}")
            if row['Location']:
                print(f"  Location: {row['Location']}")
    
    def ai_analyze(self) -> None:
        """Run AI analysis"""
        if not self.ai_agent:
            print("AI agent not initialized")
            return
            
        print("\nAI Context Analysis:")
        print("=" * 30)
        
        # Analyze context
        context = self.ai_agent.analyze_context()
        
        print(f"Calendar stress level: {context['calendar_stress_level']:.1%}")
        print(f"Conflict probability: {context['conflict_probability']:.1%}")
        print(f"Current hour: {context['hour_of_day']:02d}:00")
        
        stress_level = context['calendar_stress_level']
        if stress_level > 0.7:
            print("Status: High calendar stress - consider reducing meetings")
        elif stress_level > 0.4:
            print("Status: Moderate calendar density")
        else:
            print("Status: Low calendar stress - good scheduling balance")
        
        # Get recommendations
        print(f"\nAI Recommendations:")
        insights = self.ai_agent.intelligent_recommendations()
        
        suggestions = insights.get('personalized_suggestions', [])
        if suggestions:
            for i, suggestion in enumerate(suggestions[:5], 1):
                print(f"  {i}. {suggestion}")
        else:
            print("  AI is still learning your patterns")
            
        # Check for conflicts
        print(f"\nConflict Analysis:")
        alerts = self.ai_agent.proactive_conflict_resolution()
        
        if alerts:
            print(f"  Detected {len(alerts)} potential issues:")
            for alert in alerts:
                urgency = alert['urgency']
                icon = "RED" if urgency == 'HIGH' else "YELLOW" if urgency == 'MEDIUM' else "BLUE"
                print(f"    [{icon}] {alert['message']}")
        else:
            print("  No conflicts detected")
    
    def ai_schedule(self, request: str) -> bool:
        """Use AI to schedule based on natural language request"""
        if not self.ai_agent:
            print("AI agent not available")
            return False
            
        print(f"Processing AI request: '{request}'")
        
        result = self.ai_agent.autonomous_schedule(request)
        
        print(f"\nAI Decision: {result.get('agent_action', 'UNDEFINED')}")
        print(f"Success: {result['success']}")
        
        if result['success']:
            meeting = result['meeting']
            confidence = result.get('confidence', 0)
            
            print(f"\nSUCCESS: Meeting Scheduled:")
            print(f"  Title: {meeting.title}")
            print(f"  Time: {meeting.start_time.strftime('%Y-%m-%d %H:%M')}")
            print(f"  Duration: {(meeting.end_time - meeting.start_time).seconds // 60} minutes")
            print(f"  Participants: {meeting.participants or 'TBD'}")
            print(f"  Location: {meeting.location or 'TBD'}")
            print(f"  AI Confidence: {confidence:.1%}")
            
            if 'reasoning' in result:
                print(f"  AI Reasoning: {result['reasoning']}")
            
            return True
        else:
            print(f"FAILED: Scheduling failed: {result.get('error', 'Unknown error')}")
            
            if 'recommendations' in result:
                print(f"\nAI Alternatives:")
                for i, rec in enumerate(result['recommendations'][:3], 1):
                    print(f"  {i}. {rec['time'].strftime('%Y-%m-%d %H:%M')}")
                    print(f"     Confidence: {rec['score']:.2f}")
                    print(f"     Reasoning: {rec.get('reasoning', 'Good alternative')}")
            
            return False
    
    def cancel_meeting(self, meeting_id: int) -> bool:
        """Cancel a meeting by ID"""
        if self.basic_agent.cancel_meeting(meeting_id):
            print(f"Meeting #{meeting_id} cancelled successfully")
            return True
        else:
            print(f"Failed to cancel meeting #{meeting_id}")
            return False
    
    def show_stats(self) -> None:
        """Show scheduling statistics"""
        meetings = self.basic_agent.db_manager.get_meetings()
        
        print("\nMeeting Statistics:")
        print("=" * 25)
        print(f"Total meetings: {len(meetings)}")
        
        if meetings:
            # Calculate some basic stats
            total_duration = sum((m.end_time - m.start_time).seconds for m in meetings)
            avg_duration = total_duration / len(meetings) / 60  # Convert to minutes
            
            recurring_count = len([m for m in meetings if m.is_recurring])
            today_count = len([m for m in meetings if m.start_time.date() == datetime.now().date()])
            
            print(f"Average duration: {avg_duration:.1f} minutes")
            print(f"Recurring meetings: {recurring_count}")
            print(f"Today's meetings: {today_count}")
            
            # Most common participations
            participants = {}
            for meeting in meetings:
                if meeting.participants:
                    for participant in meeting.participants.split(','):
                        name = participant.strip()
                        participants[name] = participants.get(name, 0) + 1
            
            if participants:
                most_common = max(participants.items(), key=lambda x: x[1])
                print(f"Most frequent participant: {most_common[0]} ({most_common[1]} meetings)")
        
        # AI agent stats
        if self.ai_agent:
            report = self.ai_agent.get_agent_report()
            print(f"\nAI Agent Stats:")
            print(f"  Success rate: {report['insights']['success_rate']:.1%}")
            print(f"  Interactions: {report['memory_stats']['total_interactions']}")
            print(f"  Mode: {report['agent_info']['mode'].upper()}")

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Custom AI Agent Meeting Scheduler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --config                     # Show configuration
  %(prog)s schedule "Team Meeting"     # Schedule basic meeting
  %(prog)s ai-schedule "Schedule urgent call with client tomorrow"
  %(prog)s view                        # View upcoming schedule
  %(prog)s analyze                     # Run AI analysis
  %(prog)s stats                       # Show statistics
  %(prog)s cancel 1                    # Cancel meeting #1
        """
    )
    
    parser.add_argument('--config', action='store_true', 
                       help='Show current configuration')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Schedule command
    schedule_parser = subparsers.add_parser('schedule', help='Schedule a meeting')
    schedule_parser.add_argument('title', help='Meeting title')
    schedule_parser.add_argument('--participants', default='', help='Participants')
    schedule_parser.add_argument('--start-time', default='', help='Start time (YYYY-MM-DD HH:MM)')
    schedule_parser.add_argument('--duration', type=int, default=60, help='Duration in minutes')
    schedule_parser.add_argument('--location', default='', help='Meeting location')
    schedule_parser.add_argument('--ai', action='store_true', help='Use AI scheduling')
    
    # AI schedule command
    ai_parser = subparsers.add_parser('ai-schedule', help='AI-powered natural language scheduling')
    ai_parser.add_argument('request', help='Natural language scheduling request')
    
    # View schedule command
    view_parser = subparsers.add_parser('view', help='View upcoming schedule')
    view_parser.add_argument('--days', type=int, default=7, help='Number of days to show')
    
    # Analyze command
    subparsers.add_parser('analyze', help='Run AI analysis')
    
    # Stats command
    subparsers.add_parser('stats', help='Show statistics')
    
    # Cancel command
    cancel_parser = subparsers.add_parser('cancel', help='Cancel a meeting')
    cancel_parser.add_argument('meeting_id', type=int, help='Meeting ID to cancel')
    
    # Interactive mode
    subparsers.add_parser('interactive', help='Launch interactive mode')
    
    # Demo mode
    subparsers.add_parser('demo', help='Run demo with sample data')
    
    args = parser.parse_args()
    
    # Show configuration if requested
    if args.config:
        config.show_config()
        return
    
    # Initialize CLI
    cli = MeetingSchedulerCLI()
    
    if args.command == 'demo':
        print("Running demo...")
        cli.basic_agent = CalendarAgent()
        create_sample_data()
        print("Demo data created! Try 'view' command to see sample meetings.")
        return
    
    # Initialize agents for other commands
    try:
        cli.initialize_agents()
    except Exception as e:
        print(f"Failed to initialize agents: {e}")
        return
    
    # Execute commands
    if args.command == 'schedule':
        success = cli.schedule_meeting(
            title=args.title,
            participants=args.participants,
            start_time=args.start_time,
            duration=args.duration,
            location=args.location,
            use_ai=args.ai
        )
        sys.exit(0 if success else 1)
        
    elif args.command == 'ai-schedule':
        success = cli.ai_schedule(args.request)
        sys.exit(0 if success else 1)
        
    elif args.command == 'view':
        cli.view_schedule(args.days)
        
    elif args.command == 'analyze':
        cli.ai_analyze()
        
    elif args.command == 'stats':
        cli.show_stats()
        
    elif args.command == 'cancel':
        success = cli.cancel_meeting(args.meeting_id)
        sys.exit(0 if success else 1)
        
    elif args.command == 'interactive':
        interactive_mode(cli)
        
    else:
        parser.print_help()

def interactive_mode(cli: MeetingSchedulerCLI):
    """Interactive command mode"""
    print("\nCustom AI Agent Meeting Scheduler - Interactive Mode")
    print("=" * 55)
    print("Commands:")
    print("  schedule <title> [options]  - Schedule a meeting")
    print("  ai <request>                - AI natural language scheduling")
    print("  view [days]                 - View schedule")
    print("  analyze                     - AI analysis")
    print("  stats                       - Show statistics")
    print("  cancel <id>                 - Cancel meeting")
    print("  help                        - Show this help")
    print("  exit                        - Exit")
    print()
    
    while True:
        try:
            command = input("> ").strip().split()
            if not command:
                continue
                
            cmd = command[0].lower()
            
            if cmd == 'exit':
                print("Goodbye!")
                break
            elif cmd == 'help':
                interactive_mode(cli)
            elif cmd == 'schedule':
                if len(command) < 2:
                    print("Usage: schedule <title> [--participants <list>] [--start-time <time>] [--duration <min>]")
                    continue
                cli.schedule_meeting(' '.join(command[1:]))
            elif cmd == 'ai':
                if len(command) < 2:
                    print("Usage: ai <natural language request>")
                    print("Example: ai 'schedule urgent meeting with john tomorrow at 2pm'")
                    continue
                request = ' '.join(command[1:])
                cli.ai_schedule(request)
            elif cmd == 'view':
                days = int(command[1]) if len(command) > 1 else 7
                cli.view_schedule(days)
            elif cmd == 'analyze':
                cli.ai_analyze()
            elif cmd == 'stats':
                cli.show_stats()
            elif cmd == 'cancel':
                if len(command) < 2:
                    print("Usage: cancel <meeting_id>")
                    continue
                try:
                    meeting_id = int(command[1])
                    cli.cancel_meeting(meeting_id)
                except ValueError:
                    print("Invalid meeting ID")
            else:
                print(f"Unknown command: {cmd}. Type 'help' for commands.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()
