#!/usr/bin/env python3
"""
Telegram Time Bot
A simple bot that responds to all messages with the server's local time.
"""

import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "Hello! I'm a time bot. Send me any message and I'll respond with the current server time."
    )


async def get_current_time() -> str:
    """Get formatted current server time."""
    now = datetime.now()
    return now.strftime("%I:%M %p, %B %d, %Y")


async def echo_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the current server time for any text message."""
    current_time = await get_current_time()
    await update.message.reply_text(f"Current server time: {current_time}")


def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_time))

    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
