import asyncio
import time
from typing import List, Dict
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import Message
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.requests import change_active


def generate_keyboard(
        btn_text: str = None,
        btn_url: str = None
) -> InlineKeyboardMarkup | None:
    btn_builder = InlineKeyboardBuilder()
    btn_builder.row(
        InlineKeyboardButton(
            text=btn_text,
            url=btn_url
        )
    )
    return btn_builder.as_markup()


async def send_preview_with_keyboard(
        message: Message,
        photo: str = None,
        text: str = '',
        btn_text: str = None,
        btn_url: str = None,
) -> int:
    keyboard = generate_keyboard(btn_text, btn_url)
    sent_message = await message.answer_photo(caption=text, photo=photo, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN_V2)
    return sent_message.message_id


async def send_preview(
        message: Message,
        data: Dict
) -> int:
    message_id = await send_preview_with_keyboard(
        message,
        data['msg_photo'],
        data['msg_text'],
        data['btn_text'],
        data['btn_url']
    )
    return message_id


async def send_mail(
        session: AsyncSession,
        bot: Bot,
        user_id: str,
        from_chat_id: int,
        message_id: int,
        keyboard: InlineKeyboardMarkup = None) -> bool:
    try:
        await bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id, message_id=message_id, reply_markup=keyboard)
    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
        return await send_mail(session, bot, user_id, from_chat_id, message_id, keyboard)
    except Exception as e:
        print(e)
        await change_active(session, user_id, False)
        return False
    else:
        return True


async def start_sender(
        session: AsyncSession,
        bot: Bot,
        data: Dict,
        user_ids: List[str],
        from_chat_id: int,
        message_id: int
) -> int:
    count = 0
    keyboard = generate_keyboard(data['btn_text'], data['btn_url'])
    for u_id in user_ids:
        if await send_mail(session, bot, u_id, from_chat_id, message_id, keyboard):
            count += 1
        await asyncio.sleep(0.05)
    # print(f'Отправлено {count}/{len(user_ids)} за {round(time.time() - t_start)}с')
    return count
