import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType
from env import TOKEN

# Авторизуемся с помощью токена сообщества
vk = vk_api.VkApi(token=TOKEN)
# Работа с сообщениями
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random.randint(0, 2048)})


# Основной цикл бота
for event in longpoll.listen():
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text.lower()
            # request = request.lower()

            if request == '123':
                write_msg(event.user_id, 'Я знаю команды: привет, пока')
            elif request == 'привет':
                write_msg(event.user_id, 'ку)')
            elif request == 'пока':
                write_msg(event.user_id, 'поки(')
            # else:
            #     write_msg(event.user_id, 'Я не поняв...')
