import os
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
    obj, _ = site_app.models.BotDb.objects.get_or_create(group_id_bot=message.chat.id)
    bot.send_message(message.chat.id, "Привет!Ты записан в базу {}".format(message.chat.id))



def send_message(quryset):
    for user_bot in quryset:
        try:
            bot.send_message(int(user_bot.group_id_bot), "Привет!сообщение {}".format(user_bot))
        except Exception:
            logger.error('No ok-"%s"' % user_bot)
    logger.info('Successfully send "%s"' % 'ok')

