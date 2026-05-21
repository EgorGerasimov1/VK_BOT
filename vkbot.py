from vk_api.utils import get_random_id
from datetime import datetime 

#Работа с vk_api
class VkBot:
    def __init__(self, vk):
        self.vk = vk
        
    # Отправка нового сообщения и редактирование старого
    def send_message(self, user_id, text, keyboard=None):
        if keyboard:
            self.vk.messages.send(
                user_id=user_id,
                message=text,
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
        else:
            self.vk.messages.send(
                user_id=user_id,
                message=text,
                random_id=get_random_id()
            )

    def edit_message(self, peer_id, message_id, new_text, keyboard=None):
        if keyboard:
            self.vk.messages.edit(
                peer_id=peer_id,
                conversation_message_id=message_id,
                message=new_text,
                keyboard=keyboard.get_keyboard()
            )
        else:
            self.vk.messages.edit(
                peer_id=peer_id,
                conversation_message_id=message_id,
                message=new_text,
            )
            
    def get_user_info(self,user_id):
        user = self.vk.users.get(user_ids=user_id, fields='bdate, sex')[0]
        user_name = f"{user['first_name']} {user['last_name']}"

        age = None
        bdate = user.get('bdate')
        if bdate and bdate.count('.') == 2:
            now = datetime.now()
            b_date = datetime.strptime(bdate, "%d.%m.%Y")
            age = now.year - b_date.year
            if (now.month, now.day) < (b_date.month, b_date.day):
                age -= 1
            
        sex = user.get('sex')
        convert = {0: 'Не указано', 1: 'Жен', 2: 'Муж'}
        gender = convert.get(sex)

        user_info = {
            'name': user_name,
            'age': age,
            'gender': gender
        }
        return user_info