import io
import logging

import httpx
from aiogram import Router, F, Bot
from aiogram.types import Message

logger = logging.getLogger(__name__)

router = Router()

PREDICT_API_URL = "http://[IP_ADDRESS]/predict"


async def call_predict_api(image_buffer: io.BytesIO, filename: str = "image.jpg") -> dict:
    """
    Gửi ảnh (BytesIO trên RAM) lên prediction API.
    Không ghi ra disk, stream trực tiếp từ bộ nhớ.
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        files = {"file": (filename, image_buffer, "image/jpeg")}
        resp = await client.post(PREDICT_API_URL, files=files)
        resp.raise_for_status()
        return resp.json()


def format_prediction_message(result: dict) -> str:
    """Format kết quả predict thành tin nhắn HTML đẹp cho Telegram."""
    if not result.get("success", False):
        return "❌ <b>Nhận diện thất bại</b>\nAPI không thể xử lý ảnh này."

    label = result.get("label", "N/A")
    location_name = result.get("location_name", "Không xác định")
    inliers = result.get("inliers", 0)
    processing_time = result.get("processing_time", 0)

    return (
        f"🏛️ <b>Kết quả nhận diện địa danh</b>\n\n"
        f"📍 <b>Địa điểm:</b> {location_name}\n"
        f"🔖 <b>Mã ID:</b> <code>{label}</code>\n"
        f"🎯 <b>Điểm khớp (Inliers):</b> {inliers}\n"
        f"⏱️ <b>Thời gian xử lý:</b> {processing_time:.3f}s"
    )


@router.message(F.photo)
async def handle_photo(message: Message, bot: Bot):
    """
    Handler xử lý khi người dùng gửi ảnh lên bot.
    Luồng:
      1. Reply thông báo đang xử lý
      2. Download ảnh thẳng vào BytesIO (RAM only, không ghi disk)
      3. POST ảnh lên prediction API
      4. Reply kết quả nhận diện
    """
    try:
        await message.reply(
            "⏳ <b>Đang nhận diện địa danh...</b>\nVui lòng chờ trong giây lát."
        )

        # Lấy ảnh chất lượng cao nhất (phần tử cuối trong list)
        photo = message.photo[-1]
        logger.info(f"Processing photo file_id={photo.file_id} from chat_id={message.chat.id}")

        # aiogram tự động download vào BytesIO (RAM only) khi không truyền destination
        image_buffer: io.BytesIO = await bot.download(photo)
        logger.info(f"Loaded image into memory: {image_buffer.getbuffer().nbytes} bytes")

        # Gửi thẳng buffer RAM lên prediction API
        result = await call_predict_api(image_buffer)
        logger.info(f"Prediction result: {result}")

        # Reply kết quả về đúng message
        await message.reply(format_prediction_message(result))

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error calling predict API: {e}")
        await message.reply(
            "⚠️ <b>Lỗi kết nối API</b>\n"
            "Không thể kết nối tới máy chủ nhận diện. Vui lòng thử lại sau."
        )

    except Exception as e:
        logger.error(f"Unexpected error handling photo: {e}", exc_info=True)
        await message.reply(
            "❌ <b>Đã xảy ra lỗi</b>\nVui lòng thử lại hoặc liên hệ admin."
        )
