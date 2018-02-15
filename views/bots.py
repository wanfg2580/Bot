import os
import telegram
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework.parsers import JSONParser
from wechat_bot.models import Admin


class Bot(TemplateView):
    @csrf_exempt
    def init_bot(self, request):
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
    def bot_info(self, request):
        if request.method == 'POST':
            return JsonResponse(bot.get_me(), status=200)

    def add_admin(self):
        print(Admin.list_all_admin())
        return JsonResponse({'test':'test'}, status=200)