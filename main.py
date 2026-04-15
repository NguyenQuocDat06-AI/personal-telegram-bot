import asyncio
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.bot import bot, dp
from core.telegram import send_telegram_msg
from routers.github import router as github_router
from routers.landmark import router as landmark_router

# Đăng ký aiogram router vào Dispatcher
dp.include_router(landmark_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Quản lý vòng đời app:
    - Startup: khởi động Telegram bot polling trong asyncio background task
    - Shutdown: huỷ polling task, đóng bot session
    """
    # Xoá webhook cũ (nếu có) trước khi polling
    await bot.delete_webhook(drop_pending_updates=True)

    # Chạy polling song song với FastAPI (non-blocking)
    polling_task = asyncio.create_task(dp.start_polling(bot))
    send_telegram_msg("🤖 <b>Bot đã khởi động!</b>")

    yield  # FastAPI đang chạy

    # Dừng polling khi shutdown
    polling_task.cancel()
    try:
        await polling_task
    except asyncio.CancelledError:
        pass

    await bot.session.close()
    send_telegram_msg("🔴 <b>Bot đã dừng.</b>")


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
