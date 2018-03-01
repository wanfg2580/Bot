import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

logger = logging.getLogger('django')


class Message:
    @csrf_exempt
    def messages(request):
        if request.method == 'POST':
            data = JSONParser().parse(request)
            logger.info(data)
            return JsonResponse({'status': 'ok'}, status=200)
