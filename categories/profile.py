from keyboard import KeyboardManager
from .base import BaseHandler


class ProfileHandler(BaseHandler):

    def handler(self, user_id, peer_id, message_id, action):
        if action == 'menu':
            message = self.profile(user_id)
            self.bot.edit_message(peer_id, message_id, message, KeyboardManager.get_profile_menu())
        elif action == 'stats':
            self.bot.send_message(user_id, 'Общая статистика')
        elif action == 'edit':
            self.bot.send_message(user_id, 'Напишите ваш Рост и Вес')
            self.waiting.insert_waiting(user_id, 'profile')

    def handler_waiting(self, user_id, text):
        parts = text.split()
        if len(parts) == 2:
            height = int(parts[0])
            weight = int(parts[1])
            self.db.edit_profile(user_id, weight, height)
            self.waiting.clean_waiting(user_id)
            bmi = self.bmi(height, weight)
            self.bot.send_message(user_id, f'Рост и вес добавлен!\nВаш индекс массы тела: {bmi}')
        else:
            self.bot.send_message(user_id, 'ФОРМА: рост вес')

    def bmi(self, height, weight):
        height_m = height / 100
        bmi = weight / (height_m * height_m)
        return round(bmi, 1)
    
    def profile(self, user_id):
        user_data = self.db.get_user_data(user_id)
        name, height, weight, gender, age, goal = (
            user_data['user_name'],
            user_data['height'],
            user_data['weight'],
            user_data['gender'],
            user_data['age'],
            user_data['goal']
        )
        bmi = self.bmi(height, weight)
        message = f'Имя: {name}\n'
        message += f"Пол: {gender}, Возраст: {age}, Цель: {goal or 'Нет'}\n"
        message += f"Рост: {height}, Вес: {weight}, ИМТ: {bmi}\n"
        return message