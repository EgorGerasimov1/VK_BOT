from keyboard import KeyboardManager
from .base import BaseHandler


class MainMenuHandler(BaseHandler):
        def __init__(self, db, waiting, bot):
                super().__init__(db, waiting, bot)
                
        def handler(self, user_id, peer_id, message_id, action=None):
                self.bot.edit_message(peer_id, message_id, 'Главное меню:', KeyboardManager.get_main_menu())

        