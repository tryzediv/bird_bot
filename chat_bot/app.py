import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from env import TOKEN, GROUP_ID

# Авторизуемся с помощью токена сообщества
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
    message = (f'{user_name}, добро пожаловать в наше гнездышко ^_^ '
               f'Я знаю команды: помоги, птица, ежик')
    write_msg(chat_id, message)


def send_goodbye_message(chat_id, user_id):
    user_info = vk_api.users.get(user_ids=user_id)[0]
    user_name = user_info['first_name']
    message = f"Стриж по имени {user_name} улетел из гнезда..."
    write_msg(chat_id, message)


# Основной цикл бота
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:
            chat_id = event.chat_id
            message_text = event.object.message['text'].lower()

            if message_text == 'помоги':
                write_msg(chat_id, 'Я знаю команды: помоги, птица, ежик')
            elif message_text == 'птица':
                write_msg(chat_id, 'кукушка')
            elif message_text == 'ежик':
                write_msg(chat_id, 'По вечерам Ёжик ходил к Медвежонку '
                                   'считать звёзды. Они усаживались на '
                                   'брёвнышке и, прихлёбывая чай, смотрели '
                                   'на звёздное небо. Оно висело над '
                                   'крышей — прямо за печной трубой. Справа '
                                   'от трубы были звёзды Медвежонка, '
                                   'а слева — Ёжика…')

            if 'action' in event.object.message:
                action = event.object.message['action']
                if action['type'] == 'chat_invite_user':
                    user_id = action['member_id']
                    send_welcome_message(chat_id, user_id)
                elif action['type'] == 'chat_kick_user':
                    user_id = action['member_id']
                    send_goodbye_message(chat_id, user_id)
