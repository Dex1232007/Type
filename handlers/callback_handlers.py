from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from .common import is_member
from utils.cooldown import check_cooldown, set_cooldown
from .message_handlers import process_youtube_url

router = Router()

@router.callback_query(F.data == "check_membership")
async def check_membership_callback(callback: CallbackQuery, bot: Bot):
    if await is_member(bot, callback.from_user.id):
        await callback.message.edit_text(
            "✅ Membership Verified!\n\n"
            "You can now use all bot features.\n\n"
            "Send /start to begin."
        )
        await callback.answer("Membership verified successfully!")
    else:
        await callback.answer("❌ You still need to join all channels!", show_alert=True)

@router.callback_query(F.data.startswith("download|"))
async def download_callback(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id

    remaining_cooldown = await check_cooldown(user_id)
    if remaining_cooldown:
        await callback.answer(f"⏳ Please wait {remaining_cooldown} seconds before your next request", show_alert=True)
        return

    await set_cooldown(user_id)
    await callback.answer("Processing your request...")
    
    await callback.message.edit_text("⏳ Processing your request...")
    
    youtube_url = callback.data.split("|")[1]
    await process_youtube_url(youtube_url, callback.message, bot)
