from celery.utils.log import get_task_logger
import logging
from arenda_site.celery import app
from site_app.bot_telegram import send_message

from site_app import models

logger = get_task_logger(__name__)

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


@app.task(bind=True, default_retry_delay=5 * 60)
def send_sms_task(self, data_id, *args, **kwargs):
    logger.info("in task")
    data_text = text_for_bot(data_id)
    send_message(models.BotDb.objects.all(), data_text)
    logger.info("Send sms %s" % data_text)


def text_for_bot(id_table):

    from site_app.models import SearchTable
    import locale
    locale.setlocale(locale.LC_TIME, "ru_RU.utf8")
    obj = SearchTable.objects.get(pk=id_table)
    location = obj.location
    date_start_period = obj.date_start_period_work.strftime("%d %B %Y")
    date_end_period = obj.date_end_period_work.strftime("%d %B %Y")
    estimated_working_time = obj.estimated_working_time
    template_text = f'''
    Если вы получили это сообщение то срочно выезжайте
    Место проведения работ -{location}\n
    Дата начала периода проведения работ -{date_start_period}\n
    Дата начала периода проведения работ -{date_end_period}\n
    Предполагаемое время работ - {estimated_working_time}\n
    '''
    for obj_scope in obj.scopework_set.all():
        template_text += f'Вид работ -{obj_scope.type_work}- Объем работ - {obj_scope.scope_of_work}\n'
    return template_text
