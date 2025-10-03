"""
Configuration module for Custom AI Agent Meeting Scheduler
"""

import os
import sys
from typing import Optional

class Config:
    """Configuration management for the AI agent system"""
    
    def __init__(self):
        self.load_env_file()
        
    def load_env_file(self):
        """Load configuration from .env file if it exists"""
        env_file_paths = [
            'config.env',
            '.env',
            os.path.expanduser('~/.ai_agent_config')
        ]
        
        for env_path in env_file_paths:
            if os.path.exists(env_path):
                try:
                    self._load_from_file(env_path)
                    print(f"Configuration loaded from: {env_path}")
                    return
                except Exception as e:
                    print(f"Warning: Could not load config from {env_path}: {e}")
        
        # Fallback to environment variables
        print("Using environment variables for configuration")
    
    def _load_from_file(self, filepath: str):
        """Load configuration from file"""
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
    
    def get_api_key(self) -> Optional[str]:
        """Get Gemini API key from configuration"""
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key and api_key != 'your_gemini_api_key_here':
            return api_key
        return None
    
    def get_database_path(self) -> str:
        """Get database path"""
        return os.getenv('DATABASE_PATH', 'meeting_scheduler.db')
    
    def get_user_id(self) -> str:
        """Get default user ID"""
        return os.getenv('DEFAULT_USER_ID', 'default_user')
    
    def get_agent_mode(self) -> str:
        """Get default agent mode"""
        return os.getenv('DEFAULT_AGENT_MODE', 'BALANCED')
    
    def get_log_level(self) -> str:
        """Get logging level"""
        return os.getenv('LOG_LEVEL', 'INFO')
    
    def show_config(self):
        """Display current configuration"""
        print("Current Configuration:")
        print("-" * 30)
        print(f"Gemini API Key: {'Set' if self.get_api_key() else 'Not set (optional)'}")
        print(f"Database Path: {self.get_database_path()}")
        print(f"Default User ID: {self.get_user_id()}")
        print(f"Default Agent Mode: {self.get_agent_mode()}")
        print(f"Log Level: {self.get_log_level()}")
        
        if not self.get_api_key():
            print("\nTo enable enhanced AI features:")
            print("1. Get API key from: https://makersuite.google.com/app/apikey")
            print("2. Copy config.env.example to config.env")
            print("3. Set GOOGLE_API_KEY=your_actual_api_key")

# Global config instance
config = Config()
