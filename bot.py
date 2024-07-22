from telegram import Bot

TELEGRAM_BOT_TOKEN = 'your-token-here'

def test_token():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    print("Bot is working!" if bot.get_me() else "Failed to connect.")

if __name__ == '__main__':
    test_token()
