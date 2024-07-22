import os
import asyncio
from telegram import Bot
from telegram.error import BadRequest, TimedOut, RetryAfter

# Retrieve the bot token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

if BOT_TOKEN is None:
    raise ValueError("No BOT_TOKEN environment variable set. Please set it to the correct value.")

async def get_admin_chats():
    bot = Bot(token=BOT_TOKEN)

    # Ensure bot is properly initialized
    await bot.get_me()

    updates = await bot.get_updates()
    admin_chats = []

    for update in updates:
        if update.message:
            chat = update.message.chat
            try:
                chat_member = await bot.get_chat_administrators(chat.id)
                if any(member.user.id == bot.id for member in chat_member):
                    admin_chats.append(chat.id)
            except BadRequest as e:
                # Handle cases where no administrators exist or private chats
                print(f"Failed to get administrators for chat {chat.id}: {e}")
            except RetryAfter as e:
                # Handle rate limit exceedance
                print(f"Rate limit exceeded. Retrying after {e.retry_after} seconds.")
                await asyncio.sleep(e.retry_after)
            except TimedOut as e:
                # Handle timeout
                print(f"Request timed out: {e}. Retrying...")
                await asyncio.sleep(10)

    return admin_chats

async def main():
    try:
        admin_chats = await get_admin_chats()
        if admin_chats:
            print(f"Admin chats: {admin_chats}")
        else:
            print("No admin chats found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the main function using asyncio
if __name__ == "__main__":
    asyncio.run(main())
