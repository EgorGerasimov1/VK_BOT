from keyboard import KeyboardManager
from .base import BaseHandler


class SportHandler(BaseHandler):
    def __init__(self, db, waiting, bot):
        super().__init__(db, waiting, bot)
        
    def handler(self, user_id, peer_id, message_id, action):
        if action == 'menu':
            self.bot.edit_message(peer_id, message_id, 'Меню тренировок', KeyboardManager.get_sport_menu())
        elif action == 'today':
            self.bot.send_message(user_id, 'Вот что у тебя сегодня')
        elif action == 'schedule':
            self.bot.send_message(user_id, 'Твой график')

    def handler_waiting(self):
        pass