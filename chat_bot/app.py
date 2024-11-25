import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from env import TOKEN, GROUP_ID
from text import responses
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

vk = vk_api.VkApi(token=TOKEN)
vk_api = vk.get_api()
longpoll = VkBotLongPoll(vk, GROUP_ID)


def write_msg(chat_id, message):
    vk_api.messages.send(
        chat_id=chat_id,
        message=message,
        random_id=get_random_id()
    )


# Функция для отправки приветственного сообщения
def send_welcome_message(chat_id, user_id):
    user_info = vk_api.users.get(user_ids=user_id)[0]
    user_name = user_info['first_name']
    message = (f'Добрый день {user_name}! ' + responses['HELLO'])
    write_msg(chat_id, message)


# Функция для отправки прощального сообщения
def send_goodbye_message(chat_id, user_id):
    user_info = vk_api.users.get(user_ids=user_id)[0]
    user_name = user_info['first_name']
    message = f"Стриж по имени {user_name} улетел из гнезда..."
    write_msg(chat_id, message)


# Основной цикл бота
for event in longpoll.listen():
    logging.info(f"event.object.message: {event.object.message}")
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:
            chat_id = event.chat_id
            message_text = event.object.message['text'].lower()
            # Следим за действиями юзеров
            if 'action' in event.object.message:
                action = event.object.message['action']
                logging.info(f"Action: {action}")
                if action['type'] == 'chat_invite_user' \
                        or action['type'] == 'chat_invite_user_by_link':
                    user_id = action['member_id']
                    send_welcome_message(chat_id, user_id)
                elif action['type'] == 'chat_kick_user' \
                        or action['type'] == 'chat_kick_user_by_link':
                    user_id = action['member_id']
                    send_goodbye_message(chat_id, user_id)
                elif action['type'] == 'chat_photo_update':
                    write_msg(chat_id, 'Чик чирик, крутая фотка =)')
            # Ответы бота, идём циклом по словарю
            for key in responses:
                if message_text == key:
                    write_msg(chat_id, responses[key])
