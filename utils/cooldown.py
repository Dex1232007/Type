import time
from typing import Union

from config import COOLDOWN_TIME
from .database import db

async def check_cooldown(user_id: int) -> Union[int, bool]:
    cooldowns = await db.get_cooldowns()
    current_time = int(time.time())

    if str(user_id) in cooldowns:
        time_passed = current_time - cooldowns[str(user_id)]
        if time_passed < COOLDOWN_TIME:
            return COOLDOWN_TIME - time_passed
    return False

async def set_cooldown(user_id: int):
    cooldowns = await db.get_cooldowns()
    cooldowns[str(user_id)] = int(time.time())
    await db.set_cooldowns(cooldowns)
