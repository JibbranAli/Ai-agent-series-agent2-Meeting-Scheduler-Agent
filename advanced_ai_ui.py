"""
Advanced AI-Powered Calendar Interface
=====================================

Custom UI components integrating the advanced AI agent with enhanced 
reasoning, memory, and autonomous capabilities.
"""

import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import pandas as pd
from datetime import datetime, date, timedelta
import json
from typing import Dict, List, Optional, Any
from rich.console import Console
from rich.table import Table
from rich import print as rprint

# Import our custom AI agent
from custom_ai_agent import ReasonableAgent, AgentMode

class AdvancedAICalendarUI:
    """
    Advanced UI integrating the Custom AI Agent with intelligent reasoning
    """
    
    def __init__(self, user_id: str = "smart_user", agent_mode: AgentMode = AgentMode.BALANCED):
        self.user_id = user_id
        self.agent_mode = agent_mode
        
        # Initialize the custom AI agent
        self.ai_agent = ReasonableAgent(user_id=user_id, mode=agent_mode)
        
        # UI state
        self.current_context = {}
        self.ai_insights = {}
        self.proactive_alerts = []
        
        # Setup UI components
        self.setup_advanced_widgets()
        
        print(f"🧠 Advanced AI Calendar Interface initialized")
        print(f"👤 User: {user_id}")
        print(f"🤖 Agent Mode: {agent_mode.value}")
        
    def setup_advanced_widgets(self):
        """Setup advanced AI-powered widgets"""
        
        # Main container
        self.main_container = widgets.VBox()
        
        # AI Agent Status Header
        self.ai_header = widgets.HTML("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white;">
            <h1>🧠 Custom AI Meeting Scheduler Agent</h1>
            <p>Advanced reasoning • Autonomous decision-making • Learning patterns • Predictive scheduling</p>
        </div>
        """)
        
        # Agent Intelligence Panel
        self.intelligence_panel = self._create_intelligence_panel()
        
        # Advanced Controls
        self.advanced_controls = self._create_advanced_controls()
        
        # Autonomous Feature Toggle
        self.autonomous_panel = self._create_autonomous_panel()
        
        # AI Reasoning Interface
        self.reasoning_interface = self._create_reasoning_interface()
        
        # Context Analysis Display
        self.context_display = widgets.Output()
        
        # AI Insights Dashboard
        self.insights_dashboard = widgets.Output()
        
        # Proactive Alerts Area
        self.alerts_area = widgets.Output()
        
        # Natural Language Processing Enhanced
        self.enhanced_nl_input = widgets.Textarea(
            placeholder='Try intelligent requests: "Proactively schedule weekly reviews with Sarah considering my preferences and her availability" or "Smart-schedule a planning session optimizing for my productivity patterns"',
            description='🧠 Advanced AI Input:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='900px', height='80px')
        )
        
        self.ai_process_button = widgets.Button(
            description='🚀 AI Process & Schedule',
            button_style='info',
            tooltip='Let AI reason and schedule autonomously'
        )
        
        self.ai_analyze_button = widgets.Button(
            description='🔍 AI Analyze Context',
            button_style='success',
            tooltip='Perform deep context analysis'
        )
        
        # Learning Progress Display
        self.learning_display = widgets.Output()
        
        # Wire up handlers
        self._setup_handlers()
        
    def _create_intelligence_panel(self):
        """Create AI intelligence status panel"""
        
        # Mode selector
        mode_options = [(mode.value.title(), mode) for mode in AgentMode]
        self.mode_selector = widgets.Dropdown(
            options=mode_options,
            value=self.agent_mode,
            description='🧠 Agent Mode:',
            style={'description_width': 'initial'}
        )
        
        # Confidence level indicator
        self.confidence_gauge =进度条(widgets.FloatProgress(
            value=0.5,
            min=0, max=1,
            description='🎯 Confidence:',
            style={'description_width': 'initial', 'bar_color': 'green'}
        )
        
        # Memory indicator
        self.memory_indicator = widgets.HTML("""
        <div style="background: #f8f9fa; padding: 10px; border-radius: 5px;">
            <strong>💾 Memory:</strong> Loading patterns...<br>
            <strong>🧠 Learning:</strong> Ready to adapt<br>
            <strong>🎯 Success Rate:</strong> Initializing...
        </div>
        """)
        
        # Context insights summary
        self.context_summary = widgets.HTML("""
        <div style="background: #e3f2fd; padding: 10px; border-radius: 5px;">
            <strong>📊 Context:</strong> Analyzing user patterns...<br>
            <strong>🕐 Optimal Timing:</strong> Learning preferences...<br>
            <strong>⚖️ Calendar Balance:</strong> Monitoring stress levels...
        </div>
        """)
        
        return widgets.VBox([
            widgets.HTML("<h3>🧠 AI Intelligence Status</h3>"),
            widgets.HBox([self.mode_selector, self.confidence_gauge]),
            widgets.HBox([self.memory_indicator, self.context_summary])
        ])
    
    def _create_advanced_controls(self):
        """Create advanced control panel"""
        
        # Proactive recommendations button
        self.recommendations_button = widgets.Button(
            description='💡 Get AI Recommendations',
            button_style='warning',
            tooltip='Generate intelligent scheduling recommendations'
        )
        
        # Learning acceleration button
        self.learning_button = widgets.Button(
            description='📚 Accelerate Learning',
            button_style='info',
            tooltip='Perform intensive pattern analysis'
        )
        
        # Conflict prediction button
        self.predict_conflicts_button = widgets.Button(
            description='🔮 Predict Conflicts',
            button_style='success',
            tooltip='AI-powered conflict forecasting'
        )
        
        # Calendar optimization button
        self.optimize_button = widgets.Button(
            description='🔧 Optimize Calendar',
            button_style='primary',
            tooltip='Optimize schedule based on AI insights'
        )
        
        # Agent report button
        self.report_button = widgets.Button(
            description='📊 Full Agent Report',
            button_style='danger',
            tooltip='Generate comprehensive AI agent report'
        )
        
        return widgets.VBox([
            widgets.HTML("<h3>🚀 Advanced AI Controls</h3>"),
            widgets.GridBox(
                children=[
                    self.recommendations_button,
                    self.learning_button,
                    self.predict_conflicts_button,
                    self.optimize_button,
                    self.report_button
                ],
                layout=widgets.Layout(
                    width='100%',
                    grid_template_columns='1fr 1fr',
                    grid_gap='10px'
                )
            )
        ])
    
    def _create_autonomous_panel(self):
        """Create autonomous operation panel"""
        
        # Autonomous scheduling toggle
        self.autonomous_toggle = widgets.Checkbox(
            value=False,
            description='🚀 Enable Autonomous Scheduling',
            description_tooltip='Allow AI to make scheduling decisions independently'
        )
        
        # Confidence threshold for autonomous decisions
        self.confidence_slider = widgets.FloatSlider(
            value=0.7, min=0.3, max=0.9, step=0.1,
            description='AI阈值:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='300px')
        )
        
        # Proactive management options
        self.proactive_options = widgets.SelectMultiple(
            options=[
                'Auto Conflict Resolution',
                'Smart Time Suggestions', 
                'Predictive Scheduling',
                'Pattern Learning',
                'Personalized Optimization'
            ],
            value=['Auto Conflict Resolution', 'Smart Time Suggestions'],
            description='🤖 Active Features:',
            style={'description_width': 'initial'}
        )
        
        return widgets.VBox([
            widgets.HTML("<h3>🤖 自主操作设置</h3>"),
            self.autonomous_toggle,
            self.confidence_slider,
            self.proactive_options
        ])
    
    def _create_reasoning_interface(self):
        """Create AI reasoning explanation interface"""
        
        self.reasoning_output = widgets.Output()
        
        self.explain_button = widgets.Button(
            description='🧠 Explain AI Reasoning',
            button_style='info',
            tooltip='See how AI reached its decision'
        )
        
        self.challenge_button = widgets.Button(
            description='❓ Challenge Decision',
            button_style='warning',
            tooltip='Ask AI to reconsider its decision'
        )
        
        self.learn_from_button = widgets.Button(
            description='📚 Learn from This',
            button_style='success',
            tooltip='Use this interaction to improve AI'
        )
        
        return widgets.VBox([
            widgets.HTML("<h3>🧠 AI推理引擎</h3>"),
            widgets.HBox([self.explain_button, self.challenge_button, self.learn_from_button]),
            self.reasoning_output
        ])
    
    def _setup_handlers(self):
        """Setup event handlers for all buttons and interactions"""
        
        # Mode change handler
        self.mode_selector.observe(self._on_mode_change, names='value')
        
        # Button handlers
        self.ai_process_button.on_click(self._handle_ai_processing)
        self.ai_analyze_button.on_click(self._handle_context_analysis)
        self.recommendations_button.on_click(self._handle_recommendations)
        self.learning_button.on_click(self._handle_learning)
        self.predict_conflicts_button.on_click(self._handle_conflict_prediction)
        self.optimize_button.on_click(self._handle_calendar_optimization)
        self.report_button.on_click(self._handle_full_report)
        
        # Reasoning interface handlers
        self.explain_button.on_click(self._handle_explain_reasoning)
        self.challenge_button.on_click(self._handle_challenge_decision)
        self.learn_from_button.on_click(self._handle_learning_acceleration)
        
        # Autonomous controls
        self.autonomous_toggle.observe(self._on_autonomous_toggle, names='value')
        self.confidence_slider.observe(self._on_confidence_change, names='value')
        
    def _on_mode_change(self, change):
        """Handle agent mode change"""
        new_mode = change['new']
        self.ai_agent.set_mode(new_mode)
        
        with self.intelligence_panel:
            clear_output()
            display(HTML(f"<div style='color: green;'>🤖 Agent mode changed to: <strong>{new_mode.value}</strong></div>"))
        
        # Update UI elements based on mode
        if new_mode == AgentMode.AUTONOMOUS:
            self.autonomous_toggle.value = True
            self.confidence_gauge.description = '🎯 High Confidence Mode'
            self.confidence_gauge.style.bar_color = 'orange'
        elif new_mode == AgentMode.CONSERVATIVE:
            self.confidence_gauge.description = '🎯 Cautious Mode'
            self.confidence_gauge.style.bar_color = 'blue'
        else:
            self.confidence_gauge.description = '🎯 Balanced Mode'
            self.confidence_gauge.style.bar_color = 'green'
    
    def _on_autonomous_toggle(self, change):
        """Handle autonomous mode toggle"""
        autonomous_enabled = change['new']
        
        if autonomous_enabled:
            self.ai_agent.set_mode(AgentMode.AUTONOMOUS)
            display(HTML("<div style='color: orange;'>🤖 Autonomous scheduling enabled - AI will make independent decisions</div>"))
        else:
            self.ai_agent.set_mode(AgentMode.BALANCED)
            display(HTML("<div style='color: blue;'>💭 Balanced mode - AI will provide recommendations for approval</div>"))
    
    def _on_confidence_change(self, change):
        """Handle confidence threshold change"""
        threshold = change['new']
        self.ai_agent.confidence_threshold = threshold
        
        display(HTML(f"<div style='color: purple;'>🎯 Confidence threshold: <strong>{threshold:.1f}</strong></div>"))
    
    def _handle_ai_processing(self, button):
        """Handle AI-powered scheduling request processing"""
        request = self.enhanced_nl_input.value.strip()
        
        if not request:
            display(HTML("<div style='color: red;'>❌ Please provide a scheduling request for AI processing</div>"))
            return
        
        with self.context_display:
            clear_output()
            
            # Step 1: Advanced context analysis
            display(HTML("<h3>🔍 Step 1: AI Context Analysis</h3>"))
            context = self.ai_agent.analyze_context()
            self.current_context = context
            
            # Display context metrics
            context_table = Table(title="Context Analysis")
            context_table.add_column("Factor", style="cyan")
            context_table.add_column("Value", style="green")
            context_table.add_column("Impact", description="yellow")
            
            context_table.add_row("Calendar Stress", f"{context['calendar_stress_level']:.2f}",
                                "🟡 Balanced" if context['calendar_stress_level'] < 0.7 else "🔴 High")
            context_table.add_row("Conflict Probability", f"{context['conflict_probability']:.2f}",
                                "🟢 Low" if context['conflict_probability'] < 0.3 else "🟡 Medium")
            context_table.add_row("Current Hour", f"{context['hour_of_day']:02d}:00",
                                "🌅 Morning" if context['hour_of_day'] < 12 else "🌇 Afternoon")
            
            console = Console()
            console.print(context_table)
            
            # Step 2: Autonomous AI scheduling
            display(HTML("<h3>🤖 Step 2: AI Scheduling Decision</h3>"))
            
            result = self.ai_agent.autonomous_schedule(request)
            
            if result['success']:
                meeting = result['meeting']
                confidence = result.get('confidence', 0.8)
                
                # Update confidence gauge
                self.confidence_gauge.value = confidence
                
                display(HTML(f"""
                <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 15px; border-radius: 8px; color: white;">
                    <h4>✅ AI Successfully Scheduled</h4>
                    <p><strong>Meeting:</strong> {meeting.title}</p>
                    <p><strong>Time:</strong> {meeting.start_time.strftime('%Y-%m-%d %H:%M')}</p>
                    <p><strong>Participants:</strong> {meeting.participants or 'TBD'}</p>
                    <p><strong>AI Confidence:</strong> {confidence:.1%}</p>
                    <p><strong>Action:</strong> {result.get('agent_action', 'SCHEDULED')}</p>
                </div>
                """))
                
                if 'reasoning' in result:
                    display(HTML(f"<br><strong>🧠 AI Reasoning:</strong> {result['reasoning']}"))
                    
                if 'next_suggestions' in result:
                    display(HTML("<br><h4>💡 Next Meeting Suggestions:</h4>"))
                    for i, (slot, score) in enumerate(result['next_suggestions'][:3], 1):
                        display(HTML(f"{i}. {slot.strftime('%Y-%m-%d %H:%M')} (score: {score:.2f})"))
                        
            else:
                display(HTML(f"""
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 15px; border-radius: 8px; color: white;">
                    <h4>❌ AI Scheduling Decision</h4>
                    <p><strong>Status:</strong> {result.get('agent_action', 'NEEDS_INPUT')}</p>
                    <p><strong>Issue:</strong> {result.get('error', 'Requires human input')}</p>
                </div>
                """))
                
                # Show AI recommendations if available
                if 'recommendations' in result:
                    display(HTML("<br><h4>🧠 AI Recommendations:</h4>"))
                    
                    for i, rec in enumerate(result['recommendations'][:3], 1):
                        reasoning = rec.get('reasoning', 'Good slot')
                        display(HTML(f"""
                        <div style="border: 1px solid #ddd; padding: 10px; margin: 5px 0; border-radius: 5px;">
                            <strong>{i}. {rec['time'].strftime('%Y-%m-%d %H:%M')}</strong><br>
                            <small>Confidence: {rec['score']:.2f}</small><br>
                            <em>Reasoning: {reasoning}</em>
                        </div>
                        """))
            
            # Step 3: Learning update
            display(HTML("<h3>📚 Step 3: Learning Progress</h3>"))
            
            # Update agents insights based on this interaction
            insights = self.ai_agent.intelligent_recommendations()
            
            self.ai_insights = insights
            
            display(HTML(f"""
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
                <h4>📊 Updated AI Insights</h4>
                <p><strong>Success Rate:</strong> {insights.get('optimal_scheduling_times', {}).get('morning_preference', 0):.1%}</p>
                <p><strong>Calendar Optimization Score:</strong> {insights.get('calendar_optimization', {}).get('stress_level', 0):.2f}</p>
                <p><strong>Next Learning Focus:</strong> Conflict pattern recognition</p>
            </div>
            """))
    
    def _handle_context_analysis(self, button):
        """Handle deep context analysis"""
        with self.context_display:
            clear_output()
            
            display(HTML("<h2>🔍 Deep Context Analysis</h2>"))
            
            # Perform comprehensive analysis
            context = self.ai_agent.analyze_context()
            
            # Generate detailed insights
            insights = self.ai_agent.intelligent_recommendations()
            
            # Create detailed analysis table
            analysis_table = Table(title="Comprehensive Context Analysis")
            analysis_table.add_column("Metric", style="cyan")
            analysis_table.add_column("Current Value", style="green")
            analysis_table.add_column("AI Recommendation", style="yellow")
            
            analysis_table.add_row(
                "Calendar Stress", 
                f"{context['calendar_stress_level']:.2f}",
                "🟢 Optimized" if context['calendar_stress_level'] < 0.5 else "🟡 Moderate" if context['calendar_stress_level'] < 0.7 else "🔴 High"
            )
            
            analysis_table.add_row(
                "Meeting Preference Pattern",
                f"{insights['optimal_scheduling_times']['preferred_time_of_day']}",
                f"🎯 Focus on {insights['optimal_scheduling_times']['most_common_day']}"
            )
            
            optimal_patterns = insights['optimal_scheduling_times']
            analysis_table.add_row(
                "Schedule Optimization",
                f"{optimal_patterns['average_duration']:.1f} min avg",
                f"⚡ {'Shorter' if optimal_patterns['average_duration'] > 60 else 'Longer'} meetings recommended"
            )
            
            console.print(analysis_table)
            
            # Show personalized suggestions
            suggestions = insights.get('personalized_suggestions', [])
            if suggestions:
                display(HTML("<h3>💡 AI-Personalized Suggestions</h3>"))
                for i, suggestion in enumerate(suggestions[:5], 1):
                    display(HTML(f"<p>{i}. {suggestion}</p>"))
            
            # Update memory display
            self._update_memory_display()
    
    def _handle_recommendations(self, button):
        """Handle AI recommendations generation"""
        with self.recommendations_output:
            clear_output()
            
            display(HTML("<h2>💡 AI Smart Recommendations</h2>"))
            
            insights = self.ai_agent.intelligent_recommendations()
            
            # Calendar optimization recommendations
            optimization = insights.get('calendar_optimization', {})
            
            display(HTML(f"""
            <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 20px; border-radius: 10px;">
                <h3>🎯 Schedule Optimization</h3>
                <p><strong>Current Calendar Stress:</strong> {optimization.get('stress_level', 0):.1%}</p>
                <p><strong>Average Meeting Duration:</strong> {optimization.get('avg_meeting_duration', 60):.0f} minutes</p>
                <p><strong>Conflict Probability:</strong> {optimization.get('conflict_probability', 0):.1%}</p>
            </div>
            """))
            
            # Personalized suggestions
            suggestions = insights.get('personalized_suggestions', [])
            if suggestions:
                display(HTML("<h3>🤖 Personalized AI Suggestions</h3>"))
                for i, suggestion in enumerate(suggestions, 1):
                    display(HTML(f"""
                    <div style="background: #e3f2fd; padding: 10px; margin: 5px 0; border-radius: 5px;">
                        <strong>{i}.</strong> {suggestion}
                    </div>
                    """))
            
            # Timing optimization
            timing_patterns = insights.get('optimal_scheduling_times', {})
            display(HTML(f"""
            <div style="background: #fff3e0; padding: 15px; border-radius: 8px;">
                <h3>⏰ Optimal Timing Analysis</h3>
                <p><strong>Best Time of Day:</strong> {timing_patterns.get('preferred_time_of_day', 'Balanced')}</p>
                <p><strong>Most Productive Day:</strong> {timing_patterns.get('most_common_day', 'Friday')}</p>
                <p><strong>Ideal Meeting Duration:</strong> {timing_patterns.get('average_duration', 60):.0f} minutes</p>
            </div>
            """))
    
    def _handle_learning(self, button):
        """Handle AI learning acceleration"""
        with self.learning_display:
            clear_output()
            
            display(HTML("<h2>📚 AI Learning Acceleration</h2>"))
            display(HTML("<p>🧠 Performing intensive pattern analysis...</p>"))
            
            # Accelerate learning by analyzing more meetings
            meetings = self.ai_agent.calendar_agent.db_manager.get_meetings()
            
            if len(meetings) > 5:
                # Perform deep learning analysis
                total_interactions = len(self.ai_agent.memory.scheduling_history)
                
                display(HTML(f"""
                <div style="background: #f3e5f5; padding: 15px; border-radius: 8px;">
                    <h3>📊 Learning Progress</h3>
                    <p><strong>Total Interactions Analyzed:</strong> {total_interactions}</p>
                    <p><strong>Meeting Patterns Learned:</strong> {len(meetings)}</p>
                    <p><strong>AI Confidence Level:</strong> {self.ai_agent.confidence_threshold:.1f}</p>
                </div>
                """))
                
                # Update learning indicators
                self.memory_indicator.value = f"""
                <div style="background: #f8f9fa; padding: 10px; border-radius: 5px;">
                    <strong>💾 Memory:</strong> {total_interactions + len(meetings)} patterns loaded<br>
                    <strong>🧠 Learning:</strong> Actively adapting<br>
                    <strong>🎯 Success Rate:</strong> {self.ai_agent.insights.successful_rate:.1%}
                </div>
                """
                
                display(HTML("<div style='color: green;'>✅ Learning accelerated - AI is smarter!</div>"))
            else:
                display(HTML("<div style='color: orange;'>ℹ️ Need more meeting data for effective learning</div>"))
    
    def _handle_conflict_prediction(self, button):
        """Handle AI conflict prediction"""
        with self.alerts_area:
            clear_output()
            
            display(HTML("<h2>🔮 AI Conflict PREDICTION</h2>"))
            
            # Get proactive alerts
            alerts = self.ai_agent.proactive_conflict_resolution()
            
            if alerts:
                display(HTML("<h3>⚠️ Predicted Issues</h3>"))
                for alert in alerts:
                    urgency_color = "red" if alert['urgency'] == 'HIGH' else "orange" if alert['urgency'] == 'MEDIUM' else "blue"
                    display(HTML(f"""
                    <div style="background: #{urgency_color}20; border-left: 4px solid {urgency_color}; padding: 10px; margin: 5px 0;">
                        <strong>{alert['type']}:</strong> {alert['message']}
                        <br><small>Meeting: {alert['meeting'].title}</small>
                    </div>
                    """))
            else:
                display(HTML("<div style='color: green;'>✅ No predicted conflicts detected</div>"))
            
            # Predict future conflicts
            context = self.ai_agent.analyze_context()
            conflict_probability = context['conflict_probability']
            
            display(HTML(f"""
            <div style="background: #fff3e0; padding: 15px; border-radius: 8px;">
                <h3>📊 Conflict Risk Assessment</h3>
                <p><strong>Overall Conflict Risk:</strong> {conflict_probability:.1%}</p>
                <p><strong>Calendar Density:</strong> {"High" if context['calendar_stress_level'] > 0.7 else "Medium" if context['calendar_stress_level'] > 0.4 else "Low"}</p>
                <p><strong>Recommendation:</strong> {"Reduce scheduling frequency" if conflict_probability > 0.6 else "Current schedule is balanced"}</p>
            </div>
            """))
    
    def _handle_calendar_optimization(self, button):
        """Handle AI calendar optimization"""
        with self.insights_dashboard:
            clear_output()
            
            display(HTML("<h2>🔧 AI Calendar Optimization</h2>"))
            
            # Analyze current calendar
            meetings = self.ai_agent.calendar_agent.db_manager.get_meetings()
            context = self.ai_agent.analyze_context()
            
            # Generate optimization suggestions
            optimization_insights = []
            
            # Time distribution analysis
            morning_meetings = len([m for m in meetings if m.start_time.hour < 12])
            afternoon_meetings = len([m for m in meetings if m.start_time.hour >= 12])
            total_meetings = len(meetings)
            
            if total_meetings > 0:
                morning_ratio = morning_meetings / total_meetings
                if morning_ratio > 0.7:
                    optimization_insights.append("📅 Consider scheduling more afternoon meetings for better balance")
                elif morning_ratio < 0.3:
                    optimization_insights.append("🌅 Schedule more morning meetings to utilize peak productivity")
            
            # Duration optimization
            if meetings:
                avg_duration = sum((m.end_time - m.start_time).total_seconds() / 3600 for m in meetings) / len(meetings)
                if avg_duration > 1.5:
                    optimization_insights.append("⏱️ Consider shorter meetings - avg {:.1f}h is quite long".format(avg_duration))
                elif avg_duration < 0.5:
                    optimization_insights.append("💡 Meetings are very short ({:.1f}h) - consider combining similar topics".format(avg_duration))
            
            # Stress level optimization
            stress_level = context['calendar_stress_level']
            if stress_level > 0.7:
                optimization_insights.append("🔥 Calendar stress is high ({:.1%}) - consider breaking up long meeting blocks".format(stress_level))
            elif stress_level < 0.3:
                optimization_insights.append("✅ Calendar is well-balanced ({:.1%} utilization)".format(stress_level))
            
            # Display optimization results
            if optimization_insights:
                display(HTML("<h3>💡 Optimization Recommendations</h3>"))
                for insight in optimization_insights:
                    display(HTML(f"<p>{insight}</p>"))
            else:
                display(HTML("<div style='color: green;'>✅ Your calendar is already optimally configured!</div>"))
            
            # Calendar heatmap visualization
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            hours = range(9, 18)
            
            display(HTML("<h3>📊 Calendar Density Heatmap</h3>"))
            
            heatmap_html = "<table style='border-collapse: collapse; font-size: 12px;'>"
            heatmap_html += "<tr><td></td>"
            for day in days:
                heatmap_html += f"<td style='padding: 5px; background: #f0f0f0;'>{day}</td>"
            heatmap_html += "</tr>"
            
            for hour in hours:
                heatmap_html += f"<tr><td style='padding: 5px; background: #f0f0f0;'>{hour:02d}:00</td>"
                
                for day_idx, day in enumerate(days):
                    # Count meetings for this day/hour
                    day_meetings = [m for m in meetings if m.start_time.isoweekday() == day_idx + 1]
                    hour_meetings = len([m for m in day_meetings if m.start_time.hour == hour])
                    
                    # Color intensity based on meeting count
                    if hour_meetings == 0:
                        color = "#ffffff"
                    elif hour_meetings == 1:
                        color = "#e1f5fe"
                    elif hour_meetings == 2:
                        color = "#b3e5fc"
                    else:
                        color = "#81c9e4"
                    
                    heatmap_html += f"<td style='padding: 3px; background: {color}; text-align: center;'>{hour_meetings}</td>"
                
                heatmap_html += "</tr>"
            
            heatmap_html += "</table><br><small>Numbers show meeting count for each time slot</small>"
            
            display(HTML(heatmap_html))
    
    def _handle_full_report(self, button):
        """Generate full AI agent report"""
        with self.insights_dashboard:
            clear_output()
            
            display(HTML("<h1>📊 Complete AI Agent Report</h1>"))
            
            # Generate comprehensive report
            report = self.ai_agent.get_agent_report()
            
            # Agent info section
            agent_info = report['agent_info']
            display(HTML(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white;">
                <h2>🤖 Agent Information</h2>
                <p><strong>User ID:</strong> {agent_info['user_id']}</p>
                <p><strong>Current Mode:</strong> {agent_info['mode']}</p>
                <p><strong>Status:</strong> {"Active" if agent_info['is_active'] else "Standby"}</p>
            </div>
            """))
            
            # Memory statistics
            memory_stats = report['memory_stats']
            display(HTML(f"""
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
                <h3>💾 Memory Statistics</h3>
                <p><strong>Total Interactions:</strong> {memory_stats['total_interactions']}</p>
                <p><strong>Learning Confidence:</strong> {memory_stats['learning_confidence']}</p>
                <p><strong>Last Interaction:</strong> {memory_stats['last_interaction']}</p>
            </div>
            """))
            
            # AI insights
            insights = report['insights']
            display(HTML(f"""
            <div style="background: #e8f5e8; padding: 15px; border-radius: 8px;">
                <h3>🧠 AI Insights</h3>
                <p><strong>Success Rate:</strong> {insights['success_rate']:.1%}</p>
                <p><strong>Schedule Density:</strong> {insights['schedule_density']:.2f}</p>
                <p><strong>Calendar Stress:</strong> {insights['calendar_stress']:.1%}</p>
            </div>
            """))
            
            # Proactive alerts
            alerts = report['proactive_alerts']
            if alerts:
                display(HTML("<h3>🚨 Proactive Alerts</h3>"))
                for alert in alerts:
                    display(HTML(f"<p>• {alert['message']}</p>"))
            else:
                display(HTML("<p style='color: green;'>✅ No proactive alerts at this time</p>"))
            
            # Recommendations
            recommendations = report['recommendations']
            if recommendations:
                suggestions = recommendations['personalized_suggestions']
                if suggestions:
                    display(HTML("<h3>💡 AI Recommendations</h3>"))
                    for suggestion in suggestions:
                        display(HTML(f"<p>• {suggestion}</p>"))
    
    def _handle_explain_reasoning(self, button):
        """Explain AI reasoning process"""
        with self.reasoning_output:
            clear_output()
            
            display(HTML("<h2>🧠 AI Reasoning Explanation</h2>"))
            
            # Show the reasoning process for the last decision
            if hasattr(self, 'current_context') and self.current_context:
                display(HTML("<h3>📊 Context Factors Considered</h3>"))
                
                for factor, value in self.current_context.items():
                    if factor == 'user_availability_scores':
                        continue  # Skip complex nested data
                    
                    display(HTML(f"""
                    <div style="border: 1px solid #ddd; padding: 8px; margin: 3px 0; border-radius: 3px;">
                        <strong>{factor.replace('_', ' ').title()}:</strong> {value}
                    </div>
                    """))
                
                display(HTML("<h3>🧠 Decision Logic</h3>"))
                display(HTML("""
                <div style="background: #f0f8ff; padding: 15px; border-radius: 8px;">
                    <p><strong>Weighted Analysis:</strong></p>
                    <ul>
                        <li>Conflict Avoidance: 40% - Ensures no double-booking</li>
                        <li>User Preferences: 30% - Aligns with learned patterns</li>
                        <li>Calendar Balance: 20% - Maintains healthy schedule density</li>
                        <li>Urgency Factors: 10% - Considers meeting priority</li>
                    </ul>
                </div>
                """))
                
                display(HTML("<div style='color: purple;'>🧠 This explanation shows how AI considers multiple factors to make smart decisions!</div>"))
            else:
                display(HTML("<p style='color: orange;'>ℹ️ Run a scheduling operation first to see reasoning</p>"))
    
    def _handle_challenge_decision(self, button):
        """Allow user to challenge AI decision"""
        with self.reasoning_output:
            clear_output()
            
            display(HTML("<h2>❓ Challenge AI Decision</h2>"))
            display(HTML("<p>🤔 What would you like to challenge about the AI's decision?</p>"))
            
            # Challenge options
            challenge_options = [
                "The timing wasn't optimal for my workflow",
                "The duration doesn't match the meeting type", 
                "There are better alternative times available",
                "The conflict reasoning was incorrect",
                "I have additional constraints not considered"
            ]
            
            challenge_widget = widgets.Dropdown(
                options=challenge_options,
            description='Challenge:',
            style={'description_width': 'initial'}
            )
            
            challenge_button = widgets.Button(
                description='Submit Challenge',
                button_style='warning'
            )
            
            def handle_challenge_submission(button):
                challenge_type = challenge_widget.value
                
                # Update AI learning with challenge
                if challenge_type in self.ai_agent.memory.learning_data:
                    self.ai_agent.memory.learning_data[challenge_type] += 1
                else:
                    self.ai_agent.memory.learning_data[challenge_type] = 1
                
                self.ai_agent.save_state()
                
                display(HTML(f"""
                <div style="background: #fff3cd; padding: 15px; border-radius: 8px;">
                    <h4>✅ Challenge Recorded</h4>
                    <p>AI has learned from your feedback: "{challenge_type}"</p>
                    <p>This will improve future scheduling decisions.</p>
                </div>
                """))
            
            challenge_button.on_click(handle_challenge_submission)
            
            display(widgets.VBox([challenge_widget, challenge_button]))
    
    def _handle_learning_acceleration(self, button):
        """Handle learn from interaction"""
        with self.reasoning_output:
            clear_output()
            
            display(HTML("<h2>📚 Learn from This Interaction</h2>"))
            
            # Get user feedback
            feedback_widget = widgets.Textarea(
                placeholder="What did you think about this AI interaction? Any specific feedback?",
                description="Feedback:",
                style={'description_width': 'initial'},
                layout=widgets.Layout(width='80%', height='100px')
            )
            
            rating_widget = widgets.IntSlider(
                value=5,
                min=1,
                max=5,
                description='Rating:',
                style={'description_width': 'initial'}
            )
            
            learn_button = widgets.Button(
                description='Teach AI',
                button_style='success'
            )
            
            def handle_learning(button):
                feedback = feedback_widget.value
                rating = rating_widget.value
                
                # Add to learning data
                learning_entry = {
                    'timestamp': datetime.now(),
                    'feedback': feedback,
                    'rating': rating,
                    'context_snapshot': self.current_context.copy() if self.current_context else {}
                }
                
                self.ai_agent.memory.scheduling_history.append(learning_entry)
                self.ai_agent._update_contextual_insights()
                self.ai_agent.save_state()
                
                display(HTML(f"""
                <div style="background: #d4edda; padding: 15px; border-radius: 8px;">
                    <h4>🎉 AI Learning Update</h4>
                    <p><strong>Your Rating:</strong> {rating}/5 stars</p>
                    <p><strong>Feedback:</strong> {feedback}</p>
                    <p>✅ AI has learned from this interaction and will improve future decisions!</p>
                </div>
                """))
                
                # Update success rate display
                success_rate = self.ai_agent.insights.successful_rate
                self.confidence_gauge.value = success_rate
            
            learn_button.on_click(handle_learning)
            
            display(widgets.VBox([
                widgets.HTML("<p>📚 Help the AI learn by providing feedback:</p>"),
                rating_widget,
                feedback_widget,
                learn_button
            ]))
    
    def _update_memory_display(self):
        """Update memory indicator display"""
        total_interactions = len(self.ai_agent.memory.scheduling_history)
        success_rate = self.ai_agent.insights.successful_rate
        
        self.memory_indicator.value = f"""
        <div style="background: #f8f9fa; padding: 10px; border-radius: 5px;">
            <strong>💾 Memory:</strong> {total_interactions} patterns loaded<br>
            <strong>🧠 Learning:</strong> Actively adapting<br>
            <strong>🎯 Success Rate:</strong> {success_rate:.1%}
        </div>
        """
    
    def show_interface(self):
        """Display the complete advanced AI interface"""
        # Build main layout
        self.main_container.children = [
            self.ai_header,
            widgets.HTML("<hr>"),
            
            # Top row: Intelligence panel and advanced controls
            widgets.HBox([
                self.intelligence_panel,
                self.advanced_controls
            ]),
            
            widgets.HTML("<hr>"),
            
            # Autonomous operations
            self.autonomous_panel,
            
            widgets.HTML("<hr>"),
            
            # Reasoning interface
            self.reasoning_interface,
            
            widgets.HTML("<hr>"),
            
            # Main interaction area
            widgets.VBox([
                widgets.HTML("<h3>🧠 Advanced AI Scheduling</h3>"),
                widgets.HBox([self.enhanced_nl_input, self.ai_process_button, self.ai_analyze_button]),
                widgets.HTML("<br>"),
                widgets.Accordion(children=[
                    self.context_display, 
                    self.insights_dashboard, 
                    self.alerts_area,
                    self.learning_display,
                    self.reasoning_output
                ], titles=['Context Analysis', 'AI Insights Dashboard', 'Proactive Alerts', 'Learning Progress', 'Reasoning Engine'])
            ])
        ]
        
        # Display everything
        display(self.main_container)
        
        # Initial context analysis
        with self.context_display:
            display(HTML("<h3>🔍 Initial Context Analysis</h3>"))
            context = self.ai_agent.analyze_context()
            insights = self.ai_agent.intelligent_recommendations()
            
            display(HTML(f"""
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
                <h4>📊 Current Status</h4>
                <p><strong>Calendar Stress:</strong> {context['calendar_stress_level']:.1%}</p>
                <p><strong>Conflict Risk:</strong> {context['conflict_probability']:.1%}</p>
                <p><strong>AI Mode:</strong> {self.agent_mode.value.title()}</p>
                <p><strong>Learning Status:</strong> Ready to assist</p>
            </div>
            """))


# Convenience functions for easy access
def create_advanced_ai_ui(user_id: str = "smart_user", mode: AgentMode = AgentMode.BALANCED):
    """Create and display the advanced AI calendar interface"""
    ui = AdvancedAICalendarUI(user_id=user_id, agent_mode=mode)
    ui.show_interface()
    
    return ui, ui.ai_agent

def demo_ai_capabilities():
    """Demonstrate advanced AI capabilities"""
    print("🤖 Advanced AI Capabilities Demo")
    print("=" * 50)
    
    ui, agent = create_advanced_ai_ui(user_id="demo_user", mode=AgentMode.BALANCED)
    
    print("✅ Advanced AI interface launched!")
    print("🧠 Try the intelligent scheduling features:")
    print("  • Natural language processing")
    print("  • Autonomous decision making") 
    print("  • Proactive conflict resolution")
    print("  • Personalized recommendations")
    print("  • Learning from feedback")
    
    return ui, agent

if __name__ == "__main__":
    # Launch demo
    demo_ui, demo_agent = demo_ai_capabilities()
