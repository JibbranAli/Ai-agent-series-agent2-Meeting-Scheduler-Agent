"""
Custom AI Agent for Advanced Meeting Management
=============================================

A sophisticated AI agent with reasoning capabilities, memory system, 
learning patterns, and autonomous decision-making for intelligent calendar management.
"""

import os
import json
import pickle
import sqlite3
from datetime import datetime, timedelta, date
from typing import List, Dict, Optional, Tuple, Any
import pandas as pd
import re
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import time

# Enhanced logging for agent behavior
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AgentMode(Enum):
    """Different operational modes for the AI agent"""
    CONSERVATIVE = "conservative"  # Cautious scheduling, lots of confirmations
    AGGRESSIVE = "aggressive"     # Fast scheduling, minimal confirmation
    BALANCED = "balanced"        # Balanced approach
    LEARNING = "learning"        # Observing and learning user patterns
    AUTONOMOUS = "autonomous"    # Fully autonomous operation

class Priority(Enum):
    """Meeting priority levels"""
    CRITICAL = "critical"       # Cannot be moved
    HIGH = "high"              # Hard to move
    MEDIUM = "medium"          # Normal flexibility
    LOW = "low"                # Easy to move
    FLEXIBLE = "flexible"       # Very flexible

@dataclass
class AgentMemory:
    """Memory structure for the AI agent"""
    user_id: str
    meeting_patterns: Dict[str, Any]
    user_preferences: Dict[str, Any]
    scheduling_history: List[Dict]
    conflict_resolution_preferences: Dict[str, Any]
    communication_style: str
    last_interaction: datetime
    learning_data: Dict[str, float]

@dataclass
class ContextualInsights:
    """Contextual information for decision making"""
    user_schedule_density: float
    preferred_timing_patterns: Dict[str, float]
    meeting_type_preferences: Dict[str, Dict]
    location_preferences: Dict[str, float]
    conflict_resolution_history: List[Dict]
    successful_rate: float

class ReasonableAgent:
    """
    Advanced AI Agent with reasoning capabilities and autonomous decision-making
    """
    
    def __init__(self, user_id: str = "default_user", mode: AgentMode = AgentMode.BALANCED):
        self.user_id = user_id
        self.mode = mode
        self.memory_file = f"agent_memory_{user_id}.pkl"
        self.insights_file = f"agent_insights_{user_id}.json"
        
        # Initialize core components
        from meeting_scheduler import CalendarAgent
        self.calendar_agent = CalendarAgent()
        self.memory = self._load_memory()
        self.insights = self._load_insights()
        
        # Agent state
        self.is_active = False
        self.current_context = {}
        self.pending_decisions = []
        
        # Learning parameters
        self.learning_rate = 0.1
        self.confidence_threshold = 0.7
        
        logger.info(f"🤖 Custom AI Agent initialized for user: {user_id}")
        logger.info(f"🧠 Agent Mode: {mode.value}")
        
    def _load_memory(self) -> AgentMemory:
        """Load agent memory from persistent storage"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'rb') as f:
                    memory_data = pickle.load(f)
                    return AgentMemory(**memory_data)
        except Exception as e:
            logger.warning(f"Could not load memory: {e}")
            
        # Return default memory
        return AgentMemory(
            user_id=self.user_id,
            meeting_patterns={},
            user_preferences={},
            scheduling_history=[],
            conflict_resolution_preferences={},
            communication_style="professional",
            last_interaction=datetime.now(),
            learning_data={}
        )
    
    def _save_memory(self):
        """Save agent memory to persistent storage"""
        try:
            with open(self.memory_file, 'wb') as f:
                pickle.dump(asdict(self.memory), f)
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")
    
    def _load_insights(self) -> ContextualInsights:
        """Load contextual insights from storage"""
        try:
            if os.path.exists(self.insights_file):
                with open(self.insights_file, 'r') as f:
                    insights_data = json.load(f)
                    # Convert datetime strings back to datetime objects where needed
                    insights_data['conflict_resolution_history'] = [
                        {**d, 'timestamp': datetime.fromisoformat(d['timestamp']) if 'timestamp' in d else datetime.now()}
                        for d in insights_data.get('conflict_resolution_history', [])
                    ]
                    return ContextualInsights(**insights_data)
        except Exception as e:
            logger.warning(f"Could not load insights: {e}")
            
        return ContextualInsights(
            user_schedule_density=0.0,
            preferred_timing_patterns={},
            meeting_type_preferences={},
            location_preferences={},
            conflict_resolution_history=[],
            successful_rate=0.0
        )
    
    def _save_insights(self):
        """Save contextual insights to storage"""
        try:
            insights_data = asdict(self.insights)
            # Convert datetime objects to strings for JSON serialization
            insights_data['conflict_resolution_history'] = [
                {**d, 'timestamp': d['timestamp'].isoformat() if 'timestamp' in d else datetime.now().isoformat()}
                for d in insights_data.get('conflict_resolution_history', [])
            ]
            with open(self.insights_file, 'w') as f:
                json.dump(insights_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save insights: {e}")
    
    def analyze_context(self) -> Dict[str, Any]:
        """
        Analyze current context for intelligent decision making
        """
        context = {
            'current_time': datetime.now(),
            'day_of_week': datetime.now().weekday(),
            'hour_of_day': datetime.now().hour,
            'user_availability_scores': self._calculate_availability_scores(),
            'conflict_probability': self._estimate_conflict_probability(),
            'optimal_timing': self._find_optimal_timing_patterns(),
            'user_mood_indicator': self._analyze_user_mood(),
            'calendar_stress_level': self._calculate_calendar_stress()
        }
        
        self.current_context = context
        logger.info(f"🧠 Context analysis completed: {len(context)} factors considered")
        return context
    
    def _calculate_availability_scores(self) -> Dict[str, float]:
        """Calculate availability scores for different times"""
        meetings = self.calendar_agent.db_manager.get_meetings()
        time_slots = {}
        
        # Analyze next 14 days
        for day_offset in range(14):
            day = datetime.now().date() + timedelta(days=day_offset)
            busy_hours = set()
            
            for meeting in meetings:
                if meeting.start_time.date() == day:
                    start_hour = meeting.start_time.hour
                    end_hour = meeting.end_time.hour
                    busy_hours.update(range(start_hour, end_hour + 1))
            
            # Calculate availability for each hour (0.0 = completely free, 1.0 = very busy)
            day_scores = {}
            for hour in range(9, 18):  # Working hours
                day_scores[f"{hour}:00"] = 1.0 if hour in busy_hours else 0.0
                
            time_slots[day.isoformat()] = day_scores
            
        return time_slots
    
    def _estimate_conflict_probability(self) -> float:
        """Estimate probability of scheduling conflicts based on history"""
        meetings = self.calendar_agent.db_manager.get_meetings()
        if len(meetings) < 10:
            return 0.3  # Default moderate probability
            
        # Analyze scheduling density
        busy_hours = 0
        total_slots = 0
        
        for meeting in meetings:
            duration_hours = (meeting.end_time - meeting.start_time).total_seconds() / 3600
            busy_hours += duration_hours
            total_slots += duration_hours
            
        density = busy_hours / total_slots if total_slots > 0 else 0
        conflict_probability = min(density * 1.5, 0.9)  # Cap at 90%
        
        logger.info(f"🎯 Estimated conflict probability: {conflict_probability:.2f}")
        return conflict_probability
    
    def _find_optimal_timing_patterns(self) -> Dict[str, Any]:
        """Discover optimal timing patterns from user history"""
        meetings = self.calendar_agent.db_manager.get_meetings()
        
        if len(meetings) < 5:
            return {
                'preferred_time_of_day': 'morning',
                'most_common_day': 'Friday', 
                'average_duration': 1
            }
            
        # Analyze timing preferences
        morning_meetings = len([m for m in meetings if m.start_time.hour < 12])
        afternoon_meetings = len([m for m in meetings if m.start_time.hour >= 12])
        total = len(meetings)
        circular_preferences = {
            'morning_preference': morning_meetings / total if total > 0 else 0.5,
            'afternoon_preference': afternoon_meetings / total if total > 0 else 0.5
        }
        
        # Learn which days are preferred
        day_counts = {}
        for meeting in meetings:
            day = meeting.start_time.strftime('%A')
            day_counts[day] = day_counts.get(day, 0) + 1
            
        most_common_day = max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else 'Friday'
        preferred_time = 'morning' if circular_preferences['morning_preference'] > 0.5 else 'afternoon'
        
        optimal_patterns = {
            'preferred_time_of_day': preferred_time,
            'most_common_day': most_common_day,
            'average_duration': sum((m.end_time - m.start_time).total_seconds() / 3600 for m in meetings) / len(meetings) if meetings else 1
        }
        
        return optimal_patterns
    
    def _analyze_user_mood(self) -> Dict[str, float]:
        """Analyze user mood and stress indicators from scheduling patterns"""
        all_meetings = self.calendar_agent.db_manager.get_meetings()
        recent_meetings = [m for m in all_meetings if m.created_at > datetime.now() - timedelta(days=7)]
        
        if len(recent_meetings) < 3:
            return {'stress_level': 0.3, 'productivity_indicator': 0.7, 'balance_score': 0.6}
            
        # Analyze indicators
        cancelations = len([m for m in recent_meetings if 'cancel' in m.title.lower()])
        urgent_meetings = len([m for m in recent_meetings if m.description and 'urgent' in m.description.lower()])
        long_meetings = len([m for m in recent_meetings if (m.end_time - m.start_time).total_seconds() > 7200])  # >2 hours
        
        stress_level = min((cancelations + urgent_meetings + long_meetings) / len(recent_meetings), 1.0)
        
        stress_indicators = {
            'stress_level': stress_level,
            'productivity_indicator': 1.0 - min((cancelations / max(len(recent_meetings), 1)) * 2, 1.0),
            'balance_score': max(0.0, 1.0 - (stress_level * 0.5))
        }
        
        logger.info(f"😊 Mood analysis: stress={stress_indicators['stress_level']:.2f}, productivity={stress_indicators['productivity_indicator']:.2f}")
        return stress_indicators
    
    def _calculate_calendar_stress(self) -> float:
        """Calculate how stressed/full the calendar is"""
        meetings = self.calendar_agent.db_manager.get_meetings()
        
        # Calculate calendar density for next 30 days
        total_busy_time = 0
        total_work_time = 0
        
        for day_offset in range(30):
            day = datetime.now().date() + timedelta(days=day_offset)
            day_meetings = [m for m in meetings if m.start_time.date() == day]
            
            daily_busy = sum((m.end_time - m.start_time).total_seconds() for m in day_meetings)
            daily_work_hours = 8 * 3600  # 8 working hours per day
            
            total_busy_time += daily_busy
            total_work_time += daily_work_hours
            
        stress_level = total_busy_time / total_work_time if total_work_time > 0 else 0
        return min(stress_level, 1.0)
    
    def autonomous_schedule(self, request: str) -> Dict[str, Any]:
        """
        Autonomous scheduling with full AI reasoning
        """
        logger.info(f"🤖 Autonomous scheduling initiated for: {request}")
        
        # Step 1: Analyze context
        context = self.analyze_context()
        
        # Step 2: Enhanced natural language processing
        parsed_request = self._enhanced_nlp_parse(request)
        
        # Step 3: Intelligent slot finding
        optimal_slots = self._find_intelligent_slots(parsed_request, context)
        
        # Step 4: Autonomous decision making
        if self.mode == AgentMode.AUTONOMOUS:
            return self._make_autonomous_decision(parsed_request, optimal_slots, context)
        else:
            return self._make_balanced_decision(parsed_request, optimal_slots, context)
    
    def _enhanced_nlp_parse(self, request: str) -> Dict[str, Any]:
        """Enhanced natural language processing with context awareness"""
        
        # Contextually aware parsing
        base_parse = self.calendar_agent.gemini.parse_schedule_request(request)
        
        # Infer missing information from context
        if not base_parse.get('start_time'):
            base_parse['start_time'] = self._infer_preferred_time()
        
        if not base_parse.get('duration'):
            base_parse['duration'] = self._infer_preferred_duration(request)
            
        if not base_parse.get('location'):
            base_parse['location'] = self._infer_preferred_location()
            
        if not base_parse.get('priority'):
            base_parse['priority'] = self._infer_priority(request)
        
        # Learn from this parsing for future improvements
        self._update_learning_data(request, base_parse)
        
        return base_parse
    
    def _infer_preferred_time(self) -> Optional[datetime]:
        """Infer preferred time based on user patterns"""
        optimal_patterns = self._find_optimal_timing_patterns()
        
        preferred_hour = 9 if optimal_patterns['preferred_time_of_day'] == 'morning' else 14
        today = datetime.now().date()
        
        # Find the next available day matching user preferences
        for day_offset in range(1, 8):
            candidate_day = today + timedelta(days=day_offset)
            
            # Check if this aligns with user's preferred day pattern
            if candidate_day.strftime('%A') == optimal_patterns['most_common_day']:
                return datetime.combine(candidate_day, datetime.min.time().replace(hour=preferred_hour))
        
        # Fallback: next working day
        tomorrow = today + timedelta(days=1)
        return datetime.combine(tomorrow, datetime.min.time().replace(hour=preferred_hour))
    
    def _infer_preferred_duration(self, request: str) -> int:
        """Infer preferred duration based on context and request"""
        # Look for explicit duration mentions
        duration_patterns = [
            (r'(\d+)\s*min', lambda m: int(m.group(1))),
            (r'(\d+\.\d+)\s*hour', lambda m: int(float(m.group(1)) * 60)),
            (r'(\d+)\s*hour', lambda m: int(m.group(1)) * 60),
        ]
        
        for pattern, converter in duration_patterns:
            match = re.search(pattern, request, re.IGNORECASE)
            if match:
                return converter(match)
        
        # Infer from context and user patterns
        optimal_patterns = self._find_optimal_timing_patterns()
        base_duration = int(optimal_patterns['average_duration'] * 60)
        
        # Adjust based on meeting type keywords
        if any(word in request.lower() for word in ['standup', 'brief', 'quick', 'sync']):
            return min(base_duration, 30)
        elif any(word in request.lower() for word in ['planning', 'review', 'deep', 'brainstorm']):
            return max(base_duration, 120)
        
        return base_duration
    
    def _infer_preferred_location(self) -> str:
        """Infer preferred location based on user patterns"""
        meetings = self.calendar_agent.db_manager.get_meetings()
        
        location_counts = {}
        for meeting in meetings:
            if meeting.location:
                location_counts[meeting.location] = location_counts.get(meeting.location, 0) + 1
        
        if location_counts:
            most_popular = max(location_counts.items(), key=lambda x: x[1])[0]
            
            # Return most popular location with slight variation
            if 'virtual' in most_popular.lower() or 'zoom' in most_popular.lower():
                return 'Virtual Meeting'
            elif 'conference' in most_popular.lower():
                return 'Conference Room A'
            else:
                return most_popular
                
        return 'Virtual Meeting'  # Default modern preference
    
    def _infer_priority(self, request: str) -> Priority:
        """Infer meeting priority based on request content"""
        urgent_keywords = ['urgent', 'asap', 'immediately', 'critical', 'important', 'deadline']
        flexible_keywords = ['whenever', 'flexible', 'open', 'any time']
        
        request_lower = request.lower()
        
        if any(keyword in request_lower for keyword in urgent_keywords):
            return Priority.CRITICAL
        elif any(keyword in request_lower for keyword in flexible_keywords):
            return Priority.FLEXIBLE
        else:
            return Priority.MEDIUM
    
    def _find_intelligent_slots(self, parsed_request: Dict, context: Dict) -> List[Tuple[datetime, float]]:
        """
        Find optimal time slots using AI reasoning
        Returns list of (slot_time, confidence_score) tuples
        """
        slots = []
        
        # Analyze multiple factors to score slots
        target_date = parsed_request.get('start_time')
        if isinstance(target_date, str):
            target_date = parse_date(target_date)
        
        # Score slots based on multiple criteria
        for day_offset in range(14):  # Check next 2 weeks
            day = datetime.now().date() + timedelta(days=day_offset)
            
            for hour in range(9, 17):  # Working hours
                slot_time = datetime.combine(day, datetime.min.time().replace(hour=hour))
                
                if slot_time.date() < datetime.now().date():
                    continue
                    
                # Calculate confidence score
                score = self._calculate_slot_score(slot_time, parsed_request, context)
                if score > 0.3:  # Minimum threshold
                    slots.append((slot_time, score))
        
        # Sort by confidence score and return top candidates
        slots.sort(key=lambda x: x[1], reverse=True)
        return slots[:10]  # Top 10 suggestions
    
    def _calculate_slot_score(self, slot_time: datetime, parsed_request: Dict, context: Dict) -> float:
        """Calculate confidence score for a specific time slot"""
        score = 0.0
        
        # Factor 1: Conflict avoidance (40% weight)
        conflicts = self.calendar_agent.conflict_resolver.find_conflicts(
            slot_time, 
            slot_time + timedelta(minutes=parsed_request.get('duration', 60))
        )
        conflict_score = 0.0 if conflicts else 1.0
        
        # Factor 2: User preference alignment (30% weight)
        preferences = self._find_optimal_timing_patterns()
        hour_preference = 0.8 if preferences['preferred_time_of_day'] == 'morning' and slot_time.hour < 12 else 0.8 if preferences['preferred_time_of_day'] == 'afternoon' and slot_time.hour >= 12 else 0.5
        
        # Factor 3: Calendar stress level (20% weight)
        stress_factor = 0.8 if context['calendar_stress_level'] < 0.6 else 0.3
        
        # Factor 4: Immediate vs planning preference (10% weight)
        urgency_factor = self._calculate_urgency_factor(parsed_request, slot_time)
        
        # Weighted combination
        score = (conflict_score * 0.4 + 
                hour_preference * 0.3 + 
                stress_factor * 0.2 + 
                urgency_factor * 0.1)
        
        return score
    
    def _calculate_urgency_factor(self, parsed_request: Dict, slot_time: datetime) -> float:
        """Calculate urgency-based preference for slot timing"""
        days_from_now = (slot_time.date() - datetime.now().date()).days
        
        # High urgency should prefer sooner slots
        if parsed_request.get('priority') == Priority.CRITICAL:
            return max(0.0, 1.0 - (days_from_now * 0.2))
        elif parsed_request.get('priority') == Priority.FLEXIBLE:
            return max(0.0, days_from_now * 0.1)  # Flexible can wait
        else:
            return 1.0 / (1.0 + days_from_now * 0.2)  # Balanced
    
    def _make_autonomous_decision(self, parsed_request: Dict, optimal_slots: List, context: Dict) -> Dict[str, Any]:
        """Make fully autonomous scheduling decision"""
        if not optimal_slots:
            return {
                'success': False,
                'error': 'No suitable time slots found',
                'agent_action': 'SEARCH_EXPANDED'
            }
        
        # Select best slot autonomously
        best_slot, best_score = optimal_slots[0]
        
        # Autonomous scheduling with high confidence
        if best_score > self.confidence_threshold:
            parsed_request['start_time'] = best_slot
            result = self.calendar_agent.schedule_meeting(**parsed_request)
            
            if result['success']:
                # Learn successful scheduling pattern
                self._learn_successful_pattern(parsed_request, context)
                
                return {
                    'success': True,
                    'meeting': result['meeting'],
                    'agent_action': 'AUTONOMOUS_SCHEDULING',
                    'confidence': best_score,
                    'reasoning': f"Autonomous scheduling: selected optimal slot with {best_score:.2f} confidence",
                    'next_suggestions': optimal_slots[1:5]  # Show alternatives
                }
        
        return {
            'success': False,
            'error': 'Confidence too low for autonomous scheduling',
            'agent_action': 'REQUEST_CONFIRMATION',
            'suggestions': optimal_slots,
            'recommended_slot': optimal_slots[0]
        }
    
    def _make_balanced_decision(self, parsed_request: Dict, optimal_slots: List, context: Dict) -> Dict[str, Any]:
        """Make balanced decision requiring some user confirmation"""
        if not optimal_slots:
            return {
                'success': False,
                'error': 'No suitable time slots found',
                'agent_action': 'SEARCH_EXPANDED'
            }
        
        # Present top options to user
        recommendations = []
        for slot_time, score in optimal_slots[:5]:
            recommendations.append({
                'time': slot_time,
                'score': score,
                'reasoning': self._generate_reasoning(slot_time, score, context)
            })
        
        return {
            'success': False,  # Requires user confirmation
            'agent_action': 'RECOMMEND_SLOTS',
            'recommendations': recommendations,
            'suggested_auto_schedule': recommendations[0] if recommendations[0]['score'] > 0.8 else None
        }
    
    def _generate_reasoning(self, slot_time: datetime, score: float, context: Dict) -> str:
        """Generate human-readable reasoning for slot selection"""
        reasoning_parts = []
        
        if score > 0.8:
            reasoning_parts.append("High confidence recommendation")
        
        preferences = self._find_optimal_timing_patterns()
        if preferences['preferred_time_of_day'] == 'morning' and slot_time.hour < 12:
            reasoning_parts.append("Matches your morning preference")
        elif preferences['preferred_time_of_day'] == 'afternoon' and slot_time.hour >= 12:
            reasoning_parts.append("Aligns with your afternoon schedule")
        
        if context['calendar_stress_level'] < 0.5:
            reasoning_parts.append("Calendar has good availability")
        
        if slot_time.date() == datetime.now().date() + timedelta(days=1):
            reasoning_parts.append("Tomorrow - good balance of planning vs urgency")
        
        return " • ".join(reasoning_parts) if reasoning_parts else "Meets basic scheduling criteria"
    
    def _update_learning_data(self, request: str, parsed_data: Dict):
        """Update learning data from user interactions"""
        key = f"{self.user_id}_parsing_patterns"
        current_data = self.memory.learning_data.get(key, {})
        
        # Track successful parsing patterns
        for field in ['title', 'duration', 'participants', 'location']:
            if parsed_data.get(field):
                field_key = f"{field}_success_count"
                current_data[field_key] = current_data.get(field_key, 0) + 1
        
        current_data['total_interactions'] = current_data.get('total_interactions', 0) + 1
        self.memory.learning_data[key] = current_data
    
    def _learn_successful_pattern(self, parsed_request: Dict, context: Dict):
        """Learn from successful scheduling patterns"""
        pattern = {
            'timestamp': datetime.now(),
            'successful_command': parsed_request,
            'context_snapshot': context,
            'user_feedback_score': 1.0  # Success = positive feedback
        }
        
        self.memory.scheduling_history.append(pattern)
        
        # Keep only recent history (last 100 interactions)
        if len(self.memory.scheduling_history) > 100:
            self.memory.scheduling_history = self.memory.scheduling_history[-100:]
        
        # Update insights
        self._update_contextual_insights()
    
    def _update_contextual_insights(self):
        """Update contextual insights based on recent activity"""
        recent_patterns = self.memory.scheduling_history[-20:] if self.memory.scheduling_history else []
        
        if recent_patterns:
            success_rate = len([p for p in recent_patterns if p.get('user_feedback_score', 0) > 0.5]) / len(recent_patterns)
            self.insights.successful_rate = success_rate
            
        # Save updated insights
        self._save_insights()
    
    def proactive_conflict_resolution(self):
        """Proactively identify and resolve potential conflicts"""
        logger.info("🔮 Engaging proactive conflict resolution mode")
        
        # Find meetings in the next 7 days
        upcoming_meetings = self.calendar_agent.db_manager.get_meetings(
            datetime.now().date(),
            (datetime.now() + timedelta(days=7)).date()
        )
        
        alerts = []
        
        for meeting in upcoming_meetings:
            # Check for potential issues
            time_to_meeting = meeting.start_time - datetime.now()
            
            # Alert if meeting is very soon and has no location
            if time_to_meeting.total_seconds() < 3600 and not meeting.location:
                alerts.append({
                    'type': 'MISSING_LOCATION',
                    'meeting': meeting,
                    'urgency': 'HIGH',
                    'message': f"Meeting '{meeting.title}' starts in {int(time_to_meeting.total_seconds()/60)} minutes but has no location"
                })
            
            # Alert if there are back-to-back meetings with no gap
            overlapping = self.calendar_agent.conflict_resolver.find_conflicts(
                meeting.start_time - timedelta(minutes=5),  # Small buffer
                meeting.end_time + timedelta(minutes=5)
            )
            
            if len(overlapping) > 1:
                alerts.append({
                    'type': 'BACK_TO_BACK',
                    'meeting': meeting,
                    'urgency': 'MEDIUM',
                    'message': f"Meeting '{meeting.title}' overlaps with other meetings - consider rescheduling"
                })
        
        return alerts
    
    def intelligent_recommendations(self, request: str = None) -> Dict[str, Any]:
        """
        Provide intelligent recommendations based on learned patterns
        """
        recommendations = {
            'optimal_scheduling_times': self._find_optimal_timing_patterns(),
            'productivity_insights': self._analyze_user_mood(),
            'calendar_optimization': {
                'stress_level': self._calculate_calendar_stress(),
                'avg_meeting_duration': self._get_average_duration(),
                'conflict_probability': self._estimate_conflict_probability()
            },
            'personalized_suggestions': self._generate_personalized_suggestions()
        }
        
        return recommendations
    
    def _get_average_duration(self) -> float:
        """Get average meeting duration in minutes"""
        meetings = self.calendar_agent.db_manager.get_meetings()
        if not meetings:
            return 60  # Default
            
        total_duration = sum((m.end_time - m.start_time).total_seconds() for m in meetings)
        return total_duration / len(meetings) / 60  # Convert to minutes
    
    def _generate_personalized_suggestions(self) -> List[str]:
        """Get personalized scheduling suggestions"""
        suggestions = []
        
        patterns = self._find_optimal_timing_patterns()
        stress = self._calculate_calendar_stress()
        
        if stress > 0.7:
            suggestions.append("Consider scheduling more meetings in your preferred morning slots")
            suggestions.append("Reduce meeting duration by 15 minutes for better productivity")
        
        if patterns.get('preferred_time_of_day') == 'morning':
            suggestions.append("You tend to prefer mornings - consider scheduling more early meetings")
        
        # Check for optimization opportunities
        availability_scores = self._calculate_availability_scores()
        best_day = max(availability_scores.keys(), key=lambda k: sum([1-v for v in availability_scores[k].values()]))
        suggestions.append(f"{best_day} appears to be your most available day")
        
        return suggestions
    
    def set_mode(self, mode: AgentMode):
        """Change agent operational mode"""
        self.mode = mode
        logger.info(f"🤖 Agent mode changed to: {mode.value}")
        
        # Adjust behavior parameters based on mode
        if mode == AgentMode.AUTONOMOUS:
            self.confidence_threshold = 0.6
        elif mode == AgentMode.CONSERVATIVE:
            self.confidence_threshold = 0.8
        elif mode == AgentMode.BALANCED:
            self.confidence_threshold = 0.7
    
    def save_state(self):
        """Save current agent state"""
        self._save_memory()
        self._save_insights()
        logger.info("💾 Agent state saved successfully")
    
    def get_agent_report(self) -> Dict[str, Any]:
        """Generate comprehensive agent report"""
        return {
            'agent_info': {
                'user_id': self.user_id,
                'mode': self.mode.value,
                'is_active': self.is_active
            },
            'memory_stats': {
                'total_interactions': len(self.memory.scheduling_history),
                'learning_confidence': sum(self.memory.learning_data.get(self.user_id + '_parsing_patterns', {}).get(f'{field}_success_count', 0) 
                                        for field in ['title', 'duration', 'participants', 'location']),
                'last_interaction': self.memory.last_interaction.isoformat()
            },
            'insights': {
                'success_rate': self.insights.successful_rate,
                'schedule_density': self.insights.user_schedule_density,
                'optimal_patterns': self._find_optimal_timing_patterns(),
                'calendar_stress': self._calculate_calendar_stress()
            },
            'proactive_alerts': self.proactive_conflict_resolution(),
            'recommendations': self.intelligent_recommendations()
        }


# Example usage and demonstration
def create_custom_ai_agent_demo():
    """Demonstrate the custom AI agent capabilities"""
    print("🤖 Custom AI Agent Demo")
    print("=" * 50)
    
    # Create agent
    agent = ReasonableAgent(user_id="demo_user", mode=AgentMode.BALANCED)
    
    # Analyze current context
    context = agent.analyze_context()
    print(f"📊 Context analysis completed - {len(context)} factors analyzed")
    
    # Get intelligent recommendations
    recommendations = agent.intelligent_recommendations()
    print(f"💡 Generated {len(recommendations['personalized_suggestions'])} personalized recommendations")
    
    # Show agent report
    report = agent.get_agent_report()
    print(f"📈 Agent success rate: {report['insights']['success_rate']:.2f}")
    print(f"🎯 Calendar stress level: {report['insights']['calendar_stress']:.2f}")
    
    # Test autonomous scheduling
    test_request = "Schedule a quick sync with the marketing team tomorrow"
    result = agent.autonomous_schedule(test_request)
    print(f"🔮 Autonomous scheduling result: {result['success']}")
    if result.get('agent_action'):
        print(f"🤖 Agent action: {result['agent_action']}")
    
    # Save state?
    agent.save_state()
    print("✅ Agent state saved for future sessions")
    
    return agent

if __name__ == "__main__":
    # Run demo
    demo_agent = create_custom_ai_agent_demo()
