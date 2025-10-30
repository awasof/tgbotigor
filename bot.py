#!/usr/bin/env python3
"""
Telegram Time Bot
A simple bot that responds to all messages with the server's local time.
"""

import os
import logging
import random
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
        "Hello! Send me any message and I'll reply with a random 10-digit number."
    )


async def generate_random_digits() -> str:
    """Generate a random number as a string with exactly 10 digits."""
    digits = ''.join(random.choices('0123456789', k=10))
    return digits


async def echo_random(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with a random 10-digit number string for any text message."""
    random_number = await generate_random_digits()
    await update.message.reply_text(random_number)


def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_random))

    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
