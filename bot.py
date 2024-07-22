from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Replace 'your-token-here' with your actual bot token
TELEGRAM_BOT_TOKEN = 'your-token-here'

# Define the command handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hi')

def main():
    # Create the Application and pass the bot token
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Register the /start command handler
    application.add_handler(CommandHandler('start', start))
    
    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
