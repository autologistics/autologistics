from app.models import Update, TelegramUser, MailTemplate


# TODO: Работа с Моделью TelegramUser
# Функция для проверки Пользователя в БД
def get_user(chat_id, first_name, last_name, username):
    user, check = TelegramUser.objects.get_or_create(chat_id=chat_id)
    if check:
        user.chat_id = chat_id
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.save()
    return user


def check_user(chat_id):
    user = TelegramUser.objects.get(chat_id=chat_id)
    return user


# Функция для получения Chat ID проверенных Пользователей
def get_users_chat_id():
    users = [user.chat_id for user in TelegramUser.objects.all() if user.status]
    return users


# TODO: Работа с Моделью MailTemplate
# Функция для нахождения всех Шаблонов
def get_all_templates_title():
    templates = [template.title for template in MailTemplate.objects.all()]
    return templates


# Функция для получения Шаблона
def get_template(title):
    template = MailTemplate.objects.get(title=title)
    subject = template.subject
    context = template.context
    return subject, context


# TODO: Работа с Моделью Update
# Функция для Удаления Ассета
def delete_asset(name):
    update = Update.objects.get(name=name)
    update.delete()


def get_asset(query):
    try:
        update = Update.objects.get(name__icontains=query)
        return update
    except:
        return f'Does not Exists'
