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
CHANNEL_ID = os.getenv('CHANNEL_ID')

def send_message(text):
    try:
        bot.send_message(chat_id=CHANNEL_ID, text=text)
        print("Message sent successfully.")
    except Exception as e:
        print(f"Failed to send message: {e}")

# Example usage
if __name__ == "__main__":
    send_message("Hello, this is a test message from the bot!")
