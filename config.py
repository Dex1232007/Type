import os
from dotenv import load_dotenv

load_dotenv()

# --- BOT ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "7823078864:AAFE6NYwhsfwOQr58JJCvwhhAppsK9bS7xc")

# --- ADMIN ---
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", 6468293575))

# --- CHANNELS ---
REQUIRED_CHANNELS = ['@Yagami_xlight', '@movie_mmsb']

# --- SETTINGS ---
COOLDOWN_TIME = 10  # in seconds
MAX_SEARCH_RESULTS = 10

# --- DATABASE ---
DATABASE_FILE = 'database.json'
