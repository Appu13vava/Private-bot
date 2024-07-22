import os
import asyncio
from telegram import Bot
from telegram.error import BadRequest, TimedOut, RetryAfter

# Retrieve the bot token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

if BOT_TOKEN is None:
    raise ValueError("No BOT_TOKEN environment variable set. Please set it to the correct value.")

# List of known chat IDs to check
KNOWN_CHAT_IDS = [
    # Add your chat IDs here
    -1001895249918, # Example chat ID
]

async def get_chat_members_count():
    bot = Bot(token=BOT_TOKEN)
    chat_member_counts = []

    for chat_id in KNOWN_CHAT_IDS:
        try:
            chat_member = await bot.get_chat_administrators(chat_id)
            if any(member.user.id == bot.id for member in chat_member):
                # Fetch the number of members in the chat
                member_count = await bot.get_chat_members_count(chat_id)
                chat_member_counts.append((chat_id, member_count))
        except BadRequest as e:
            print(f"Failed to get administrators for chat {chat_id}: {e}")
        except RetryAfter as e:
            print(f"Rate limit exceeded. Retrying after {e.retry_after} seconds.")
            await asyncio.sleep(e.retry_after)
        except TimedOut as e:
            print(f"Request timed out: {e}. Retrying...")
            await asyncio.sleep(10)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    return chat_member_counts

async def main():
    try:
        chat_member_counts = await get_chat_members_count()
        if chat_member_counts:
            for chat_id, member_count in chat_member_counts:
                print(f"Chat ID: {chat_id}, Number of Members: {member_count}")
        else:
            print("No admin chats found or no data available.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
