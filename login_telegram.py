# from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler

# Replace 'your_bot_token' with the token provided by BotFather
bot_token = ''
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your bot.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
updater.idle()
