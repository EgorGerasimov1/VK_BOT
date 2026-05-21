from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class KeyboardManager:
    def __init__():
        pass

    @staticmethod    
    def get_main_menu():
        keyboard = VkKeyboard(inline=True)
        keyboard.add_callback_button('Тренировки', payload={'type': 'sport', 'action': 'menu'})
        keyboard.add_callback_button('Сон', payload={'type': 'sleep', 'action': 'menu'})
        keyboard.add_line()
        keyboard.add_callback_button('Еда', payload={'type': 'food', 'action': 'menu'})
        keyboard.add_callback_button('Задачи', payload={'type': 'task', 'action': 'menu'})
        keyboard.add_line()
        keyboard.add_callback_button('Профиль', payload={'type': 'profile', 'action': 'menu'})
        return keyboard

    @staticmethod
    def get_food_menu():
        keyboard = VkKeyboard(inline=True)
        keyboard.add_callback_button('Еда сегодня', payload={'type': 'food', 'action': 'today'})
        keyboard.add_callback_button('Статистика Еды', payload={'type': 'food', 'action': 'stats'})
        keyboard.add_line()
        keyboard.add_callback_button('Назад', payload={'type': 'main_menu', 'action': 'back'})
        return keyboard
    
    @staticmethod
    def get_profile_menu():
        keyboard = VkKeyboard(inline=True)
        keyboard.add_callback_button('Общая статистика', payload={'type': 'profile', 'action': 'stats'})
        keyboard.add_callback_button('Редактировать', payload={'type': 'profile', 'action': 'edit'})
        keyboard.add_line()
        keyboard.add_callback_button('Назад', payload={'type': 'main_menu', 'action': 'back'})
        return keyboard
    
    @staticmethod
    def get_sleep_menu():
        keyboard = VkKeyboard(inline=True)
        keyboard.add_callback_button('Сон сегодня', payload={'type': 'sleep', 'action': 'today'})
        keyboard.add_callback_button('Статистика сна', payload={'type': 'sleep', 'action': 'stats'})
        keyboard.add_line()
        keyboard.add_callback_button('Назад', payload={'type': 'main_menu', 'action': 'back'})
        return keyboard
    
    @staticmethod
    def get_sport_menu():
        keyboard = VkKeyboard(inline=True)
        keyboard.add_callback_button('Тренировка сегодня', payload={'type': 'sport', 'action': 'today'})
        keyboard.add_callback_button('График Тренировок', payload={'type': 'sport', 'action': 'schedule'})
        keyboard.add_line()
        keyboard.add_callback_button('Назад', payload={'type': 'main_menu', 'action': 'back'})
        return keyboard
    
    @staticmethod
    def get_task_menu():
        keyboard = VkKeyboard(inline=True)
        keyboard.add_callback_button('Задачи сегодня', payload={'type': 'task', 'action': 'today'})
        keyboard.add_callback_button('Управление задачами', payload={'type': 'task', 'action': 'control'})
        keyboard.add_line()
        keyboard.add_callback_button('Назад', payload={'type': 'main_menu', 'action': 'back'})
        return keyboard
