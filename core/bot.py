from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.config import config

# Bot instance với HTML parse mode mặc định
bot = Bot(
    token=config.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Dispatcher quản lý routing các handler
dp = Dispatcher()
