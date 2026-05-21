from keyboard import KeyboardManager
from .base import BaseHandler


class FoodHandler(BaseHandler):

    def handler(self, user_id, peer_id, message_id, action):
        if action == 'menu':
            self.bot.edit_message(peer_id, message_id, 'Меню еда', KeyboardManager.get_food_menu())
        elif action == 'today':
            self.bot.send_message(user_id, 'Напиши что сегодня поел по форме:\nПродукт белок калории')
            self.waiting.insert_waiting(user_id, 'food')
        elif action == 'stats':
            message = self.today_statistics(user_id)
            self.bot.send_message(user_id, message)


    def handler_waiting(self, user_id, text):
        parts = text.split()
        if len(parts) == 3:
            product = parts[0]
            protein = parts[1]
            calories = parts[2]
            self.db.add_food(user_id, product, protein, calories)
            self.waiting.clean_waiting(user_id)
            today_food = self.db.get_today_stats_food(user_id)
            self.bot.send_message(user_id, f"Еда добавлена белка:{today_food['total_protein']} калорий:{today_food['total_calories']}")
        else:
            self.bot.send_message(user_id, 'ФОРМА: подукт белок калории')

    def today_statistics(self, user_id):
        stats = self.db.get_today_statistics(user_id)
        food_list = self.db.get_today_food(user_id)
        message = 'Статистика за сегодня:\n'
        message += f"Белка сегодня: {stats['total_protein'] or '0'}\n"
        message += f"Калорий за сегодня: {stats['total_calories'] or '0'}\n"

        if food_list:
            for food in food_list:
                message += f"-{food['product']}: {food['protein']}г белка, {food['calories']} ккал, {food['time_only']}"
                message += '\n'
        else:
            message += 'Сегодня вы еще не ели'

        return message


