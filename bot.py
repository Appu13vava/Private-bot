import telebot
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Get bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    logging.error("BOT_TOKEN environment variable not set.")
    raise ValueError("BOT_TOKEN environment variable not set.")

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# Replace with your channel ID or username
CHANNEL_ID = os.getenv('CHANNEL_ID')
if not CHANNEL_ID:
    logging.error("CHANNEL_ID environment variable not set.")
    raise ValueError("CHANNEL_ID environment variable not set.")

def send_message(text):
    try:
        bot.send_message(chat_id=CHANNEL_ID, text=text)
        logging.info("Message sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send message: {e}")

# Example usage
if __name__ == "__main__":
    send_message("Hello, this is a test message from the bot!")
