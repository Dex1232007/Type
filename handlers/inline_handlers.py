from aiogram import Router, F, Bot
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
import base64

from .common import is_member
from utils.youtube import search_youtube

router = Router()

@router.inline_query()
async def handle_inline_query(inline_query: InlineQuery, bot: Bot):
    user_id = inline_query.from_user.id
    query = inline_query.query.strip()

    if not await is_member(bot, user_id):
        await inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    id='not_member',
                    title='❌ Join Required Channels',
                    input_message_content=InputTextMessageContent(
                        message_text="🚫 You need to join our channels to use the bot."
                    )
                )
            ],
            cache_time=5
        )
        return

    if not query:
        await inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    id='empty',
                    title='Type a song name or keyword',
                    input_message_content=InputTextMessageContent(
                        message_text="🔍 Type a song name to search from YouTube..."
                    )
                )
            ],
            cache_time=5
        )
        return
        
    results_data = await search_youtube(query)
    results = []
    
    for video in results_data[:10]: # Limit to 10 results for inline
        results.append(
            InlineQueryResultArticle(
                id=base64.b64encode(video['url'].encode()).decode(),
                title=video['title'],
                description=f"🎧 Author: {video['author']}\n🔗 URL: {video['url']}",
                thumbnail_url=f"https://i.ytimg.com/vi/{video['id']}/hqdefault.jpg",
                input_message_content=InputTextMessageContent(
                    message_text=f"🎵 <b>{video['title']}</b>\n\n🔗URL: {video['url']}\n\n<i>🔌 Powered By @itachiXCoder</i>",
                    parse_mode='HTML'
                ),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🎧 Download", url=f"https://t.me/{(await bot.get_me()).username}?start={video['url']}")],
                    [InlineKeyboardButton(text="🔍 Search More", switch_inline_query_current_chat=video['title'])]
                ])
            )
        )
        
    await inline_query.answer(results, cache_time=5)

