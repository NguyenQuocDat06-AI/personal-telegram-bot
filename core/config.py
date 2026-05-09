import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # --- Telegram Bot ---
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    # --- Group id ---
    CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID")
    
    URL_SUPABASE: str = os.getenv("SUPABASE_URL")
    TOKEN_SUPABASE: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

config = Config()
