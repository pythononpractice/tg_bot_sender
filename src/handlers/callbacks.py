import time
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.requests import get_active_users
from src.keyboards.inline.create_mail import get_kb_confirm
from src.states.base import CreateMessage
from src.utils import sender
from src.main import bot


async def cancel_sending(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Рассылка отменена(')
    await state.clear()
    await callback.answer()


async def start_sending(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await callback.message.answer('Рассылка началась')
    await state.clear()
    await callback.answer()

    user_ids = await get_active_users(session)
    t_start = time.time()
    message_id = data.get('message_id')
    count = await sender.start_sender(
        session=session,
        bot=bot,
        data=data,
        user_ids=user_ids,
        from_chat_id=callback.message.chat.id,
        message_id=message_id)
    await callback.message.answer(f'Отправлено {count}/{len(user_ids)} за {round(time.time() - t_start)}с')


