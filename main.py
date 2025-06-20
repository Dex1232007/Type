import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers import common, message_handlers, callback_handlers, inline_handlers, admin_handlers

async def main() -> None:
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    # Register routers
    dp.include_router(common.router)
    dp.include_router(admin_handlers.router)
    dp.include_router(message_handlers.router)
    dp.include_router(callback_handlers.router)
    dp.include_router(inline_handlers.router)
    
    # Register middleware
    dp.message.middleware()(common.membership_check_middleware)
    dp.callback_query.middleware()(common.membership_check_middleware)

    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
