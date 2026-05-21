class BotCaсhe:
    def __init__(self):
        self.caсhe = {}

    def insert_caсhe(self, user_id, user_info):
        self.caсhe[user_id] = user_info
    
    def get_caсhe(self, user_id):
        return self.caсhe.get(user_id)
    
    def clean_caсhe(self, user_id):
        self.caсhe.pop(user_id, None)

    def is_caсhe(self, user_id):
        return user_id in self.caсhe
        
