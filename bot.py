from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging

# Replace with your actual bot token
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# This will store unique user IDs
user_ids = set()

def start(update: Update, context: CallbackContext):
    """Send a greeting message when the /start command is issued and track the user."""
    user_id = update.message.from_user.id
    user_ids.add(user_id)
    update.message.reply_text('Hi!')

def count_users(update: Update, context: CallbackContext):
    """Respond with the count of unique users."""
    user_count = len(user_ids)
    update.message.reply_text(f'Total unique users: {user_count}')

def main():
    """Start the bot and set up command handlers."""
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Register command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('count_users', count_users))
    
    # Start the Bot
    updater.start_polling()
    logger.info("Bot is polling...")
    
    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
