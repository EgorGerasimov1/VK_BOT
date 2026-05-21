
class BaseHandler:
    def __init__(self, db, waiting, bot):
        self.db = db
        self.waiting = waiting
        self.bot = bot

    def handle(self):
        raise NotImplementedError
    
    def handle_waiting(self):
        raise NotImplementedError