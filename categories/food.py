from keyboard import KeyboardManager
from .base import BaseHandler
from config import COUNTER_FOOD_PROTEIN, COUNTER_FOOD_CALORIES, MAX_AMOUNT_CALORIES, MAX_AMOUNT_PROTEIN

class FoodHandler(BaseHandler):
    def __init__(self, db, waiting, bot):
        super().__init__(db, waiting, bot)

    def handler(self, user_id, peer_id, message_id, action):
        if action == 'menu':
            self.bot.edit_message(peer_id, message_id, 'Меню еда', KeyboardManager.get_food_menu())
        elif action == 'add':
            self.bot.send_message(user_id, 'Напиши что сегодня поел по форме:\nПродукт белок калории')
            self.waiting.insert_waiting(user_id, 'food')
        elif action == 'stats':
            message = self.today_stats(user_id)
            self.bot.send_message(user_id, message)


    def handler_waiting(self, user_id, text):
        error, product, protein, calories = self.valid_food_input(text)
        if error:
            self.bot.send_message(user_id, error)
            return
        self.db.add_food(user_id, product, protein, calories)
        self.waiting.clean_waiting(user_id)
        today_food = self.db.get_today_stats_food(user_id)
        calculate_data = self.db.get_calculate_data(user_id)
        message = self.form_response(product, protein, calories, today_food, calculate_data)
        self.bot.send_message(user_id, message)
    
    def valid_food_input(self, text):
        parts = text.split()
        error = None
        if len(parts) != 3:
            error = 'ФОРМА: подукт белок калории'
            return (error, None, None, None)
        
        product, protein, calories = parts

        if not self.is_text(product):
            error = 'Продукт не должен быть числом'
            return (error, None, None, None)
        
        if not self.is_digit(protein) or not self.is_digit(calories):
            error = 'Укажите парамметры числами!(неотрицательнымы)'
            return (error, None, None, None)
        
        if float(protein) > MAX_AMOUNT_PROTEIN or float(calories) > MAX_AMOUNT_CALORIES:
            error = 'Укажите приемлемое значение белка(P<100) и калорий(C<2000)'
            return (error, None, None, None)
        
        return (error, product, protein, calories)
    
    def form_response(self, product, protein, calories, today_food, data):
        message = 'Ваш прием пищи:\n'
        message += f'Вы съели: {product}\n'
        for pr, text in COUNTER_FOOD_PROTEIN.items():
            if int(protein) >= pr:
                message += f'Белок: {text}\n'
                break
        for cal, text in COUNTER_FOOD_CALORIES.items():
            if int(calories) >= cal:
                message += f'Калории: {text}\n'
                break
        rda = self.calculate_rda(data['weight'])
        bmr = self.calculate_bmr( data['weight'], data['height'], data['age'], data['gender'])
        message += f"Вы съели сегодня: {today_food['total_protein']}г белка, {today_food['total_calories']} ккал\n"
        message += f"Сколько нужно: От {rda['min_protein']} до {rda['max_protein']}г белка, {bmr} ккал"
        return message

    def today_stats(self, user_id):
        today_food = self.db.get_today_stats_food(user_id)
        food_list = self.db.get_today_food(user_id)
        calculate_data = self.db.get_calculate_data(user_id)
        return self.form_stats_message(today_food, food_list, calculate_data)
        
    def form_stats_message(self, today_food, food_list, data):
        rda = self.calculate_rda(data['weight'])
        bmr = self.calculate_bmr( data['weight'], data['height'], data['age'], data['gender'])

        message = 'Статистика за сегодня:\n'
        message += f"Белка сегодня: {today_food['total_protein'] or '0'}\n"
        message += f"Калорий за сегодня: {today_food['total_calories'] or '0'}\n"
        message += f"Сколько нужно: От {rda['min_protein']} до {rda['max_protein']}г белка, {bmr} ккал\n"
        if food_list:
            message += 'Сегодня вы съели:\n'
            for food in food_list:
                message += f"{food['product']}: {food['protein']}г белка, {food['calories']} ккал, {food['time_only']}"
                message += '\n'
        else:
            message += 'Сегодня вы еще не ели\n'
        return message
        

        
        
