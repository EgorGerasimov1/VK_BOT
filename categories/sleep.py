from keyboard import KeyboardManager
from .base import BaseHandler


class SleepHandler(BaseHandler):
    def __init__(self, db, waiting, bot):
        super().__init__(db, waiting, bot)
    def handler(self, user_id, peer_id, message_id, action):
        if action == 'menu':
            self.bot.edit_message(peer_id, message_id, 'Меню Сна', KeyboardManager.get_sleep_menu())
        elif action == 'today':
            self.bot.send_message(user_id, 'Твой сон сегодня')
        elif action == 'stats':
            self.bot.send_message(user_id, 'Статистика твоего сна')

    def handler_waiting(self):
        pass