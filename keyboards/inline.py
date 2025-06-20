from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import REQUIRED_CHANNELS

def join_channels_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="✅ Verify Membership", callback_data="check_membership")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def start_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🎛️ Mini App", web_app={"url": "https://zawmyo123.serv00.net/youtube/index.html"})],
        [InlineKeyboardButton(text="🔍 Search Song", switch_inline_query_current_chat="")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def search_results_keyboard(results: list) -> InlineKeyboardMarkup:
    buttons = []
    for i, video in enumerate(results):
        buttons.append([InlineKeyboardButton(text=f"{i+1}. Download", callback_data=f"download|{video['url']}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
