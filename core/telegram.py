import requests
import logging
from core.config import config

logger = logging.getLogger(__name__)

def send_telegram_msg(message: str, chat_id: str = None) -> bool:
    """
    Gửi tin nhắn Telegram đến chat_id được chỉ định.
    Nếu không truyền chat_id, sẽ dùng CHAT_ID mặc định trong config.
    """
    target_chat_id = chat_id or config.CHAT_ID
    bot_token = config.TELEGRAM_BOT_TOKEN
    
    if not target_chat_id or not bot_token:
        logger.error("Chưa cấu hình TELEGRAM_BOT_TOKEN hoặc CHAT_ID")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": target_chat_id,
        "text": message,
        "parse_mode": "HTML" # Cho phép hiển thị định dạng in đậm, in nghiêng bằng HTML
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Lỗi khi gửi tin nhắn Telegram: {e}")
        return False
