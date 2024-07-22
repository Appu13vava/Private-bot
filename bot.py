from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.update import Update

# Replace with your actual bot token
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

def start(update: Update, context: CallbackContext):
    """Send a greeting message when the /start command is issued."""
    update.message.reply_text('Hi Ranga')

def main():
    """Start the bot and set up command handlers."""
    # Initialize the Updater and Bot with the token
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    
    # Ensure the bot is properly initialized
    bot = updater.bot

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    # Register the /start command handler
    dp.add_handler(CommandHandler('start', start))
    
    # Start the Bot
    updater.start_polling()
    print("Bot is polling...")
    
    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
