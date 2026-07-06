import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///reminders.db')
    
    # Time settings
    TIMEZONE = 'UTC'
    DEFAULT_REMINDER_HOUR = 9  # 9 AM
    DEFAULT_REMINDER_MINUTE = 0
    
    # Messages
    WELCOME_MESSAGE = """
Welcome to Daily Reminder Bot! 🎯

I'll help you stay on track with daily reminders.

Commands:
/start - Show this message
/set_time - Set daily reminder time (HH:MM in UTC)
/set_reminder - Set your daily reminder message
/view_reminder - View your current reminder
/delete_reminder - Delete your reminder
/help - Show help message
"""
    
    HELP_MESSAGE = """
📌 How to use this bot:

1. First, set your daily reminder time:
   /set_time 09:00 (UTC time)

2. Set your reminder message:
   /set_reminder Your reminder text here

3. The bot will send your reminder every day at the set time

4. You can view or delete your reminder anytime

⚠️ Time is in UTC format (24-hour)
   Example: 09:00 for 9 AM, 14:30 for 2:30 PM
"""
