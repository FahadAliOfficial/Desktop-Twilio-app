"""
Configuration module for the Twilio Calling Dashboard
Handles application settings and environment variables
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class AppConfig:
    """
    Application configuration class
    """
    
    def __init__(self):
        # Twilio Configuration
        self.TWILIO_ACCOUNT_SID: Optional[str] = os.getenv('TWILIO_ACCOUNT_SID')
        self.TWILIO_AUTH_TOKEN: Optional[str] = os.getenv('TWILIO_AUTH_TOKEN')
        self.TWILIO_PHONE_NUMBER: Optional[str] = os.getenv('TWILIO_PHONE_NUMBER')
        self.TWILIO_TOLL_FREE_NUMBER: Optional[str] = os.getenv('TWILIO_TOLL_FREE_NUMBER')
        
        # Supabase Configuration
        self.SUPABASE_URL: Optional[str] = os.getenv('SUPABASE_URL')
        self.SUPABASE_KEY: Optional[str] = os.getenv('SUPABASE_KEY')
        
        # Application Settings
        self.APP_NAME = "Twilio Calling Dashboard"
        self.APP_VERSION = "1.0.0"
        self.DEFAULT_COUNTRY_CODE = "+1"
        
        # UI Settings
        self.WINDOW_WIDTH = 1200
        self.WINDOW_HEIGHT = 800
        self.POPUP_WIDTH = 350
        self.POPUP_HEIGHT = 500
        
        # Call Settings
        self.MAX_CALL_DURATION = 3600  # 1 hour in seconds
        self.CALL_TIMEOUT = 30  # 30 seconds
        
        # Export Settings
        self.EXPORT_FORMATS = ['xlsx', 'csv']
        self.MAX_EXPORT_RECORDS = 10000
    
    def validate_twilio_config(self) -> bool:
        """
        Validate if Twilio configuration is complete
        
        Returns:
            bool: True if configuration is valid
        """
        return all([
            self.TWILIO_ACCOUNT_SID,
            self.TWILIO_AUTH_TOKEN,
            self.TWILIO_PHONE_NUMBER
        ])
    
    def validate_supabase_config(self) -> bool:
        """
        Validate if Supabase configuration is complete
        
        Returns:
            bool: True if configuration is valid
        """
        return all([
            self.SUPABASE_URL,
            self.SUPABASE_KEY
        ])
    
    def get_caller_id_options(self) -> dict:
        """
        Get available caller ID options
        
        Returns:
            dict: Dictionary of caller ID options
        """
        options = {
            "hidden": "Hide Caller ID",
            "company": f"Company Number ({self.TWILIO_PHONE_NUMBER})"
        }
        
        if self.TWILIO_TOLL_FREE_NUMBER:
            options["toll_free"] = f"Toll Free ({self.TWILIO_TOLL_FREE_NUMBER})"
        
        return options
