import os
from typing import Dict, Callable
from dotenv import load_dotenv

load_dotenv()

#VK
TOKEN = os.getenv('VK_TOKEN')
ID_CLUB = os.getenv('VK_GROUP_ID')

MAX_LEN_MESSAGE = 100

#DB
DATABASE_PATH = 'data/database.db'


#Food
MAX_AMOUNT_PROTEIN = 100
COUNTER_FOOD_PROTEIN = {
    70: 'Большое содержание белка на один прием пищи!',
    51: 'Порог нормы белка за один прием пищи',
    30: 'Отличный прием белковой пищи!',
    15: 'Хороший прием белковой пищи(В следующий прием нужно добрать белка)',
    0: 'Низкое содержание белка(Включите в рацион больше белковых продуктов)'
}
MAX_AMOUNT_CALORIES = 2000
COUNTER_FOOD_CALORIES = {
    1400: 'Большое содержание калорий на один прием пищи!',
    600: 'Нормальный прием пищи по калориям',
    250: 'Легкий прием пищи по калориям',
    0: 'Очень низкая калорийность'
}

#profile
MAX_AGE  = 120
MIN_HEIGHT = 55
MAX_HEIGHT = 251
MIN_WEIGHT = 10
MAX_WEIGHT = 600
MIN_BMI = 12
MAX_BMI = 55