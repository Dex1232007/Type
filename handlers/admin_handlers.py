import asyncio
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from config import ADMIN_CHAT_ID
from utils.database import db

router = Router()
router.message.filter(F.from_user.id == ADMIN_CHAT_ID)
router.callback_query.filter(F.from_user.id == ADMIN_CHAT_ID)

class BroadcastState(StatesGroup):
    get_message = State()
    confirm = State()

@router.message(Command("broadcast"))
async def broadcast_command(message: Message, state: FSMContext):
    await message.answer("Please send the message you want to broadcast. It can be text, photo, video, etc., with a caption.")
    await state.set_state(BroadcastState.get_message)

@router.message(BroadcastState.get_message)
async def get_broadcast_message(message: Message, state: FSMContext):
    await state.update_data(
        message_id=message.message_id,
        chat_id=message.chat.id
    )
    
    await message.answer(
        "This is the message to be broadcasted. Are you sure? (yes/no)"
    )
    await state.set_state(BroadcastState.confirm)

@router.message(BroadcastState.confirm)
async def confirm_broadcast(message: Message, state: FSMContext, bot: Bot):
    if message.text.lower() != 'yes':
        await message.answer("Broadcast cancelled.")
        await state.clear()
        return

    data = await state.get_data()
    from_chat_id = data['chat_id']
    message_id = data['message_id']
    
    users = await db.get_all_users()
    
    await message.answer(f"Starting broadcast to {len(users)} users...")
    
    sent_count = 0
    failed_count = 0
    
    for user_id in users:
        try:
            await bot.copy_message(
                chat_id=user_id,
                from_chat_id=from_chat_id,
                message_id=message_id
            )
            sent_count += 1
            await asyncio.sleep(0.1) # Avoid hitting API limits
        except Exception:
            failed_count += 1
            
    await message.answer(f"Broadcast finished.\n\nSent: {sent_count}\nFailed: {failed_count}")
    await state.clear()
