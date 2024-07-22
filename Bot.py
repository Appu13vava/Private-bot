from telethon.sync import TelegramClient, events
from telethon.tl.functions.channels import SendMessageRequest

# Telegram API credentials (replace with your actual values)
api_id = '15917107'
api_hash = 'fea3f7efd54a3e37e9c71617e1a9639e''
bot_token = ''

# Session name
session_name = 'my_telegram_session'

# Initialize the client and create the session
client = TelegramClient(session_name, api_id, api_hash)

async def list_admin_chats():
    await client.start()

    try:
        dialogs = await client.get_dialogs(limit=None)

        print("List of admin chats:")
        for dialog in dialogs:
            entity = dialog.entity
            # Check if the entity is a channel and the bot is an admin
            if entity.creator or entity.admin_rights:
                print(f"{entity.title} - {entity.id}")

    except Exception as e:
        print(f"Error: {str(e)}")

    await client.disconnect()

async def post_message_to_channel(channel_id, message):
    await client.start()

    try:
        # Send message to the channel
        await client(SendMessageRequest(
            peer=channel_id,
            message=message
        ))

        print(f"Message posted to channel {channel_id}")

    except Exception as e:
        print(f"Error posting message: {str(e)}")

    await client.disconnect()

async def main():
    # Replace with your admin channel ID and message content
    channel_id = 'your_channel_id'
    message = 'Hello from my bot! This is a test message.'

    await list_admin_chats()
    await post_message_to_channel(channel_id, message)

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
