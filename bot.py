#!/usr/bin/env python3
"""
Telegram Bot
A bot that responds with random numbers and can check Moscow weather.
"""

import os
import logging
import random
import httpx
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
        "Hello! I can do the following:\n"
        "• Send any message → Get a random 10-digit number\n"
        "• /weather → Get current weather in Moscow"
    )


async def generate_random_digits() -> str:
    """Generate a random number as a string with exactly 10 digits."""
    digits = ''.join(random.choices('0123456789', k=10))
    return digits


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
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_random))

    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
