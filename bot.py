import telebot
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# Replace with your channel ID or username
CHANNEL_ID = '@YourChannelUsername'  # or '-1001234567890' for private channels

def send_message(text):
    bot.send_message(chat_id=CHANNEL_ID, text=text)

# Example usage
if __name__ == "__main__":
    send_message("Hello, this is a test message from the bot!")
