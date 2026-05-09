from aiogram import Bot
from aiogram.types import BotCommand

async def setup_commands(bot: Bot):
    """
    Cấu hình danh sách lệnh (menu) cho bot.
    Các lệnh này sẽ hiển thị khi người dùng gõ '/' hoặc nhấn vào nút Menu.
    """
    commands = [
        BotCommand(command="start", description="Bắt đầu và xem danh sách lệnh"),
        BotCommand(command="help", description="Nhận hỗ trợ"),
        BotCommand(command="github", description="Thông tin GitHub integration"),
    ]
    await bot.set_my_commands(commands)
