
class User_Manager:
    def __init__(self, db, waiting, bot):
        self.db = db
        self.waiting = waiting
        self.bot = bot

    def creat_info(self, user_id):
        if self.db.get_user_data(user_id):
            pass
        else:
            user_info = self.bot.get_user_info(user_id)
            self.db.add_user(user_id, user_info)
            self.bot.send_message(user_id, 'Напишите ваш Рост и Вес')
            self.waiting.insert_waiting(user_id, 'profile')

    def handler_waiting(self, user_id, handlers, text):
        if self.waiting.is_waiting(user_id):
            key = self.waiting.get_waiting(user_id)
            if key in handlers:
                handler = handlers[key].handler_waiting
                handler(user_id, text)
            return True
        return False                