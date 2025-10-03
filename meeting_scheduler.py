"""
Meeting Scheduler Agent - Core Module
====================================

A comprehensive AI-powered meeting scheduler with natural language processing,
conflict resolution, and smart calendar management capabilities.
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta, date
from typing import List, Dict, Optional, Tuple
import pandas as pd
import pytz
from dateutil.parser import parse as parse_date
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
Base = declarative_base()

class Meeting(Base):
    """SQLAlchemy model for storing meeting data"""
    __tablename__ = 'meetings'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    participants = Column(Text)  # JSON string or comma-separated
    location = Column(String(200))
    is_recurring = Column(Boolean, default=False)
    recurring_pattern = Column(String(50))  # 'weekly', 'biweekly', 'monthly'
    recurrence_end_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DatabaseManager:
    """Manages database operations for meetings"""
    
    def __init__(self, db_path: str = "meeting_scheduler.db"):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
    def add_meeting(self, **kwargs) -> Meeting:
        """Add a new meeting to the database"""
        try:
            # Parse datetime strings if provided
            if 'start_time' in kwargs and isinstance(kwargs['start_time'], str):
                kwargs['start_time'] = parse_date(kwargs['start_time'])
            if 'end_time' in kwargs and isinstance(kwargs['end_time'], str):
                kwargs['end_time'] = parse_date(kwargs['end_time'])
                
            meeting = Meeting(**kwargs)
            self.session.add(meeting)
            self.session.commit()
            logger.info(f"Added meeting: {meeting.title} at {meeting.start_time}")
            return meeting
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error adding meeting: {e}")
            raise
            
    def get_meetings(self, start_date: date = None, end_date: date = None) -> List[Meeting]:
        """Retrieve meetings within a date range"""
        query = self.session.query(Meeting)
        
        if start_date:
            query = query.filter(Meeting.start_time >= start_date)
        if end_date:
            query = query.filter(Meeting.start_time <= end_date)
            
        return query.order_by(Meeting.start_time).all()
    
    def get_meeting_by_id(self, meeting_id: int) -> Optional[Meeting]:
        """Get a specific meeting by ID"""
        return self.session.query(Meeting).filter(Meeting.id == meeting_id).first()
    
    def update_meeting(self, meeting_id: int, **updates) -> Optional[Meeting]:
        """Update an existing meeting"""
        try:
            meeting = self.get_meeting_by_id(meeting_id)
            if not meeting:
                return None
                
            for key, value in updates.items():
                if hasattr(meeting, key):
                    if key in ['start_time', 'end_time'] and isinstance(value, str):
                        value = parse_date(value)
                    setattr(meeting, key, value)
                    
            meeting.updated_at = datetime.utcnow()
            self.session.commit()
            logger.info(f"Updated meeting: {meeting.title}")
            return meeting
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error updating meeting: {e}")
            raise
            
    def delete_meeting(self, meeting_id: int) -> bool:
        """Delete a meeting by ID"""
        try:
            meeting = self.get_meeting_by_id(meeting_id)
            if meeting:
                self.session.delete(meeting)
                self.session.commit()
                logger.info(f"Deleted meeting: {meeting.title}")
                return True
            return False
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error deleting meeting: {e}")
            raise
    
    def get_conflicts(self, start_time: datetime, end_time: datetime, exclude_id: int = None) -> List[Meeting]:
        """Check for time conflicts with existing meetings"""
        query = self.session.query(Meeting).filter(
            Meeting.start_time < end_time,
            Meeting.end_time > start_time
        )
        
        if exclude_id:
            query = query.filter(Meeting.id != exclude_id)
            
        return query.all()

class GeminiIntegration:
    """Handles integration with Google's Gemini AI for natural language processing"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize Gemini integration
        Args:
            api_key: Google Generative AI API key. If None, will use hardcoded key
        """
        # Hardcoded Gemini API key for Custom AI Agent
        self.api_key = api_key or "AIzaSyA5w6gUBNgab_q04cQ6mh3KQjcwSvylwtc"
        self.client = None
        self.model_name = "gemini-2.0-flash"
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model_name)
            logger.info(f"Gemini {self.model_name} integration initialized successfully")
        except ImportError:
            logger.warning("google-generativeai not installed. LLM features disabled.")
        except Exception as e:
            logger.warning(f"Gemini initialization failed: {e}. LLM features disabled.")
    
    def parse_schedule_request(self, request: str) -> Dict:
        """
        Parse a natural language scheduling request using Gemini
        Returns a structured dictionary with scheduling details
        """
        if not self.client:
            return self._fallback_parse(request)
        
        try:
            prompt = f"""
            Parse this meeting scheduling request into structured JSON:
            "{request}"
            
            Extract and return ONLY a valid JSON object with these exact fields:
            {{
                "title": "Meeting title or subject",
                "participants": "Comma-separated participant names",
                "start_time": "YYYY-MM-DD HH:MM format or null",
                "duration": "Duration in minutes as integer",
                "location": "Meeting location or empty string",
                "recurring": false,
                "recurring_pattern": ""
            }}
            
            Rules:
            - If time not specified, use null for start_time
            - Extract participant names accurately
            - Default duration to 60 if not specified
            - Return ONLY the JSON, no other text
            """
            
            if self.client:
                response = self.client.generate_content(prompt)
                response_text = response.text.strip()
                
                # Clean up response to extract JSON
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0]
                elif "```" in response_text:
                    response_text = response_text.split("```")[1]
                
                try:
                    parsed_data = json.loads(response_text)
                    logger.info(f"Gemini parsed request: {request[:50]}...")
                    return parsed_data
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse Gemini JSON: {response_text[:100]}")
                    return self._fallback_parse(request)
            else:
                return self._fallback_parse(request)
            
        except Exception as e:
            logger.error(f"Error parsing with Gemini: {e}")
            return self._fallback_parse(request)
    
    def _fallback_parse(self, request: str) -> Dict:
        """Fallback parsing without LLM - basic keyword extraction"""
        import re
        
        # Extract common patterns
        title_match = re.search(r'(?:meeting|call|session)\s+(?:with|for)\s+([^.]+)', request, re.IGNORECASE)
        participants_match = re.search(r'(?:with|meeting)\s+([A-Za-z\s]+?)(?:\s+at|\s+on|\s+next)', request, re.IGNORECASE)
        time_match = re.search(r'(?:at|on)\s+([A-Za-z0-9\s:,]+(?:AM|PM|am|pm)?)', request, re.IGNORECASE)
        
        return {
            'title': title_match.group(1).strip() if title_match else 'Meeting',
            'participants': participants_match.group(1).strip() if participants_match else '',
            'start_time': None,  # Would need complex date parsing
            'duration': 60,  # Default 1 hour
            'location': '',
            'recurring': False,
            'recurring_pattern': ''
        }
    
    def generate_reschedule_message(self, original_time: str, suggested_times: List[str]) -> str:
        """Generate polite rescheduling messages"""
        if not self.client:
            return self._fallback_reschedule_message(original_time, suggested_times)
        
        try:
            prompt = f"""
            Generate a concise, professional email message for rescheduling a meeting.
            
            Original time: {original_time}
            Suggested alternatives: {', '.join(suggested_times[:3])}
            
            Format:
            Subject: [Meeting Reschedule Request]
            
            Body: Brief, polite message.
            
            Keep it professional, concise, and friendly.
            """
            
            if self.client:
                response = self.client.generate_content(prompt)
                return response.text.strip()
            else:
                return self._fallback_reschedule_message(original_time, suggested_times)
            
        except Exception as e:
            logger.error(f"Error generating reschedule message: {e}")
            return self._fallback_reschedule_message(original_time, suggested_times)
    
    def _fallback_reschedule_message(self, original_time: str, suggested_times: List[str]) -> str:
        """Fallback reschedule message without LLM"""
        return f"""
        Subject: Meeting Reschedule Request
        
        Hi there,
        
        I hope you're doing well. I need to reschedule our meeting originally planned for {original_time}.
        
        I have the following times available:
        {chr(10).join(f"- {time}" for time in suggested_times[:3])}
        
        Please let me know which works best for you.
        
        Best regards
        """

class ConflictResolver:
    """Handles meeting conflict detection and resolution"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def find_conflicts(self, start_time: datetime, end_time: datetime, exclude_id: int = None) -> List[Tuple[Meeting, str]]:
        """
        Find conflicts and describe them
        Returns list of (conflicting_meeting, conflict_description) tuples
        """
        conflicts = self.db_manager.get_conflicts(start_time, end_time, exclude_id)
        conflict_descriptions = []
        
        for meeting in conflicts:
            if start_time <= meeting.start_time < end_time:
                desc = f"Overlaps with start of '{meeting.title}'"
            elif start_time < meeting.end_time <= end_time:
                desc = f"Overlaps WITH end of '{meeting.title}'"
            elif meeting.start_time <= start_time and meeting.end_time >= end_time:
                desc = f"Completely covered by '{meeting.title}'"
            else:
                desc = f"Partially overlaps with '{meeting.title}'"
                
            conflict_descriptions.append((meeting, desc))
            
        return conflict_descriptions
    
    def suggest_alternatives(self, start_time: datetime, duration_minutes: int = 60, 
                           days_ahead: int = 7, exclude_id: int = None) -> List[datetime]:
        """
        Suggest alternative times that don't conflict
        
        Args:
            start_time: Desired start time
            duration_minutes: Meeting duration in minutes
            days_ahead: How many days to look ahead for alternatives
            exclude_id: Meeting ID to exclude from conflict checking
        """
        alternatives = []
        working_hours_start = start_time.replace(hour=9, minute=0, second=0, microsecond=0)
        working_hours_end = start_time.replace(hour=17, minute=0, second=0, microsecond=0)
        
        for day_offset in range(days_ahead):
            current_day = start_time.date() + timedelta(days=day_offset)
            
            # Skip weekends
            if current_day.weekday() > 4:
                continue
                
            day_start = datetime.combine(current_day, datetime.min.time().replace(hour=9))
            day_end = datetime.combine(current_day, datetime.min.time().replace(hour=17))
            
            slots = self._get_available_slots(day_start, day_end, duration_minutes, exclude_id)
            alternatives.extend(slots[:3])  # Limit to 3 per day
            
            if len(alternatives) >= 10:  # Limit total suggestions
                break
                
        return alternatives
    
    def _get_available_slots(self, day_start: datetime, day_end: datetime, 
                           duration_minutes: int, exclude_id: int) -> List[datetime]:
        """Get available time slots for a given day"""
        slots = []
        slot_duration = timedelta(minutes=30)  # Check every 30 minutes
        
        current_time = day_start
        while current_time + timedelta(minutes=duration_minutes) <= day_end:
            end_time = current_time + timedelta(minutes=duration_minutes)
            conflicts = self.db_manager.get_conflicts(current_time, end_time, exclude_id)
            
            if not conflicts:
                slots.append(current_time)
                
            current_time += slot_duration
            
        return slots

class CalendarAgent:
    """Main agent class that orchestrates all scheduling operations"""
    
    def __init__(self, db_path: str = "meeting_scheduler.db", gemini_api_key: str = None):
        self.db_manager = DatabaseManager(db_path)
        self.gemini = GeminiIntegration(gemini_api_key)
        self.conflict_resolver = ConflictResolver(self.db_manager)
        
    def schedule_meeting(self, **meeting_data) -> Dict:
        """
        Schedule a new meeting with conflict resolution
        
        Returns:
            Dict with 'success', 'meeting', 'conflicts', 'suggestions' keys
        """
        try:
            # Ensure end_time is set if only duration provided
            if 'duration' in meeting_data and 'end_time' not in meeting_data:
                start_time = meeting_data['start_time']
                if isinstance(start_time, str):
                    start_time = parse_date(start_time)
                end_time = start_time + timedelta(minutes=meeting_data['duration'])
                meeting_data['end_time'] = end_time
                del meeting_data['duration']
            
            start_time = meeting_data['start_time']
            end_time = meeting_data['end_time']
            
            if isinstance(start_time, str):
                start_time = parse_date(start_time)
            if isinstance(end_time, str):
                end_time = parse_date(end_time)
                
            # Check for conflicts
            conflicts = self.conflict_resolver.find_conflicts(start_time, end_time)
            
            if conflicts:
                # Suggest alternatives
                duration = int((end_time - start_time).total_seconds() / 60)
                suggestions = self.conflict_resolver.suggest_alternatives(
                    start_time, duration, exclude_id=None
                )
                
                return {
                    'success': False,
                    'conflicts': conflicts,
                    'suggestions': suggestions[:5],  # Top 5 suggestions
                    'gemini_message': self.gemini.generate_reschedule_message(
                        start_time.strftime('%Y-%m-%d %H:%M'), 
                        [s.strftime('%Y-%m-%d %H:%M') for s in suggestions[:3]]
                    )
                }
            
            # No conflicts, create the meeting
            meeting = self.db_manager.add_meeting(**meeting_data)
            
            return {
                'success': True,
                'meeting': meeting,
                'conflicts': [],
                'suggestions': []
            }
            
        except Exception as e:
            logger.error(f"Error scheduling meeting: {e}")
            return {
                'success': False,
                'error': str(e),
                'conflicts': [],
                'suggestions': []
            }
    
    def parse_and_schedule(self, natural_language_request: str) -> Dict:
        """Parse natural language request and schedule meeting"""
        parsed_data = self.gemini.parse_schedule_request(natural_language_request)
        return self.schedule_meeting(**parsed_data)
    
    def view_schedule(self, start_date: date = None, end_date: date = None) -> pd.DataFrame:
        """Return upcoming meetings as a pandas DataFrame"""
        meetings = self.db_manager.get_meetings(start_date, end_date)
        
        if not meetings:
            return pd.DataFrame(columns=['ID', 'Title', 'Start Time', 'End Time', 'Participants', 'Location'])
        
        data = []
        for meeting in meetings:
            data.append({
                'ID': meeting.id,
                'Title': meeting.title,
                'Start Time': meeting.start_time.strftime('%Y-%m-%d %H:%M'),
                'End Time': meeting.end_time.strftime('%Y-%m-%d %H:%M'),
                'Participants': meeting.participants or '',
                'Location': meeting.location or ''
            })
            
        return pd.DataFrame(data)
    
    def reschedule_meeting(self, meeting_id: int, new_start_time: datetime, **updates) -> Dict:
        """Reschedule an existing meeting"""
        try:
            old_meeting = self.db_manager.get_meeting_by_id(meeting_id)
            if not old_meeting:
                return {'success': False, 'error': 'Meeting not found'}
            
            # Calculate new end time
            duration = old_meeting.end_time - old_meeting.start_time
            new_end_time = new_start_time + duration
            
            # Check for conflicts (excluding the current meeting)
            conflicts = self.conflict_resolver.find_conflicts(new_start_time, new_end_time, meeting_id)
            
            if conflicts:
                duration_minutes = int(duration.total_seconds() / 60)
                suggestions = self.conflict_resolver.suggest_alternatives(
                    new_start_time, duration_minutes, exclude_id=meeting_id
                )
                
                return {
                    'success': False,
                    'conflicts': conflicts,
                    'suggestions': suggestions[:5]
                }
            
            # Update the meeting
            updates['start_time'] = new_start_time
            updates['end_time'] = new_end_time
            updated_meeting = self.db_manager.update_meeting(meeting_id, **updates)
            
            return {
                'success': True,
                'meeting': updated_meeting
            }
            
        except Exception as e:
            logger.error(f"Error rescheduling meeting: {e}")
            return {'success': False, 'error': str(e)}
    
    def cancel_meeting(self, meeting_id: int) -> bool:
        """Cancel/delete a meeting"""
        return self.db_manager.delete_meeting(meeting_id)
    
    def search_meetings(self, **criteria) -> List[Meeting]:
        """Search meetings by various criteria"""
        # This would be expanded with more sophisticated search logic
        return self.db_manager.get_meetings(
            criteria.get('start_date'),
            criteria.get('end_date')
        )

# Convenience functions for easy access
def create_sample_data():
    """Create sample meetings for demonstration"""
    agent = CalendarAgent()
    
    sample_meetings = [
        {
            'title': 'Weekly Team Standup',
            'description': 'Daily standup meeting with the development team',
            'start_time': datetime.now() + timedelta(days=1, hours=10),
            'end_time': datetime.now() + timedelta(days=1, hours=10, minutes=15),
            'participants': 'John, Sarah, Mike, Lisa',
            'location': 'Conference Room A',
            'is_recurring': True,
            'recurring_pattern': 'weekly'
        },
        {
            'title': 'Client Call - Project Review',
            'description': 'Monthly review with the main client',
            'start_time': datetime.now() + timedelta(days=3, hours=14),
            'end_time': datetime.now() + timedelta(days=3, hours=15),
            'participants': 'Emily Chen (Client), Sarah, Mike',
            'location': 'Virtual',
            'is_recurring': False
        },
        {
            'title': 'Sprint Planning Meeting',
            'description': 'Planning for the next development sprint',
            'start_time': datetime.now() + timedelta(days=7, hours=9),
            'end_time': datetime.now() + timedelta(days=7, hours=11),
            'participants': 'Entire Development Team',
            'location': 'Conference Room B',
            'is_recurring': True,
            'recurring_pattern': 'biweekly'
        }
    ]
    
    for meeting_data in sample_meetings:
        try:
            agent.schedule_meeting(**meeting_data)
        except Exception as e:
            logger.warning(f"Could not create sample meeting: {e}")

if __name__ == "__main__":
    # Demo usage
    print("Meeting Scheduler Agent - Demo")
    print("=" * 40)
    
    agent = CalendarAgent()
    
    # Create sample data
    create_sample_data()
    
    # View upcoming meetings
    print("\\nUpcoming Meetings:")
    print("-" * 20)
    df = agent.view_schedule()
    if not df.empty:
        print(df.to_string(index=False))
    else:
        print("No meetings scheduled.")
