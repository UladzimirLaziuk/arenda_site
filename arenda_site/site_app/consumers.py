import datetime
import json

from asgiref.sync import sync_to_async
from channels.consumer import AsyncConsumer
from site_app.models import Renter
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class EchoConsumerAsync(AsyncConsumer):

    async def websocket_connect(self, event):
        logger.error('websocket_connect')
        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        logger.info('websocket_receive')
        text_data_json = json.loads(event['text'])
        if text_data_json.get("message"):
            message = text_data_json["message"]
            logger.info('message %s' % message)
        else:
            logger.info('message None')
            message = None
        datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ads_title, index = await query_asinc(message)
        text_data = json.dumps({
            'message': ads_title,
            'index': index,
            'time_massage': datetime_str,
        })
        await self.send({
            "type": "websocket.send",
            "text": text_data,
        })


@sync_to_async
def query_asinc(data_message):
    # queryset = Renter.objects.filter(title__icontains=data_message).values_list('title', 'id')
    queryset = Renter.objects.all()
    index = ''
    if not queryset:
        return None, None
    ads_title = queryset.first().name_organization
    return ads_title, index
