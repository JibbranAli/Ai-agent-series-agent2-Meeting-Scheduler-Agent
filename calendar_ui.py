"""
Calendar UI Module for Jupyter Notebook
======================================

Provides interactive widgets and display functions for the Meeting Scheduler Agent
in Jupyter notebook environment.
"""

import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import pandas as pd
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional
import json

class CalendarUI:
    """Interactive UI components for the meeting scheduler"""
    
    def __init__(self, calendar_agent):
        self.agent = calendar_agent
        self.setup_widgets()
        
    def setup_widgets(self):
        """Initialize all interactive widgets"""
        
        # Main container
        self.main_container = widgets.VBox()
        
        # Title
        self.title = widgets.HTML("<h2>📅 Smart Meeting Scheduler Agent</h2>")
        
        # Control buttons
        self.refresh_button = widgets.Button(
            description='🔄 Refresh',
            button_style='info',
            tooltip='Refresh the calendar view'
        )
        
        self.new_meeting_button = widgets.Button(
            description='➕ New Meeting',
            button_style='success',
            tooltip='Schedule a new meeting'
        )
        
        self.view_meetings_button = widgets.Button(
            description='📋 View All',
            button_style='primary',
            tooltip='View all meetings'
        )
        
        self.clear_data_button = widgets.Button(
            description='🗑️ Clear All',
            button_style='danger',
            tooltip='Clear all meeting data'
        )
        
        # Natural language input
        self.nl_input = widgets.Text(
            placeholder='Type a natural language request, e.g., "Schedule a meeting with John next Tuesday at 3 PM"',
            description='🗣️ Natural Language:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='800px')
        )
        
        self.submit_nl_button = widgets.Button(
            description='✨ Parse & Schedule',
            button_style='warning',
            tooltip='Parse and schedule using AI'
        )
        
        # Meeting form widgets
        self.meeting_form_container = widgets.VBox()
        
        self.meeting_title = widgets.Text(
            placeholder='Meeting title',
            description='Title:',
            layout=widgets.Layout(width='400px')
        )
        
        self.meeting_participants = widgets.Text(
            placeholder='John, Sarah, Mike',
            description='Participants:',
            layout=widgets.Layout(width='400px')
        )
        
        self.meeting_location = widgets.Text(
            placeholder='Conference Room A or Virtual',
            description='Location:',
            layout=widgets.Layout(width='400px')
        )
        
        self.meeting_date = widgets.DatePicker(
            description='Date:',
            value=date.today()
        )
        
        self.meeting_time = widgets.TimePicker(
            description='Time:',
            tooltips=['Start time']
        )
        
        self.meeting_duration = widgets.Dropdown(
            options=[15, 30, 45, 60, 90, 120, 180],
            value=60,
            description='Duration (minutes):'
        )
        
        self.meeting_description = widgets.Textarea(
            placeholder='Meeting description or agenda...',
            description='Description:',
            layout=widgets.Layout(width='400px', height='100px')
        )
        
        self.recurring_checkbox = widgets.Checkbox(
            description='Is this a recurring meeting?',
            value=False
        )
        
        self.recurring_pattern = widgets.Dropdown(
            options=['weekly', 'biweekly', 'monthly'],
            value='weekly',
            description='Pattern:',
            disabled=True
        )
        
        self.submit_button = widgets.Button(
            description='📅 Schedule Meeting',
            button_style='success',
            tooltip='Schedule the meeting'
        )
        
        self.cancel_form_button = widgets.Button(
            description='❌ Cancel',
            button_style='warning',
            tooltip='Cancel form'
        )
        
        # Meeting management
        self.meeting_id_input = widgets.IntText(
            placeholder='Enter meeting ID',
            description='Meeting ID:',
            value=1,
            layout=widgets.Layout(width='200px')
        )
        
        self.delete_button = widgets.Button(
            description='🗑️ Delete Meeting',
            button_style='danger',
            tooltip='Delete selected meeting'
        )
        
        self.reschedule_button = widgets.Button(
            description='🔄 Reschedule',
            button_style='info',
            tooltip='Reschedule selected meeting'
        )
        
        # Output areas
        self.output_area = widgets.Output()
        self.schedule_output = widgets.Output()
        
        # Wire up button handlers
        self.setup_handlers()
        
        # Initially hide the form
        self.hide_meeting_form()
        
    def setup_handlers(self):
        """Connect buttons to their handler functions"""
        
        self.refresh_button.on_click(self.refresh_calendar)
        self.new_meeting_button.on_click(self.show_meeting_form)
        self.view_meetings_button.on_click(self.view_all_meetings)
        self.clear_data_button.on_click(self.clear_all_data)
        
        self.submit_nl_button.on_click(self.handle_natural_language)
        
        self.submit_button.on_click(self.handle_form_submit)
        self.cancel_form_button.on_click(self.hide_meeting_form)
        
        self.delete_button.on_click(self.handle_delete_meeting)
        self.reschedule_button.on_click(self.handle_reschedule)
        
        self.recurring_checkbox.observe(self.toggle_recurring_options, names='value')
        
    def refresh_calendar(self, button):
        """Refresh and display current calendar"""
        with self.output_area:
            clear_output()
            self.display_current_schedule()
            
    def display_current_schedule(self):
        """Display upcoming meetings in a formatted table"""
        df = self.agent.view_schedule()
        
        if df.empty:
            display(HTML("<h3>📅 No meetings scheduled</h3><p>Click 'New Meeting' to schedule your first meeting!</p>"))
        else:
            # Style the DataFrame for better display
            styled_df = df.style.set_properties(**{
                'text-align': 'left',
                'font-size': '12px'
            }).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#f0f0f0'),
                                           ('font-weight', 'bold'),
                                           ('text-align', 'center')]}
            ])
            
            display(HTML("<h3>📅 Upcoming Meetings</h3>"))
            display(styled_df)
            
            # Add summary statistics
            total_meetings = len(df)
            today_meetings = len(df[df['Start Time'].str.contains(datetime.now().strftime('%Y-%m-%d'))])
            
            display(HTML(f"""
                <div style="margin-top: 15px; padding: 10px; background-color: #f8f9fa; border-radius: 5px;">
                    <strong>📊 Summary:</strong> {total_meetings} total meetings • {today_meetings} meetings today
                </div>
            """))
            
    def show_meeting_form(self, button):
        """Display the meeting creation form"""
        # Clear any previous form
        self.meeting_form_container.children = []
        
        # Build form layout
        form_title = widgets.HTML("<h3>📝 Schedule New Meeting</h3>")
        
        form_grid = widgets.GridBox(
            children=[
                self.meeting_title,
                self.meeting_participants,
                self.meeting_location,
                self.meeting_description,
                widgets.VBox([self.meeting_date, self.meeting_time]),
                widgets.VBox([self.meeting_duration, self.recurring_checkbox, self.recurring_pattern]),
                widgets.HBox([self.submit_button, self.cancel_form_button])
            ],
            layout=widgets.Layout(
                width='800px',
                grid_template_columns='1fr 1fr',
                grid_gap='10px'
            )
        )
        
        self.meeting_form_container.children = [form_title, form_grid]
        
        # Show form in output area
        with self.output_area:
            clear_output()
            display(self.meeting_form_container)
            
    def hide_meeting_form(self, button=None):
        """Hide the meeting form"""
        self.meeting_form_container.children = []
        
    def handle_form_submit(self, button):
        """Process the meeting form submission"""
        try:
            # Gather form data
            meeting_data = {
                'title': self.meeting_title.value,
                'participants': self.meeting_participants.value,
                'location': self.meeting_location.value,
                'description': self.meeting_description.value,
                'start_time': datetime.combine(
                    self.meeting_date.value, 
                    self.meeting_time.value if self.meeting_time.value else datetime.min.time().replace(hour=9)
                ),
                'duration': self.meeting_duration.value,
                'is_recurring': self.recurring_checkbox.value,
                'recurring_pattern': self.recurring_pattern.value if self.recurring_checkbox.value else ''
            }
            
            # Remove empty fields
            meeting_data = {k: v for k, v in meeting_data.items() if v}
            
            # Validate required fields
            if not meeting_data.get('title'):
                with self.output_area:
                    display(HTML("<div style='color: red;'>❌ Please provide a meeting title.</div>"))
                return
                
            # Schedule the meeting
            result = self.agent.schedule_meeting(**meeting_data)
            
            with self.output_area:
                clear_output()
                
                if result['success']:
                    display(HTML("<div style='color: green;'>✅ Meeting scheduled successfully!</div>"))
                    self.hide_meeting_form()
                    # Clear the form
                    self.meeting_title.value = ''
                    self.meeting_participants.value = ''
                    self.meeting_location.value = ''
                    self.meeting_description.value = ''
                else:
                    if 'conflicts' in result:
                        conflicts_html = "<br>".join([f"• {desc}" for _, desc in result['conflicts']])
                        suggestions_html = "<br>".join([f"• {s.strftime('%Y-%m-%d %H:%M')}" 
                                                      for s in result.get('suggestions', [])])
                        
                        display(HTML(f"""
                        <div style='color: orange;'>
                        <h4>⚠️ Time Conflict Detected!</h4>
                        <p><strong>Conflicts:</strong></p>
                        <p>{conflicts_html}</p>
                        
                        <p><strong>Suggested Alternative Times:</strong></p>
                        <p>{suggestions_html}</p>
                        
                        <details>
                        <summary>💌 AI-Generated Reschedule Message</summary>
                        <pre style='background: #f5f5f5; padding: 10px; margin-top: 5px;'>
{result.get('gemini_message', '')}
                        </pre>
                        </details>
                        </div>
                        """))
                    else:
                        display(HTML(f"<div style='color: red;'>❌ Error: {result.get('error', 'Unknown error')}</div>"))
                        
        except Exception as e:
            with self.output_area:
                display(HTML(f"<div style='color: red;'>❌ Error scheduling meeting: {str(e)}</div>"))
                
    def handle_natural_language(self, button):
        """Process natural language scheduling request"""
        request = self.nl_input.value.strip()
        
        if not request:
            with self.output_area:
                display(HTML("<div style='color: red;'>❌ Please enter a natural language request.</div>"))
            return
            
        with self.output_area:
            clear_output()
            display(HTML(f"🤖 <strong>Processing request:</strong> '{request}'<br><br>"))
            
            try:
                result = self.agent.parse_and_schedule(request)
                
                if result['success']:
                    display(HTML("<div style='color: green;'>✅ Meeting scheduled successfully from natural language!</div>"))
                else:
                    if 'error' in result:
                        display(HTML(f"<div style='color: red;'>❌ Error: {result['error']}</div>"))
                    else:
                        display(HTML("<div style='color: red;'>❌ Could not parse the request. Please try a more specific format.</div>"))
                        
                # Clear the input
                self.nl_input.value = ''
                
            except Exception as e:
                display(HTML(f"<div style='color: red;'>❌ Error processing request: {str(e)}</div>"))
                
    def view_all_meetings(self, button):
        """Display all meetings with management options"""
        with self.output_area:
            clear_output()
            
            df = self.agent.view_schedule()
            
            if df.empty:
                display(HTML("<h3>📋 No meetings found</h3>"))
            else:
                display(HTML("<h3>📋 All Meetings</h3>"))
                display(df.style.set_properties(**{
                    'text-align': 'left',
                    'font-size': '12px'
                }))
                
                # Management controls
                display(HTML("<h4>🔧 Meeting Management</h4>"))
                
                management_controls = widgets.VBox([
                    widgets.HBox([
                        self.meeting_id_input,
                        self.delete_button,
                        self.reschedule_button
                    ], layout=widgets.Layout(justify_content='flex-start'))
                ])
                
                display(management_controls)
                
    def handle_delete_meeting(self, button):
        """Delete a meeting by ID"""
        meeting_id = self.meeting_id_input.value
        
        if not meeting_id:
            with self.output_area:
                display(HTML("<div style='color: red;'>❌ Please enter a meeting ID.</div>"))
            return
            
        try:
            # Get meeting details for confirmation
            meetings = self.agent.db_manager.get_meetings()
            meeting_to_delete = next((m for m in meetings if m.id == meeting_id), None)
            
            if not meeting_to_delete:
                with self.output_area:
                    display(HTML(f"<div style='color: red;'>❌ No meeting found with ID {meeting_id}.</div>"))
                return
                
            # Show confirmation dialog (simple for now)
            confirmation_html = f"""
            <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <h4>⚠️ Confirm Deletion</h4>
                <p><strong>Meeting:</strong> {meeting_to_delete.title}</p>
                <p><strong>Time:</strong> {meeting_to_delete.start_time.strftime('%Y-%m-%d %H:%M')}</p>
                <p><strong>Participants:</strong> {meeting_to_delete.participants or 'No participants listed'}</p>
                <br>
                <button onclick="confirmDelete()" style="background-color: #dc3545; color: white; padding: 8px 16px; border: none; border-radius: 4px;">✅ Confirm Delete</button>
                <script>
                function confirmDelete() {{
                    // This would normally trigger the actual delete
                    alert('Meeting deletion would be confirmed here');
                }}
                </script>
            </div>
            """
            
            # For demo purposes, actually delete without user interaction
            success = self.agent.cancel_meeting(meeting_id)
            
            with self.output_area:
                if success:
                    display(HTML("<div style='color: green;'>✅ Meeting deleted successfully!</div>"))
                else:
                    display(HTML("<div style='color: red;'>❌ Failed to delete meeting.</div>"))
                    
        except Exception as e:
            with self.output_area:
                display(HTML(f"<div style='color: red;'>❌ Error deleting meeting: {str(e)}</div>"))
                
    def handle_reschedule(self, button):
        """Reschedule a meeting"""
        meeting_id = self.meeting_id_input.value
        
        if not meeting_id:
            with self.output_area:
                display(HTML("<div style='color: red;'>❌ Please enter a meeting ID.</div>"))
            return
            
        # Create rescheduling form (simplified)
        with self.output_area:
            clear_output()
            
            reschedule_html = f"""
            <h3>🔄 Reschedule Meeting (ID: {meeting_id})</h3>
            <p><strong>Note:</strong> Advanced rescheduling interface would be here.</p>
            <p>For now, you can modify meeting details directly in the database or use the natural language input.</p>
            <p><em>Try: "Reschedule meeting {meeting_id} to tomorrow at 2 PM"</em></p>
            """
            
            display(HTML(reschedule_html))
            
            # Show the natural language input focused on rescheduling
            reschedule_nl_input = widgets.Text(
                placeholder=f"Reschedule meeting {meeting_id} to...",
                description='🗣️ Reschedule:',
                style={'description_width': 'initial'},
                layout=widgets.Layout(width='600px')
            )
            
            reschedule_button = widgets.Button(
                description='🔄 Reschedule',
                button_style='info'
            )
            
            def handle_reschedule_nl(button):
                request = reschedule_nl_input.value
                if request:
                    display(HTML(f"🤖 Reschedule request: '{request}'<br>"))
                    # Here you would parse and execute the reschedule logic
                    
            reschedule_button.on_click(handle_reschedule_nl)
            display(widgets.HBox([reschedule_nl_input, reschedule_button]))
            
    def clear_all_data(self, button):
        """Clear all meeting data (with confirmation)"""
        with self.output_area:
            clear_output()
            
            warning_html = """
            <div style="background-color: #f8d7da; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <h4>⚠️ Clear All Data</h4>
                <p><strong>Warning:</strong> This will delete ALL meetings from the database.</p>
                <p>This action cannot be undone.</p>
                <br>
                <button onclick="clearData()" style="background-color: #dc3545; color: white; padding: 8px 16px; border: none; border-radius: 4px;">🗑️ Confirm Clear All</button>
                <br><br>
                <small>Click the button above to confirm clearing all data.</small>
            </div>
            """
            
            display(HTML(warning_html))
            
            # For safety, require explicit confirmation
            confirm_button = widgets.Button(
                description='🗑️ Really Clear All Data',
                button_style='danger',
                tooltip='This will permanently delete all meetings'
            )
            
            def confirm_clear_data(button):
                try:
                    # Clear the database (this is a simplified version)
                    meetings = self.agent.db_manager.get_meetings()
                    deleted_count = 0
                    
                    for meeting in meetings:
                        if self.agent.db_manager.delete_meeting(meeting.id):
                            deleted_count += 1
                            
                    with self.output_area:
                        display(HTML(f"""
                        <div style='color: green;'>
                        ✅ Cleared {deleted_count} meetings from the database.
                        </div>
                        """))
                        
                except Exception as e:
                    with self.output_area:
                        display(HTML(f"<div style='color: red;'>❌ Error clearing data: {str(e)}</div>"))
                        
            confirm_button.on_click(confirm_clear_data)
            display(confirm_button)
            
    def toggle_recurring_options(self, change):
        """Enable/disable recurring pattern options"""
        self.recurring_pattern.disabled = not change['new']
        
    def show_dashboard(self):
        """Display the main dashboard"""
        # Build the main interface
        control_buttons = widgets.HBox([
            self.refresh_button,
            self.new_meeting_button,
            self.view_meetings_button,
            self.clear_data_button
        ])
        
        nl_section = widgets.VBox([
            widgets.HTML("<h3>🤖 AI-Powered Scheduling</h3>"),
            widgets.HBox([self.nl_input, self.submit_nl_button])
        ])
        
        # Main layout
        self.main_container.children = [
            self.title,
            control_buttons,
            widgets.HTML("<hr>"),
            nl_section,
            widgets.HTML("<hr>"),
            self.schedule_output,
            self.output_area,
            self.meeting_form_container
        ]
        
        # Display the interface
        display(self.main_container)
        
        # Initialize with current schedule
        with self.schedule_output:
            clear_output()
            display(HTML("<h3>📊 Quick Stats</h3>"))
            
            # Show quick statistics
            try:
                meetings = self.agent.db_manager.get_meetings()
                today = datetime.now().date()
                
                today_meetings = [m for m in meetings if m.start_time.date() == today]
                upcoming_meetings = [m for m in meetings if m.start_time.date() > today]
                
                stats_html = f"""
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;">
                    <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; text-align: center;">
                        <h4 style="margin: 0; color: #1976d2;">📅 Total Meetings</h4>
                        <p style="font-size: 24px; margin: 5px 0;">{len(meetings)}</p>
                    </div>
                    <div style="background: #f3e5f5; padding: 15px; border-radius: 8px; text-align: center;">
                        <h4 style="margin: 0; color: #7b1fa2;">📅 Today</h4>
                        <p style="font-size: 24px; margin: 5px 0;">{len(today_meetings)}</p>
                    </div>
                    <div style="background: #e8f5e8; padding: 15px; border-radius: 8px; text-align: center;">
                        <h4 style="margin: 0; color: #388e3c;">📅 Upcoming</h4>
                        <p style="font-size: 24px; margin: 5px 0;">{len(upcoming_meetings)}</p>
                    </div>
                </div>
                """
                
                display(HTML(stats_html))
                
            except Exception as e:
                display(HTML(f"<p>Could not load statistics: {str(e)}</p>"))

# Convenience function for easy initialization
def create_calendar_ui(db_path="meeting_scheduler.db", gemini_api_key=None):
    """Create and display the calendar UI"""
    from meeting_scheduler import CalendarAgent
    
    agent = CalendarAgent(db_path, gemini_api_key)
    ui = CalendarUI(agent)
    ui.show_dashboard()
    
    return ui, agent

# Example usage functions
def demo_ai_features():
    """Demonstrate AI-powered features"""
    demo_html = """
    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h2>🤖 Demo: AI-Powered Features</h2>
        
        <h3>Try these natural language commands:</h3>
        <ul>
            <li><strong>Simple Scheduling:</strong> "Schedule a meeting with John tomorrow at 3 PM"</li>
            <li><strong>Duration-based:</strong> "Book a 30-minute slot with Sarah next week"</li>
            <li><strong>Recurring:</strong> "Set up weekly standup every Monday at 9 AM"</li>
            <li><strong>Conflict Resolution:</strong> "Schedule meeting with client at 2 PM Tuesday"</li>
            <li><strong>Queries:</strong> "Show all meetings tomorrow" or "What meetings do I have next week?"</li>
        </ul>
        
        <h3>Smart Conflict Resolution:</h3>
        <p>When conflicts are detected, the agent will:</p>
        <ul>
            <li>✅ Identify conflicting meetings</li>
            <li>💡 Suggest alternative time slots</li>
            <li>💌 Generate polite rescheduling messages</li>
            <li>📝 Provide conflict analysis with explanations</li>
        </ul>
        
        <h3>AI Features:</h3>
        <ul>
            <li>🧠 Natural language understanding</li>
            <li>⚡ Smart time parsing</li>
            <li>🎯 Intelligent scheduling patterns</li>
            <li>💬 Polite communication generation</li>
            <li>🔍 Context-aware meeting queries</li>
        </ul>
    </div>
    """
    display(HTML(demo_html))

def quick_commands():
    """Show quick command examples"""
    commands_html = """
    <h3>⚡ Quick Commands Reference</h3>
    <div style="background: #fff3cd; padding: 15px; border-radius: 8px;">
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background: #f0f0f0;">
                <th style="padding: 8px; border: 1px solid #ddd;">Command Type</th>
                <th style="padding: 8px; border: 1px solid #ddd;">Example</th>
                <th style="padding: 8px; border: 1px solid #ddd;">Action</th>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">📅 Schedule</td>
                <td style="padding: 8px; border: 1px solid #ddd;">"Meeting with Sarah tomorrow"</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Creates new meeting</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">🔄 Reschedule</td>
                <td style="padding: 8px; border: 1px solid #ddd;">"Move Friday's meeting to Monday"</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Updates existing meeting</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">❌ Cancel</td>
                <td style="padding: 8px; border: 1px solid #ddd;">"Cancel meeting with John"</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Removes meeting</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">🔍 Query</td>
                <td style="padding: 8px; border: 1px solid #ddd;">"What meetings tomorrow?"</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Shows filtered results</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">📋 Recurring</td>
                <td style="padding: 8px; border: 1px solid #ddd;">"Weekly team standup every Monday"</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Sets up recurring series</td>
            </tr>
        </table>
    </div>
    """
    display(HTML(commands_html))

if __name__ == "__main__":
    print("Calendar UI Module - Ready for Jupyter Import")
    print("Import with: from calendar_ui import create_calendar_ui, demo_ai_features")
