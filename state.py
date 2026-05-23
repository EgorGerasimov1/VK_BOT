class Waiting:
    def __init__(self):
        self.waiting = {}

    def insert_waiting(self, user_id, category):
        self.waiting[user_id] = category

    def get_waiting(self, user_id):
        return self.waiting.get(user_id)

    def clean_waiting(self, user_id):
        self.waiting.pop(user_id, None)
        
    def is_waiting(self, user_id):
        return user_id in self.waiting