"""
Run this script first to verify your Telegram bot is working correctly.
Usage: python test_telegram.py
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

print(f"Token: {token[:20]}...{token[-5:] if token else 'NOT FOUND'}")
print(f"Chat ID: {chat_id if chat_id else 'NOT FOUND'}")

if not token or not chat_id:
    print("\n❌ Missing credentials! Check your .env file.")
    exit(1)

url = f"https://api.telegram.org/bot{token}/sendMessage"
payload = {
    "chat_id": chat_id,
    "text": "✅ <b>Test Message!</b>\nYour Internship Bot is correctly configured.",
    "parse_mode": "HTML"
}

print("\nSending test message to Telegram...")
response = requests.post(url, json=payload, timeout=10)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")

if response.status_code == 200:
    print("\n✅ SUCCESS! Check your Telegram — you should see the test message.")
else:
    print("\n❌ FAILED! See the response above for the exact error.")
    print("\nCommon fixes:")
    print("  - 'chat not found': Make sure you sent /start to your bot in Telegram first.")
    print("  - 'bot was blocked': Unblock the bot in Telegram.")
    print("  - 'unauthorized': Your bot token is wrong. Check .env file.")
