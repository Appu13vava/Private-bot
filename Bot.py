from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, ChatMemberHandler
import json

TOKEN = '7307746406:AAEeU_xh_HLDhk8y9ewmNduSPwtjXuA-xGE'
CHANNELS_FILE = 'channels.json'
USERS_FILE = 'users.json'
SESSIONS_FILE = 'sessions.json'
AUTHORIZED_USERS_FILE = 'authorized_users.json'

def load_data(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_channels():
    return load_data(CHANNELS_FILE)

def save_channels(channels):
    save_data(CHANNELS_FILE, channels)

def load_users():
    return load_data(USERS_FILE)

def save_users(users):
    save_data(USERS_FILE, users)

def load_sessions():
    return load_data(SESSIONS_FILE)

def save_sessions(sessions):
    save_data(SESSIONS_FILE, sessions)

def load_authorized_users():
    return load_data(AUTHORIZED_USERS_FILE)

def save_authorized_users(users):
    save_data(AUTHORIZED_USERS_FILE, users)

async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    users = load_users()
    if user.id not in users:
        users[user.id] = {'username': user.username, 'sessions': {}}
        save_users(users)
    await update.message.reply_text('Hello! I am your bot.')

async def list_channels(update: Update, context: CallbackContext) -> None:
    channels = load_channels()
    if channels:
        await update.message.reply_text('\n'.join([f"{c['title']} ({c['id']})" for c in channels.values()]))
    else:
        await update.message.reply_text('No channels found.')

async def adchannels(update: Update, context: CallbackContext) -> None:
    if check_admin(update):
        channels = load_channels()
        if channels:
            await update.message.reply_text('\n'.join([f"{c['title']} ({c['id']})" for c in channels.values()]))
        else:
            await update.message.reply_text('No admin channels found.')
    else:
        await update.message.reply_text('You are not authorized to use this command.')

async def chat_member_update(update: Update, context: CallbackContext) -> None:
    new_chat_member = update.chat_member.new_chat_member
    if new_chat_member and new_chat_member.status == 'administrator':
        chat = update.chat_member.chat
        channels = load_channels()
        if chat.id not in channels:
            channels[chat.id] = {'id': chat.id, 'title': chat.title}
            save_channels(channels)

async def authenticate(update: Update, context: CallbackContext) -> None:
    if context.args and context.args[0] == TOKEN:
        authorized_users = load_authorized_users()
        user_id = update.message.from_user.id
        authorized_users[user_id] = True
        save_authorized_users(authorized_users)
        await update.message.reply_text('You have been authenticated as an admin.')
    else:
        await update.message.reply_text('Authentication failed.')

def check_admin(update: Update) -> bool:
    user_id = update.message.from_user.id
    authorized_users = load_authorized_users()
    return authorized_users.get(user_id, False)

async def broadcast(update: Update, context: CallbackContext) -> None:
    if check_admin(update):
        message = ' '.join(context.args)
        users = load_users()
        for user_id in users:
            await context.bot.send_message(chat_id=user_id, text=message)
        await update.message.reply_text('Broadcast message sent.')
    else:
        await update.message.reply_text('You are not authorized to use this command.')

async def post_to_channels(update: Update, context: CallbackContext) -> None:
    if check_admin(update):
        message = ' '.join(context.args)
        channels = load_channels()
        for channel in channels.values():
            await context.bot.send_message(chat_id=channel['id'], text=message)
        await update.message.reply_text('Message posted to all admin channels.')
    else:
        await update.message.reply_text('You are not authorized to use this command.')

async def create_session(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    users = load_users()
    if user_id in users:
        session_name = ' '.join(context.args)
        if session_name:
            sessions = users[user_id].get('sessions', {})
            if session_name not in sessions:
                sessions[session_name] = {}
                users[user_id]['sessions'] = sessions
                save_users(users)
                await update.message.reply_text(f"Session '{session_name}' created.")
            else:
                await update.message.reply_text(f"Session '{session_name}' already exists.")
        else:
            await update.message.reply_text("Please provide a name for the session.")
    else:
        await update.message.reply_text("User not recognized.")

async def list_sessions(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    users = load_users()
    if user_id in users:
        sessions = users[user_id].get('sessions', {})
        if sessions:
            await update.message.reply_text('\n'.join(sessions.keys()))
        else:
            await update.message.reply_text('No sessions found.')
    else:
        await update.message.reply_text("User not recognized.")

def main():
    # Create an instance of the Application class
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("list_channels", list_channels))
    application.add_handler(CommandHandler("authenticate", authenticate))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("post_to_channels", post_to_channels))
    application.add_handler(CommandHandler("create_session", create_session))
    application.add_handler(CommandHandler("list_sessions", list_sessions))
    application.add_handler(CommandHandler("adchannels", adchannels))
    application.add_handler(ChatMemberHandler(chat_member_update))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
