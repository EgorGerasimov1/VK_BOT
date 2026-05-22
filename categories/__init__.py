from .sport import SportHandler
from .food import FoodHandler
from .sleep import SleepHandler
from .task import TaskHandler
from .profile import ProfileHandler
from .main_menu import MainMenuHandler

#Dict handlers

HANDLERS_CLASSES = {
    'food': FoodHandler,
    'profile': ProfileHandler,
    'sleep': SleepHandler,
    'sport': SportHandler,
    'task': TaskHandler,
    'main_menu': MainMenuHandler
} 