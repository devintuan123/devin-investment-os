import os

import requests
from dotenv import load_dotenv


load_dotenv()


def send_telegram_message(message: str) -> bool:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Telegram skipped: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is missing.")
        return False

    try:
        response = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": message},
            timeout=15,
        )
    except requests.RequestException as exc:
        print(f"Telegram skipped: {exc}")
        return False

    if not response.ok:
        print(f"Telegram skipped: API returned {response.status_code}.")
        return False
    return True
