import json
import asyncio
from typing import Dict, List, Any

from config import DATABASE_FILE

class Database:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._lock = asyncio.Lock()
        self._data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"users": [], "cooldowns": {}}

    async def _save_data(self):
        async with self._lock:
            with open(self.file_path, 'w') as f:
                json.dump(self._data, f, indent=4)

    async def add_user(self, user_id: int):
        if user_id not in self._data['users']:
            self._data['users'].append(user_id)
            await self._save_data()

    async def get_all_users(self) -> List[int]:
        return self._data['users']

    async def get_cooldowns(self) -> Dict[str, int]:
        return self._data.get('cooldowns', {})

    async def set_cooldowns(self, cooldowns: Dict[str, int]):
        self._data['cooldowns'] = cooldowns
        await self._save_data()

db = Database(DATABASE_FILE)
