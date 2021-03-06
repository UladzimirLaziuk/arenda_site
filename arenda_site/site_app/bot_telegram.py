import os

from telebot.apihelper import ApiTelegramException

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arenda_site.settings')

from arenda_site.settings import bot

import site_app
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# rental ->name
# t.me/RentalMinBot


@bot.message_handler(commands=['start'])
def start_message(message):
    print(message.chat.id)
    obj, _ = site_app.models.BotDb.objects.get_or_create(group_id_bot=message.chat.id)
    bot.send_message(message.chat.id, "Привет!Ты записан в базу {}".format(message.chat.id))



def send_message(quryset, text):
    logger.info(' send for quryset -"%s"' % quryset)
    for user_bot in quryset:
        try:
            msg = bot.send_message(int(user_bot.group_id_bot), "Привет!сообщение {}".format(text))
            logger.info(' send for user_bot -"%s"' % user_bot.group_id_bot)
        except Exception:
            logger.error('No ok-"%s"' % user_bot)
        logger.info('Successfully send "%s"' % 'ok')
        return msg.message_id
    return None

#
# from telebot import types


@bot.message_handler(content_types=['text'])
def handle_text(message):

    bot.send_message(message.from_user.id, 'Что\nЧто?')

# hideBoard = types.ReplyKeyboardRemove()
# chat_id = 404086968
# a = types.ReplyKeyboardRemove()
# bot.send_message(message.from_user.id, 'Что', reply_markup=a)
# bot.send_message(chat_id, 't')


def del_message(el):
    for chat in site_app.models.BotDb.objects.all():
        logger.info(f'trying to remove from the chat_id-{chat}  {el}')
        try:
            res = bot.delete_message(chat.group_id_bot, el)
        except ApiTelegramException:
            logger.info(f'message - {el} -not found')
            res = None
        logger.info('Successfully delete "%s"' % res)
        return res

