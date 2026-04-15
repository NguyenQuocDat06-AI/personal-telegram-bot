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

# Đăng ký tất cả aiogram routers tại đây (chỉ chạy 1 lần khi module được import)
# Tránh gọi dp.include_router() ở ngoài module này để không bị double-attach
from routers.landmark import router as landmark_router  # noqa: E402
dp.include_router(landmark_router)
