from telegram import Bot
from telegram.ext import Updater, CommandHandler

# Replace 'your-token-here' with your actual bot token
TELEGRAM_BOT_TOKEN = 'your-token-here'

def start(update, context):
    update.message.reply_text('Hello!')

def main():
    # Create a Bot instance
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    
    # Create the Updater and pass the Bot instance
    updater = Updater(bot=bot, use_context=True)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    # Register the /start command handler
    dp.add_handler(CommandHandler('start', start))
    
    # Start the Bot
    updater.start_polling()
    
    # Block until you press Ctrl+C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time.
    updater.idle()

if __name__ == '__main__':
    main()
