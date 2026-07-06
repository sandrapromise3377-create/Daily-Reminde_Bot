import logging
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
from config import Config
from handlers import (
    start_command, help_command, set_time, set_reminder,
    view_reminder, delete_reminder, send_daily_reminders
)
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import pytz

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def setup_scheduler(application):
    """Setup the scheduler for daily reminders"""
    scheduler = BackgroundScheduler(timezone=pytz.UTC)
    
    # Check every minute for reminders
    scheduler.add_job(
        send_daily_reminders,
        trigger=IntervalTrigger(minutes=1),
        args=[application],
        id='daily_reminder_job'
    )
    scheduler.start()
    logger.info("Scheduler started successfully")
    return scheduler

def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(Config.BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("set_time", set_time))
    application.add_handler(CommandHandler("set_reminder", set_reminder))
    application.add_handler(CommandHandler("view_reminder", view_reminder))
    application.add_handler(CommandHandler("delete_reminder", delete_reminder))
    
    # Setup scheduler for daily reminders
    scheduler = setup_scheduler(application)
    
    # Start the bot
    logger.info("Bot started successfully!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
