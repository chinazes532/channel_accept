import datetime

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ChatJoinRequest

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb

from app.filters.admin_filter import AdminProtect

from app.database.requests.user.add import set_user
from config import CHANNEL_ID

user = Router()


@user.callback_query(F.data == "check_sub")
async def check_sub(callback: CallbackQuery):
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    
    await callback.message.edit_text("Спасибо за подписку, вы можете пользоваться ботом!")

    await set_user(callback.from_user.id, callback.from_user.full_name, current_date)


@user.message(CommandStart())
async def start_command(message: Message):
    admin = AdminProtect()
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    if not await admin(message):
        await set_user(message.from_user.id, message.from_user.full_name, current_date)
    else:
        await set_user(message.from_user.id, message.from_user.full_name, current_date)
        await message.answer(f"Вы успешно авторизовались как администратор!",
                             reply_markup=rkb.admin_menu)


@user.chat_join_request()
async def handle_chat_join_request(join_request: ChatJoinRequest, bot: Bot):
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    if join_request.chat.id == CHANNEL_ID:
        await set_user(join_request.from_user.id, join_request.from_user.full_name, current_date)
        await join_request.approve()
        await bot.send_message(join_request.from_user.id, "Заявка принята!")

