import os
import telegram
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser


class Bot:
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