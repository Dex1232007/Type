import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from config import REQUIRED_CHANNELS
from utils.database import db
from keyboards.inline import start_keyboard, join_channels_keyboard

router = Router()

async def is_member(bot, user_id: int) -> bool:
    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception as e:
            logging.error(f"Failed to check membership for {user_id} in {channel}: {e}")
            # If the bot can't check, let's be lenient. Or you can return False.
            continue
    return True

@router.message(CommandStart())
async def command_start_handler(message: Message, bot) -> None:
    await db.add_user(message.from_user.id)
    
    if not await is_member(bot, message.from_user.id):
        text = (
            "🔒 Restricted Access\n\n"
            "You must join our channels to use this bot:\n\n"
            f"1. {REQUIRED_CHANNELS[0]}\n"
            f"2. {REQUIRED_CHANNELS[1]}\n\n"
            "Join them and click the button below to verify:"
        )
        await message.answer(text, reply_markup=join_channels_keyboard())
        return

    text = (
        "🎵 <b>YouTube Music Bot</b>\n\n"
        "Send me:\n"
        "• A song name to search\n"
        "• A YouTube URL to download\n\n"
        "<i>Made by @ItachiXCoder</i>"
    )
    await message.answer(text, reply_markup=start_keyboard(), parse_mode='HTML')

# Middleware to check membership for all handlers
@router.message()
@router.callback_query()
async def membership_check_middleware(handler, event, data):
    bot = data['bot']
    user_id = event.from_user.id
    
    if not await is_member(bot, user_id):
        text = (
            "🚫 Access Denied\n\n"
            "You need to join our channels to use this bot:\n\n"
            f"1. {REQUIRED_CHANNELS[0]}\n"
            f"2. {REQUIRED_CHANNELS[1]}\n\n"
            "Join them and click the button below to verify:"
        )
        if isinstance(event, Message):
            await event.answer(text, reply_markup=join_channels_keyboard())
        elif isinstance(event, CallbackQuery):
            await event.message.edit_text(text, reply_markup=join_channels_keyboard())
            await event.answer("❌ You must join our channels first!", show_alert=True)
        return
        
    return await handler(event, data)
