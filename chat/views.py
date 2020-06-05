from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
import logging
logger = logging.getLogger("django")  # 为loggers中定义的名称

def index(request):
    logger.info('get 33  shopItems')
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    logger.info('get shopItems.....')
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })