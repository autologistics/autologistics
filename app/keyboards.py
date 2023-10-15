from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from .queries import get_all_templates_title


# TODO: Работа с Кнопками Бота
# Функция для создания стартовых кнопок
def start_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    search_button = KeyboardButton(text='Search Asset')
    all_assets = KeyboardButton(text='Get All Assets')
    markup.add(search_button, all_assets)
    return markup


# Функция для создания шаблонных кнопок
def template_buttons(name, mail):
    markup = InlineKeyboardMarkup(row_width=3)
    templates = get_all_templates_title()
    buttons = []
    for template in templates:
        buttons.append(InlineKeyboardButton(text=template, callback_data=f'template_{template}_{mail}_{name}'))
    markup.add(*buttons)
    finish_btn = InlineKeyboardButton(text='Finish', callback_data=f'finish_{name}')
    markup.add(finish_btn)
    return markup


# Функция для Завершения Ассета
def finish_buttons(name):
    markup = InlineKeyboardMarkup()
    finish_btn = InlineKeyboardButton(text='Finish', callback_data=f'finish_{name}')
    markup.add(finish_btn)
    return markup
