import os
from typing import Dict, Callable
from dotenv import load_dotenv

load_dotenv()

#VK
TOKEN = os.getenv('VK_TOKEN')
ID_CLUB = os.getenv('VK_GROUP_ID')

#DB
DATABASE_PATH = 'data/database.db'

#Dict handlers
from categories import *

HANDLERS_CLASSES = {
    'food': FoodHandler,
    'profile': ProfileHandler,
    'sleep': SleepHandler,
    'sport': SportHandler,
    'task': TaskHandler,
    'main_menu': MainMenuHandler
} 