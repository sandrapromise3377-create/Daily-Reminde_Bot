from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
import re
from database import Database
from config import Config

db = Database()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    db.add_user(
        user_id=user.id,
        chat_id=update.effective_chat.id,
        username=user.username
    )
    await update.message.reply_text(Config.WELCOME_MESSAGE)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(Config.HELP_MESSAGE)

async def set_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /set_time command"""
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text(
            "Please provide a time in HH:MM format (UTC).\n"
            "Example: /set_time 09:00"
        )
        return
    
    time_str = context.args[0]
    
    # Validate time format
    if not re.match(r'^([0-1][0-9]|2[0-3]):[0-5][0-9]$', time_str):
        await update.message.reply_text(
            "Invalid time format. Please use HH:MM in 24-hour format (UTC).\n"
            "Example: 09:00 or 14:30"
        )
        return
    
    # Update or create user with time
    user = db.get_user(user_id)
    if user:
        if user.reminder_text:
            db.update_reminder(user_id, time_str, user.reminder_text)
        else:
            db.update_reminder(user_id, time_str, None)
        await update.message.reply_text(
            f"✅ Daily reminder time set to {time_str} UTC!\n"
            "Now set your reminder message using:\n"
            "/set_reminder Your message here"
        )
    else:
        await update.message.reply_text("Please use /start first to register.")

async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /set_reminder command"""
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text(
            "Please provide your reminder message.\n"
            "Example: /set_reminder Take medicine"
        )
        return
    
    reminder_text = ' '.join(context.args)
    user = db.get_user(user_id)
    
    if not user:
        await update.message.reply_text("Please use /start first to register.")
        return
    
    if not user.reminder_time:
        await update.message.reply_text(
            "Please set a time first using:\n"
            "/set_time HH:MM"
        )
        return
    
    db.update_reminder(user_id, user.reminder_time, reminder_text)
    await update.message.reply_text(
        f"✅ Reminder set!\n"
        f"⏰ Time: {user.reminder_time} UTC\n"
        f"📝 Message: {reminder_text}\n\n"
        "You'll receive this reminder daily at the specified time."
    )

async def view_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /view_reminder command"""
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    
    if not user or not user.reminder_time or not user.reminder_text:
        await update.message.reply_text(
            "You don't have any reminder set.\n"
            "Use /set_time and /set_reminder to set up your daily reminder."
        )
        return
    
    await update.message.reply_text(
        f"📋 Your current reminder:\n\n"
        f"⏰ Time: {user.reminder_time} UTC\n"
        f"📝 Message: {user.reminder_text}"
    )

async def delete_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /delete_reminder command"""
    user_id = update.effective_user.id
    
    if db.delete_reminder(user_id):
        await update.message.reply_text(
            "✅ Your reminder has been deleted successfully."
        )
    else:
        await update.message.reply_text(
            "You don't have any active reminder to delete."
        )

async def send_daily_reminders(context: ContextTypes.DEFAULT_TYPE):
    """Send daily reminders to all users"""
    users = db.get_all_active_users()
    current_time = datetime.utcnow().strftime("%H:%M")
    
    for user in users:
        if user.reminder_time == current_time:
            try:
                await context.bot.send_message(
                    chat_id=user.chat_id,
                    text=f"⏰ Daily Reminder!\n\n{user.reminder_text}"
                )
            except Exception as e:
                print(f"Failed to send reminder to {user.user_id}: {e}")
