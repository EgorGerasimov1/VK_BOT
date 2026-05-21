from keyboard import KeyboardManager
from .base import BaseHandler


class TaskHandler(BaseHandler):

    def handler(self, user_id, peer_id, message_id, action):
        if action == 'menu':
            self.bot.edit_message(peer_id, message_id, 'Меню задач', KeyboardManager.get_task_menu())
        elif action == 'today':
            self.bot.send_message(user_id, 'Задачи на сегодня')
        elif action == 'control':
            self.bot.send_message(user_id, 'Управления задачами')

    def handler_waiting(self):
        pass