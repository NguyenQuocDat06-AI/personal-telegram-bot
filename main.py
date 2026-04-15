import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from routers.github import router as github_router
from core.telegram import send_telegram_msg

# Xử lý các tác vụ thực hiện khi Khởi động và Tắt ứng dụng
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Khi khởi động ---
    send_telegram_msg("🟢 API Server (FastAPI) cho Bot đã khởi động!")
    yield
    # --- Khi tắt ứng dụng ---
    send_telegram_msg("🔴 API Server cho Bot đã dừng!")

app = FastAPI(
    title="Personal Telegram Bot API",
    description="Bot API quản lý thông báo, webhook và các tác vụ cá nhân",
    lifespan=lifespan
)

# Thêm router cho github webhook
app.include_router(github_router)

@app.get("/")
async def root():
    return {"message": "Telegram Bot API đang hoạt động!"}

if __name__ == "__main__":
    # Để API có thể được gọi từ bên ngoài thông qua IP public (như 13.229.155.181) -> host="0.0.0.0"
    # Lắng nghe ở port 8001 theo yêu cầu của bạn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
