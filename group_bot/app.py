import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from text import responses
from env import TOKEN

# Авторизуемся с помощью токена сообщества
vk = vk_api.VkApi(token=TOKEN)
# Работа с сообщениями
longpoll = VkLongPoll(vk)


def create_carousel():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Что сделать в первую очередь', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Чем накормить стрижа', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Где в Тюмени купить насекомых', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Способы кормления стрижа', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Витамины. Обязательно!', color=VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()


def write_msg(user_id, message, keyboard=None):
    vk.method('messages.send', {'user_id': user_id,
                                'message': message,
                                'random_id': get_random_id(),
                                'keyboard': keyboard})


# Основной цикл бота
for event in longpoll.listen():
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            text = event.text.lower()
            user_id = event.user_id
            if text == 'старт':
                write_msg(user_id, 'Выберите один из вариантов:', create_carousel())

            # Ответы бота, идём циклом по словарю
            for key in responses:
                if text == key:
                    write_msg(user_id, responses[key], create_carousel())
