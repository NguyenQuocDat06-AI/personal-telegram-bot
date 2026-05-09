from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    help_text = (
        "👋 <b>Chào mừng bạn đến với Bot cá nhân!</b>\n\n"
        "Dưới đây là danh sách các lệnh bạn có thể sử dụng:\n"
        "/start - Bắt đầu và xem danh sách lệnh\n"
        "/help - Nhận hỗ trợ\n"
        "/github - Thông tin về GitHub integration\n"
        "📸 <b>Gửi ảnh:</b> Gửi một tấm ảnh địa danh để tôi nhận diện.\n"
        "💬 <b>Chat:</b> Gửi bất kỳ tin nhắn nào khác để trò chuyện cùng tôi."
    )
    await message.reply(help_text)

@router.message()
async def echo_handler(message: types.Message):
    try:
        # Echo back the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # Fallback for messages that can't be copied
        await message.answer("Tôi đã nhận được tin nhắn của bạn!")
