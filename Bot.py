from telegram import Update, Chat
from telegram.ext import Updater, CommandHandler, CallbackContext, ChatMemberHandler
import json

TOKEN = '7307746406:AAEeU_xh_HLDhk8y9ewmNduSPwtjXuA-xGE'
API_ID = 15917107
API_HASH = 'fea3f7efd54a3e37e9c71617e1a9639e'
CHANNELS_FILE = 'channels.json'
USERS_FILE = 'users.json'
SESSIONS_FILE = 'sessions.json'
AUTHORIZED_USERS_FILE = 'authorized_users.json'

# Function to load data from a JSON file
def load_data(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Function to save data to a JSON file
from telegram import Update, Chat
from telegram.ext import Updater, CommandHandler, CallbackContext, ChatMemberHandler
import json

TOKEN = '7307746406:AAEeU_xh_HLDhk8y9ewmNduSPwtjXuA-xGE'
API_ID = 15917107
API_HASH = 'fea3f7efd54a3e37e9c71617e1a9639e'
CHANNELS_FILE = 'channels.json'
USERS_FILE = 'users.json'
SESSIONS_FILE = 'sessions.json'
AUTHORIZED_USERS_FILE = 'authorized_users.json'

# Function to load data from a JSON file
def load_data(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Function to save data to a JSON file
def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)

# Functions to handle channels and users
def load_channels():
    return load_data(CHANNELS_FILE)

def save_channels(channels):
    save_data(CHANNELS_FILE, channels)

def load_users():
    return load_data(USERS_FILE)

def save_users(users):
    save_data(USERS_FILE, users)

# Functions to load and save sessions and authorized users
def load_sessions():
    return load_data(SESSIONS_FILE)

def save_sessions(sessions):
    save_data(SESSIONS_FILE, sessions)

def load_authorized_users():
    return load_data(AUTHORIZED_USERS_FILE)

def save_authorized_users(users):
    save_data(AUTHORIZED_USERS_FILE, users)

# Command handlers
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    users = load_users()
    if user.id not in users:
        users[user.id] = {'username': user.username, 'sessions': {}}
        save_users(users)
    update.message.reply_text('Hello! I am your bot.')

def list_channels(update: Update, context: CallbackContext) -> None:
    channels = load_channels()
    if channels:
        update.message.reply_text('\n'.join([f"{c['title']} ({c['id']})" for c in channels.values()]))
    else:
        update.message.reply_text('No channels found.')

def adchannels(update: Update, context: CallbackContext) -> None:
    if check_admin(update):
        channels = load_channels()
        if channels:
            update.message.reply_text('\n'.join([f"{c['title']} ({c['id']})" for c in channels.values()]))
        else:
            update.message.reply_text('No admin channels found.')
    else:
        update.message.reply_text('You are not authorized to use this command.')

def chat_member_update(update: Update, context: CallbackContext) -> None:
    new_chat_member = update.chat_member.new_chat_member
    if new_chat_member and new_chat_member.status == 'administrator':
        chat = update.chat_member.chat
        channels = load_channels()
        if chat.id not in channels:
            channels[chat.id] = {'id': chat.id, 'title': chat.title}
            save_channels(channels)

def authenticate(update: Update, context: CallbackContext) -> None:
    if context.args and context.args[0] == TOKEN:
        authorized_users = load_authorized_users()
        user_id = update.message.from_user.id
        authorized_users[user_id] = True
        save_authorized_users(authorized_users)
        update.message.reply_text('You have been authenticated as an admin.')
    else:
        update.message.reply_text('Authentication failed.')

def check_admin(update: Update) -> bool:
    user_id = update.message.from_user.id
    authorized_users = load_authorized_users()
    return authorized_users.get(user_id, False)

def broadcast(update: Update, context: CallbackContext) -> None:
    if check_admin(update):
        message = ' '.join(context.args)
        users = load_users()
        for user_id in users:
            context.bot.send_message(chat_id=user_id, text=message)
        update.message.reply_text('Broadcast message sent.')
    else:
        update.message.reply_text('You are not authorized to use this command.')

def post_to_channels(update: Update, context: CallbackContext) -> None:
    if check_admin(update):
        message = ' '.join(context.args)
        channels = load_channels()
        for channel in channels.values():
            context.bot.send_message(chat_id=channel['id'], text=message)
        update.message.reply_text('Message posted to all admin channels.')
    else:
        update.message.reply_text('You are not authorized to use this command.')

# Session management
def create_session(update: Update, context: CallbackContext) -> None:
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
                update.message.reply_text(f"Session '{session_name}' created.")
            else:
                update.message.reply_text(f"Session '{session_name}' already exists.")
        else:
            update.message.reply_text("Please provide a name for the session.")
    else:
        update.message.reply_text("User not recognized.")

def list_sessions(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    users = load_users()
    if user_id in users:
        sessions = users[user_id].get('sessions', {})
        if sessions:
            update.message.reply_text('\n'.join(sessions.keys()))
        else:
            update.message.reply_text('No sessions found.')
    else:
        update.message.reply_text("User not recognized.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("list_channels", list_channels))
    dispatcher.add_handler(CommandHandler("authenticate", authenticate, pass_args=True))
    dispatcher.add_handler(CommandHandler("broadcast", broadcast, pass_args=True))
    dispatcher.add_handler(CommandHandler("post_to_channels", post_to_channels, pass_args=True))
    dispatcher.add_handler(CommandHandler("create_session", create_session, pass_args=True))
    dispatcher.add_handler(CommandHandler("list_sessions", list_sessions))
    dispatcher.add_handler(CommandHandler("adchannels", adchannels))
    dispatcher.add_handler(ChatMemberHandler(chat_member_update, ChatMemberHandler.CHAT_MEMBER))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
