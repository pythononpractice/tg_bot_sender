import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from src.database.engine import AsyncSessionLocal
from src.handlers import commands, callbacks
from src.handlers.base import start_handler
from config import config
from src.handlers import create_mail_message_router
from src.middleware.datebase import DataBaseSession
from src.states.base import CreateMessage

dp = Dispatcher()
bot = Bot(config.token, parse_mode=ParseMode.MARKDOWN)


def set_handlers():
    dp.message.register(start_handler, CommandStart())
    dp.message.register(commands.create_sender_handler, Command(commands=['sender']), F.from_user.id.in_(config.admin_ids))
    dp.include_router(create_mail_message_router)
    dp.callback_query.register(callbacks.cancel_sending, F.data == "cancel")
    dp.callback_query.register(callbacks.start_sending, F.data.startswith("start"), CreateMessage.confirm_sender)


def set_middlewares():
    dp.update.middleware(DataBaseSession(session_pool=AsyncSessionLocal))


async def main() -> None:
    set_middlewares()
    set_handlers()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())