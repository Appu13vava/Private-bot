# login_telegram.py

from telethon.sync import TelegramClient

api_id = 'your_api_id'
api_hash = 'your_api_hash'
phone_number = 'your_phone_number'

# Create a new TelegramClient instance
client = TelegramClient('session_name', api_id, api_hash)

# Function to perform login
async def perform_login():
    await client.start(phone=phone_number)
    # Check if user is already authorized or not
    if await client.is_user_authorized():
        print("User is already authorized.")
    else:
        # Send code to phone, then ask user to enter it
        await client.send_code_request(phone_number)
        code = input('Enter the code you received: ')
        # Sign in with the code
        await client.sign_in(phone_number, code)
        print("Successfully logged in.")

# Running the login function
with client:
    client.loop.run_until_complete(perform_login())
