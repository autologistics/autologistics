import time
from datetime import datetime

import pytz
from django.shortcuts import redirect
from telebot import TeleBot
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove, InputFile, Update as up
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.settings import TOKEN, LOCAL_TIME_ZONE

from .utils import export_to_excel, send_mail_to_broker
from .site_parser.main import get_api_samsara_info, get_selenium_info, get_search_samsara_info
from .keyboards import start_buttons, template_buttons, finish_buttons
from .queries import get_user, get_users_chat_id, delete_asset, check_user, get_asset, get_template

bot = TeleBot(TOKEN, parse_mode='HTML')
timezone = pytz.timezone(LOCAL_TIME_ZONE)


def index(request):
    return redirect('admin:index')


@csrf_exempt
def bot_webhook(request):
    json_str = request.body.decode('UTF-8')
    update = up.de_json(json_str)
    bot.process_new_updates([update])
    return JsonResponse({'status': 'ok'})


def roots_message(chat_id):
    bot.send_message(chat_id, 'You have no roots', reply_markup=ReplyKeyboardRemove())


# Стартовый Хендлер
@bot.message_handler(commands=['start'])
def start_handler(message: Message):
    chat_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    user = get_user(chat_id, first_name, last_name, username)
    if user.status:
        bot.send_message(chat_id, 'hello', reply_markup=start_buttons())
    else:
        roots_message(chat_id)


@bot.message_handler(regexp='Search Asset')
def search_asset_handler(message: Message):
    chat_id = message.chat.id
    user = check_user(chat_id)
    if user.status:
        msg = bot.send_message(chat_id, 'Write Asset Name')
        bot.register_next_step_handler(msg, get_result_handler)
    else:
        roots_message(chat_id)


def get_result_handler(message: Message):
    chat_id = message.chat.id
    query = message.text
    user = check_user(chat_id)
    if user.status:
        update = get_asset(query)
        if 'Does not Exists' == update:
            bot.send_message(chat_id, f'{query} ' + update)
        else:
            msg = get_search_samsara_info(update)
            if msg[1]:
                bot.send_message(chat_id, msg[0], reply_markup=template_buttons(msg[2], msg[3]))
            else:
                bot.send_message(chat_id, msg[0], reply_markup=finish_buttons(msg[2]))
    else:
        roots_message(chat_id)


@bot.message_handler(regexp='Get All Assets')
def get_all_assets_handler(message: Message):
    chat_id = message.chat.id
    user = check_user(chat_id)
    if user.status:
        file_path, filename = export_to_excel()
        with open(file_path, mode='rb') as file:
            bot.send_document(chat_id, document=InputFile(file))
    else:
        roots_message(chat_id)


# Хедлер для заврешения Ассета
@bot.callback_query_handler(lambda call: 'finish' in call.data)
def finish_asset_handler(call: CallbackQuery):
    chat_id = call.message.chat.id
    user = check_user(chat_id)
    if user.status:
        _, name = call.data.split('_')
        call_id = call.id
        delete_asset(name)
        bot.answer_callback_query(call_id, f'{name} was Finished')
    else:
        roots_message(chat_id)


@bot.callback_query_handler(lambda call: 'template' in call.data)
def send_mail_handler(call: CallbackQuery):
    chat_id = call.message.chat.id
    user = check_user(chat_id)
    if user.status:
        _, template, mail, name = call.data.split('_')
        call_id = call.id
        subject, context = get_template(template)
        send_mail_to_broker(mail, subject, context)
        bot.answer_callback_query(call_id, f'{name} was Sent')
    else:
        roots_message(chat_id)


def selenium_parser():
    print('Selenium Parser')
    messages = get_selenium_info()
    for message in messages:
        time.sleep(2)
        for chat_id in get_users_chat_id():
            if message[1]:
                bot.send_message(chat_id, message[0], reply_markup=template_buttons(message[2], message[3]))
            else:
                bot.send_message(chat_id, message[0], reply_markup=finish_buttons(message[2]))


def samsara_parser():
    print('Samsara Parser')
    local_time = datetime.now(tz=timezone)
    if local_time.hour != 8 and local_time.minute != 0:
        messages = get_api_samsara_info()
        for message in messages:
            time.sleep(2)
            for chat_id in get_users_chat_id():
                if message[1]:
                    bot.send_message(chat_id, message[0], reply_markup=template_buttons(message[2], message[3]))
                else:
                    bot.send_message(chat_id, message[0], reply_markup=finish_buttons(message[2]))
