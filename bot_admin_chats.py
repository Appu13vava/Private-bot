import asyncio
from telegram import Bot
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram import Update

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = 'YOUR_BOT_TOKEN'

async def get_admin_chats():
    # Create an instance of the Bot
    bot = Bot(token=BOT_TOKEN)

    # Fetch updates
    updates = await bot.get_updates()
    admin_chats = []

    for update in updates:
        if update.message:
            chat = update.message.chat
            if chat.id in admin_chats:
                continue
            chat_member = await bot.get_chat_administrators(chat.id)
            if any(member.user.id == bot.id for member in chat_member):
                admin_chats.append(chat.id)
    
    return admin_chats

async def main():
    admin_chats = await get_admin_chats()
    print(f"Admin chats: {admin_chats}")

# Run the main function using asyncio
if __name__ == "__main__":
    asyncio.run(main())
