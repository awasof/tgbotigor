# Telegram Time Bot

A simple Telegram bot that responds to all messages with the current server time.

## Features

- Responds to any text message with the current server time
- Uses python-telegram-bot v20+ with async/await
- Deployable via CapRover
- Environment variable configuration

## Local Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `env.example`:
   ```bash
   cp env.example .env
   ```
4. Edit `.env` and add your bot token:
   ```
   BOT_TOKEN=your_actual_bot_token_here
   ```
5. Run the bot:
   ```bash
   python bot.py
   ```

## Getting a Bot Token

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the token and add it to your `.env` file

## CapRover Deployment

1. Make sure you have CapRover CLI installed and configured
2. Set the `BOT_TOKEN` environment variable in your CapRover app settings
3. Deploy using:
   ```bash
   caprover deploy
   ```

## Environment Variables

- `BOT_TOKEN` - Your Telegram bot token (required)

## Bot Commands

- `/start` - Welcome message
- Any text message - Returns current server time in format: "Current server time: HH:MM AM/PM, Month DD, YYYY"

## Project Structure

```
.
├── bot.py                 # Main bot application
├── requirements.txt       # Python dependencies
├── env.example           # Example environment variables
├── Dockerfile            # Container configuration
├── captain-definition    # CapRover deployment config
├── .gitignore           # Git ignore file
└── README.md            # This file
```
