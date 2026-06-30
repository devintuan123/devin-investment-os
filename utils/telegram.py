import os

import requests
from dotenv import load_dotenv


load_dotenv()


def send_telegram_message(message: str) -> bool:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Warning: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is missing.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        response = requests.post(url, json={"chat_id": chat_id, "text": message}, timeout=15)
    except requests.RequestException as exc:
        print(f"Warning: Telegram request failed: {exc}")
        return False

    if not response.ok:
        print(f"Warning: Telegram API returned {response.status_code}: {response.text}")
        return False

    return True
