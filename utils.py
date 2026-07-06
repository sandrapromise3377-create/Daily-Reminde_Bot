from datetime import datetime
import pytz

def get_utc_time():
    """Get current UTC time"""
    return datetime.now(pytz.UTC)

def validate_time_format(time_str):
    """Validate time string in HH:MM format"""
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def format_time_for_display(time_str):
    """Format time for display"""
    try:
        time_obj = datetime.strptime(time_str, '%H:%M')
        return time_obj.strftime('%I:%M %p')
    except:
        return time_str
