import os
from pathlib import Path
from typing import Final
from dotenv import load_dotenv


load_dotenv()


class Config:
    TOKEN = os.getenv('BOT_TOKEN', 'Enter bot token to the .env!')
    ADMIN_IDS = tuple(int(i) for i in str(os.getenv('BOT_ADMIN_IDS')).split(','))
    SOURCE_FOLDER = os.path.join(Path(__file__).parent, 'source')
    RESULT_FOLDER = os.path.join(Path(__file__).parent, 'result')
    POSTIZ_API_KEY = os.getenv('POSTIZ_API_KEY')
    POSTIZ_UPLOAD_FILE_URL = os.getenv('POSTIZ_UPLOAD_FILE_URL')
    POSTIZ_POST_VIDEOS_URL = os.getenv('POSTIZ_POST_VIDEOS_URL')
    RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
    DATABASE_PATH = os.getenv('DATABASE_PATH')
    MAX_LINKS_PER_CHANNEL = 10

    DEBUG: Final = bool(os.getenv('DEBUG'))
