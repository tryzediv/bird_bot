import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType
from env import TOKEN

# Авторизуемся с помощью токена сообщества
vk = vk_api.VkApi(token=TOKEN)
# Работа с сообщениями
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id,
                                'message': message,
                                "random_id": random.randint(0, 2048)})


# Основной цикл бота
for event in longpoll.listen():
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text.lower()

            if request == '123':
                write_msg(event.user_id, 'Я знаю команды: привет, пока')
            elif request == 'привет':
                write_msg(event.user_id, 'ку)')
            elif request == 'пока':
                write_msg(event.user_id, 'поки(')
            elif request == 'лошадка':
                write_msg(event.user_id, '«А интересно, — подумал Ёжик, — '
                                         'если Лошадь ляжет спать, она захлебнётся в тумане?» '
                                         '— и он стал медленно спускаться с горки, чтобы '
                                         'попасть в туман и посмотреть, как там внутри.')
            elif request == 'медвежонок':
                write_msg(event.user_id, '— Я обязательно, ты слышишь? Я обязательно, '
                                         '— сказал Медвежонок. Ёжик кивнул. — Я обязательно приду '
                                         'к тебе, что бы ни случилось. Я буду возле тебя всегда. '
                                         'Ёжик глядел на Медвежонка тихими глазами и молчал. '
                                         '— Ну что ты молчишь? — Я верю, — сказал Ёжик.')
