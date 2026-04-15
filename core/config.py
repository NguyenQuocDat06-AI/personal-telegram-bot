import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # --- Telegram Bot ---
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    # --- Group id ---
    CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID")

config = Config()
