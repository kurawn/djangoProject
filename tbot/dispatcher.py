from telebot import types
from telebot.apihelper import ApiTelegramException

from tbot_base.bot import tbot
from tbot_base.models import BotConfig
from .models import Chat, User


@tbot.message_handler(commands=['start'])
def start_messages(message: types.Message):
    tbot.send_message(message.from_user.id, 'Чтоб добавить пользователя, напишите #StandForUkraine_Secure + тег '
                                            'человека в тг Система выдаст вам ссылку, которую нужно будет дать лично '
                                            'приглашенному')


@tbot.message_handler(func=lambda message: True)
def text_messages(message: types.Message):
    chat_name = message.text.split(' ')[0]
    chat = Chat.objects.filter(name=chat_name).last()
    if chat:
        user_in_chat = tbot.get_chat_member(chat_id=chat.chat_id, user_id=message.from_user.id)
        print(11)
        print(user_in_chat)
        if user_in_chat.status in ['member', 'creator', 'administrator']:
            link = tbot.create_chat_invite_link(chat_id=chat.chat_id,
                                                name=message.text.replace('@', '').split(' ')[1] + ' ' + str(message.from_user.id),
                                                creates_join_request=True)
            tbot.send_message(message.from_user.id, link.invite_link)
            refer, created_refer = User.objects.get_or_create(user_id=message.from_user.id)
            if created_refer:
                refer.name = f'{message.from_user.first_name} {message.from_user.last_name}'
                refer.username = message.from_user.username
            refer.chats.add(chat)
            refer.save()
        else:
            tbot.send_message(message.from_user.id, f'силка неможе бути згенерована вас немає в чаті{chat_name}')

    else:
        try:

            tbot.send_message(message.from_user.id, f'{chat_name}, немає')
        except Exception as e:
            print(e)


@tbot.my_chat_member_handler(func=lambda message: True)
def add_chat(message: types.Message):
    Chat.objects.get_or_create(name=message.chat.title, chat_id=message.chat.id)


@tbot.chat_join_request_handler(func=lambda message: True)
def join_chat_user(message: types.Message):
    user_name = message.from_user.username
    user_name_in_link = message.invite_link.name.replace('@', '').split(' ')[0]
    if user_name == user_name_in_link:
        try:
            tbot.approve_chat_join_request(chat_id=message.chat.id, user_id=message.from_user.id)
            tbot.revoke_chat_invite_link(chat_id=message.chat.id, invite_link=message.invite_link.invite_link)
            chat = Chat.objects.filter(chat_id=message.chat.id).last()
            if not chat:
                chat =Chat.objects.create(name=message.chat.title, chat_id=message.chat.id)
                chat.name = message.chat.title
                chat.save()
            user, created = User.objects.get_or_create(user_id=message.from_user.id)
            refer, created_refer = User.objects.get_or_create(user_id=message.invite_link.name.split(' ')[1])
            if created:
                user.name = message.from_user.first_name + ' ' + message.from_user.last_name
                user.username = message.from_user.username
                user.refer = refer
            user.chats.add(chat)
            user.save()
        except Exception as e:
            print(e)
    else:
        tbot.decline_chat_join_request(chat_id=message.chat.id, user_id=message.from_user.id)