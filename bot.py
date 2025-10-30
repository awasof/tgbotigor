#!/usr/bin/env python3
"""
Telegram Bot
A bot with OpenAI chat, weather checking, and random number generation.
"""

import os
import logging
import random
import httpx
import sys
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

# Load environment variables
load_dotenv()

# Configure logging - force output to stdout
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout,
    force=True
)
logger = logging.getLogger(__name__)

logger.info("Bot starting up...")

# Get tokens from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

logger.info(f"BOT_TOKEN present: {bool(BOT_TOKEN)}")
logger.info(f"OPENAI_API_KEY present: {bool(OPENAI_API_KEY)}")

if not BOT_TOKEN:
    logger.error("BOT_TOKEN environment variable is missing!")
    raise ValueError("BOT_TOKEN environment variable is required")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY environment variable is missing!")
    raise ValueError("OPENAI_API_KEY environment variable is required")

# Initialize OpenAI client
try:
    openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    logger.info("OpenAI client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    raise


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "Hello! I'm an AI assistant powered by OpenAI. I can:\n"
        "• Chat with you about anything (just send a message)\n"
        "• /weather → Get current weather in Moscow\n"
        "• /random → Generate a random 10-digit number"
    )


async def random_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate and send a random 10-digit number."""
    digits = ''.join(random.choices('0123456789', k=10))
    await update.message.reply_text(f"🎲 Random number: {digits}")


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get and display current weather in Moscow."""
    try:
        async with httpx.AsyncClient() as client:
            # Using wttr.in API - no API key required
            response = await client.get(
                'https://wttr.in/Moscow?format=j1',
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            
            # Extract weather information
            current = data['current_condition'][0]
            temp = current['temp_C']
            feels_like = current['FeelsLikeC']
            humidity = current['humidity']
            description = current['weatherDesc'][0]['value']
            wind_speed = current['windspeedKmph']
            
            weather_text = (
                f"🌤 Weather in Moscow:\n\n"
                f"Temperature: {temp}°C (feels like {feels_like}°C)\n"
                f"Conditions: {description}\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind_speed} km/h"
            )
            
            await update.message.reply_text(weather_text)
            
    except httpx.TimeoutException:
        await update.message.reply_text("⚠️ Weather service timeout. Please try again later.")
    except httpx.HTTPError as e:
        logger.error(f"HTTP error getting weather: {e}")
        await update.message.reply_text("⚠️ Unable to fetch weather data. Please try again later.")
    except Exception as e:
        logger.error(f"Error getting weather: {e}")
        await update.message.reply_text("⚠️ An error occurred while fetching weather data.")


async def chat_with_openai(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular text messages by chatting with OpenAI."""
    user_message = update.message.text
    
    try:
        # Send typing action to show bot is processing
        await update.message.chat.send_action(action="typing")
        
        # Call OpenAI API
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful and friendly assistant in a Telegram bot. Keep responses concise and engaging."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        # Extract and send the response
        ai_response = response.choices[0].message.content
        await update.message.reply_text(ai_response)
        
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        await update.message.reply_text(
            "⚠️ Sorry, I'm having trouble processing your message right now. Please try again later."
        )


def main() -> None:
    """Start the bot."""
    try:
        logger.info("Creating Application...")
        # Create the Application
        application = Application.builder().token(BOT_TOKEN).build()
        logger.info("Application created successfully")

        # Register handlers
        logger.info("Registering handlers...")
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("weather", weather))
        application.add_handler(CommandHandler("random", random_number))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_openai))
        logger.info("Handlers registered successfully")

        # Start the bot
        logger.info("Starting bot polling...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"Fatal error in main(): {e}", exc_info=True)
        raise


if __name__ == '__main__':
    try:
        logger.info("=== Bot Script Starting ===")
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)
        sys.exit(1)
