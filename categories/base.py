
class BaseHandler:
    def __init__(self, db, waiting, bot):
        self.db = db
        self.waiting = waiting
        self.bot = bot

    def handle(self):
        raise NotImplementedError
    
    def handle_waiting(self):
        raise NotImplementedError
    
    def check_text(self, value):
        if value.isdigit():
            return False
        return True

    def check_digit(self, value, allow_zero=True):
        value = value.replace(',','.')
        try:
           num = float(value)
        except ValueError:
             return False
        if num < 0:
            return False
        if num == 0:
            return allow_zero
        return True