import asyncio
import uvicorn
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.bot import bot, dp
from core.commands import setup_commands
from core.telegram import send_telegram_msg
from routers.github import router as github_router

# Cấu hình logging để xem log của cả FastAPI và Aiogram
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Quản lý vòng đời app:
    - Startup: khởi động Telegram bot polling trong asyncio background task
    - Shutdown: huỷ polling task, đóng bot session
    """
    # Xoá webhook cũ (nếu có) trước khi polling
    await bot.delete_webhook(drop_pending_updates=True)

    # Cấu hình danh sách lệnh (menu)
    await setup_commands(bot)
    
    # Chạy polling song song với FastAPI (non-blocking)
    # Tắt handle_signals để FastAPI tự quản lý việc shutdown
    polling_task = asyncio.create_task(dp.start_polling(bot, handle_signals=False))
    send_telegram_msg("🤖 <b>Bot đã khởi động!</b>")

    yield  # FastAPI đang chạy

    # Dừng polling khi shutdown
    polling_task.cancel()
    try:
        await polling_task
    except (asyncio.CancelledError, Exception):
        pass

    await bot.session.close()


app = FastAPI(
    title="Personal Telegram Bot API",
    description="Bot API",
    lifespan=lifespan
)

# FastAPI router cho GitHub Webhook (vẫn giữ nguyên)
app.include_router(github_router)


@app.get("/")
async def root():
    return {"message": "Telegram Bot API start!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=False)
