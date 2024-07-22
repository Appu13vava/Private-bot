from telegram import Bot
import os

# Retrieve the bot token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Initialize the bot with the token
bot = Bot(token=BOT_TOKEN)

# Function to get admin chats
def get_admin_chats():
    updates = bot.get_updates()
    admin_chats = []

    for update in updates:
        chat = update.message.chat
        if update.message.chat.id in admin_chats:
            continue
        chat_member = bot.get_chat_administrators(chat.id)
        if any(member.user.id == bot.id for member in chat_member):
            admin_chats.append(chat.id)
    
    return admin_chats

if __name__ == "__main__":
    admin_chats = get_admin_chats()
    print(f"Admin chats: {admin_chats}")
