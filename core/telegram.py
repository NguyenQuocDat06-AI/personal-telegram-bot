import requests
import logging
from core.config import config

logger = logging.getLogger(__name__)

def send_telegram_msg(message: str, chat_id: str = None) -> bool:
    """
    init function to send telegram message
    send chat_id or config.CHAT_ID
    """
    target_chat_id = chat_id or config.CHAT_ID
    bot_token = config.TELEGRAM_BOT_TOKEN
    
    if not target_chat_id or not bot_token:
        logger.error("ERROR: TELEGRAM_BOT_TOKEN or CHAT_ID is not configured")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": target_chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"ERROR: Send message {e}")
        return False
