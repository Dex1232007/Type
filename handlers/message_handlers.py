from aiogram import Router, F, Bot
from aiogram.types import Message

from utils.cooldown import check_cooldown, set_cooldown
from utils.youtube import extract_youtube_url_only, search_youtube, get_yt_info, get_audio_info
from keyboards.inline import search_results_keyboard
from config import MAX_SEARCH_RESULTS

router = Router()

async def process_youtube_url(url: str, message: Message, bot: Bot):
    info = await get_yt_info(url)
    if not info['ok']:
        await message.answer(f"❌ Failed to get video info. Error: {info['error']}")
        return

    audio_info = await get_audio_info(url)
    if not audio_info['ok']:
        await message.answer(f"❌ Failed to get download link. Error: {audio_info['error']}")
        return
        
    try:
        await bot.send_chat_action(message.chat.id, 'upload_audio')
        await message.answer_audio(
            audio=audio_info['download_url'],
            title=info['title'],
            performer=info['author'],
            duration=int(info['duration']) if info['duration'].isdigit() else 0,
            thumbnail=info['thumbnail'],
            caption="Make By @ItachiXCoder"
        )
    except Exception as e:
        await message.answer(f"❌ Failed to send audio. Error: {e}")

@router.message(F.text)
async def handle_text_message(message: Message, bot: Bot):
    user_id = message.from_user.id
    
    # Cooldown Check
    remaining_cooldown = await check_cooldown(user_id)
    if remaining_cooldown:
        await message.answer(f"⏳ Please wait {remaining_cooldown} seconds before your next request.")
        return

    await set_cooldown(user_id)

    # YouTube URL Handling
    youtube_url = extract_youtube_url_only(message.text)
    if youtube_url:
        await message.answer("⏳ Processing your YouTube link...")
        await process_youtube_url(youtube_url, message, bot)
        return

    # Search Handling
    await message.answer(f'🔍 Searching YouTube for "{message.text}"...')
    results = await search_youtube(message.text)
    
    if not results:
        await message.answer(f'❌ No results found for "{message.text}"')
        return
        
    message_text = "📋 <b>Search Results:</b>\n\n"
    search_results = results[:MAX_SEARCH_RESULTS]
    
    for i, video in enumerate(search_results):
        message_text += f"{i+1}. <b>{video['title']}</b>\n"
        
    await message.answer(
        message_text, 
        reply_markup=search_results_keyboard(search_results), 
        parse_mode='HTML'
    )
