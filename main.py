import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import TOKEN, ID_CLUB, DATABASE_PATH, MAX_LEN_MESSAGE
from categories import HANDLERS_CLASSES
from vkbot import VkBot
from keyboard import KeyboardManager
from database import DataBase
from waiting import Waiting
from cache import BotCaсhe
from user_manager import User_Manager
import time

vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk_session, ID_CLUB)
vk = vk_session.get_api()

bot = VkBot(vk)
waiting = Waiting()
db = DataBase(DATABASE_PATH)
cache = BotCaсhe()
user_manager = User_Manager(db, waiting, bot)

handlers = {}
for category, Handler_Class in HANDLERS_CLASSES.items():
    handlers[category] = Handler_Class(db, waiting, bot)
    
#Цикл работы программы
def run():
    while True:
        try:
            for event in longpoll.listen():
                if not _handler_event(event):
                    continue
        except Exception as e:
            print(f'Какая-то ошибка: {e}')
            print('Перезагрузка через 5 секунд')
            time.sleep(5)


def _handler_event(event) -> bool:
    if event.type == VkBotEventType.MESSAGE_NEW:
        user_id = event.obj.message['from_id']
        text = event.obj.message['text'].lower().strip()

        if len(text) > MAX_LEN_MESSAGE:
            bot.send_message(user_id, 'Слишком длинный запрос!')
            return False

        user_manager.create_info(user_id)

        if user_manager.handler_waiting(user_id, handlers, text):
            return False
                    
        if text in ['меню','начать']:
            bot.send_message(user_id, 'Вот меню', KeyboardManager.get_main_menu())
        elif text == 'привет':
            bot.send_message(user_id, 'И тебе привет, напиши (меню) для работы со мной')
        else:
            bot.send_message(user_id, 'Напиши (меню) для работы со мной')

    elif event.type == VkBotEventType.MESSAGE_EVENT:
        user_id = event.obj.user_id
        payload = event.obj.payload
        peer_id = event.obj.peer_id
        message_id = event.obj.conversation_message_id

        vk.messages.sendMessageEventAnswer(
            event_id=event.obj.event_id,
            user_id=user_id,
            peer_id=peer_id
        )

        action_type = payload.get('type')
        action_action = payload.get('action')

        key = (action_type)

        if key in handlers:
            handler = handlers[key].handler
            handler(user_id, peer_id, message_id, action_action)
        else:
            print('Несуществующий ключ')
    return True


if __name__ == '__main__':
    run()