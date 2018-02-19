import os
import telegram
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework.parsers import JSONParser
from wechat_bot.models import Admin
from bot_util import wechat_util

logger = logging.getLogger('django')


class Bot(TemplateView):
    @csrf_exempt
    def init_bot(request):
        global bot
        if request.method == 'POST':
            data = JSONParser().parse(request)
            path = data.get("path")
            certificate = open(os.path.join(path), "rb")
            bot = telegram.Bot(token=data.get('token'))
            bot.set_webhook(data.get('url'), certificate=certificate)
            info = bot.get_webhook_info()
            return JsonResponse(info, status=200)

    @csrf_exempt
    def bot_info(request):
        if request.method == 'POST':
            return JsonResponse(bot.get_me(), status=200)

    @csrf_exempt
    def get_admin_list(request):
        if request.method == 'GET':
            admin_list = Admin.list_all_admin()
            response = []
            if admin_list is not None:
                for admin in admin_list:
                    admin = admin.__dict__
                    admin.pop('_state')
                    response.append(admin)
            logger.info('管理员列表：%s', response)
            return JsonResponse(response, status=200, safe=False)

    @csrf_exempt
    def add_admin(request):
        if request.method == 'POST':
            data = JSONParser().parse(request)
            name = data.get('name')
            right_level = data.get('right_level')
            status = data.get('status')
            if right_level == 0:
                Admin.add_admin(name=name, right_level=right_level, status=status)
                wechat_util.add_admin(name)
            else:
                group_name = data.get('group_name')
                Admin.add_admin(name=name, right_level=right_level, group_name=group_name, status=status)
                wechat_util.add_admin(name, group_name)
            return JsonResponse({'code': '0000'}, status=200)