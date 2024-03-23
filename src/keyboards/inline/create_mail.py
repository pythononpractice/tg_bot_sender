from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_kb_confirm() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Отправить сейчас", callback_data=f"start"),
        InlineKeyboardButton(text="Отменить", callback_data=f"cancel"),
    )
    return builder