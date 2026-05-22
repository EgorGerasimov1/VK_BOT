from keyboard import KeyboardManager
from .base import BaseHandler
from config import MAX_HEIGHT, MIN_HEIGHT, MAX_AGE, MAX_WEIGHT, MIN_WEIGHT, MIN_BMI, MAX_BMI

class ProfileHandler(BaseHandler):

    def handler(self, user_id, peer_id, message_id, action):
        if action == 'menu':
            message = self.profile(user_id)
            self.bot.edit_message(peer_id, message_id, message, KeyboardManager.get_profile_menu())
        elif action == 'stats':
            self.bot.send_message(user_id, 'Общая статистика')
        elif action == 'edit':
            self.bot.send_message(user_id, 'Напишите ваш: рост вес возраст')
            self.waiting.insert_waiting(user_id, 'profile')

    def handler_waiting(self, user_id, text):
        calculate_data = self.db.get_calculate_data(user_id)
        error, height, weight, age = self.valid_profile_input(text, calculate_data)
        if error:
            self.bot.send_message(user_id, error)
            return
        self.db.edit_profile(user_id, height, weight, age)
        bmi = self.calculate_bmi(height, weight)
        self.bot.send_message(user_id, f'Данные добавлены!\nВаш индекс массы тела: {bmi}')
        self.waiting.clean_waiting(user_id)
    
    def valid_profile_input(self, text, data):
        parts = text.split()
        error = None
        if len(parts) != 3:
            error = 'ФОРМА: рост вес возраст'
            return (error, None, None, None)
        
        for val in parts:
            if not self.is_digit(val, allow_zero=False):
                error = 'Укажите параметры числами!(неотрицательными)'
                return (error, None, None, None)

        height = float(parts[0])
        weight = float(parts[1])
        age = float(parts[2])

        if not age.is_integer():
            error = 'Возраст должен быть целым числом'
            return (error, None, None, None)
        if age > MAX_AGE:
            error = 'Нереалистичный возраст!'
            return (error, None, None, None)
        if height < MIN_HEIGHT or height > MAX_HEIGHT:
            error = 'Нереалистичный рост'
            return (error, None, None, None)
        if weight < MIN_WEIGHT or weight > MAX_WEIGHT:
            error = 'Нереалистичный вес'
            return (error, None, None, None)
        
        bmi = self.calculate_bmi(height, weight)
        if bmi < MIN_BMI or bmi > MAX_BMI:
            error = 'Нереалистичное сочетание роста и веса!'
            return (error, None, None, None)
        
        return(error, height, weight, age)
        

        
        
        
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
        bmi = self.calculate_bmi(height, weight)
        message = f'Имя: {name}\n'
        message += f"Пол: {gender}, Возраст: {age}, Цель: {goal or 'Нет'}\n"
        message += f"Рост: {height}, Вес: {weight}, ИМТ: {bmi}\n"
        return message