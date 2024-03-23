from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F
from src.keyboards.inline.create_mail import get_kb_confirm
from src.states.base import CreateMessage
from src.utils import sender

router = Router()


@router.message(CreateMessage.get_text, F.text)
async def set_text_handler(message: Message, state: FSMContext):
    await state.update_data(msg_text=message.md_text)
    await message.answer(
        text="Отлично, а теперь отправьте фото:"
    )
    await state.set_state(CreateMessage.get_photo)


@router.message(CreateMessage.get_photo, F.photo)
async def set_photo_handler(message: Message, state: FSMContext):
    await state.update_data(msg_photo=message.photo[-1].file_id)
    data = await state.get_data()
    await state.set_state(CreateMessage.get_keyboard_text)
    await message.answer(
        text="Введите текст для кнопки:"
    )


@router.message(CreateMessage.get_keyboard_text, F.text)
async def set_btn_text_handler(message: Message, state: FSMContext):
    await state.update_data(btn_text=message.text)
    await state.set_state(CreateMessage.get_keyboard_url)
    await message.answer('Супер! Осталось отправьте ссылку для кнопки:')


@router.message(CreateMessage.get_keyboard_url, F.text)
async def set_btn_url_handler(message: Message, state: FSMContext):
    await state.update_data(btn_url=message.text)
    data = await state.get_data()
    message_id = await sender.send_preview(
        message,
        data
    )
    await state.update_data(message_id=message_id)
    await message.answer(
        text='*Сообщение для рассылки сформировано!*\n\nЧтобы начать, нажмите кнопку ниже',
        reply_markup=get_kb_confirm().as_markup(),
        parse_mode=ParseMode.MARKDOWN
    )
    await state.set_state(CreateMessage.confirm_sender)