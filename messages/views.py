import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

logger = logging.getLogger('django')


@csrf_exempt
def snippet_list(request):
    """
    列出所有已经存在的snippet或者创建一个新的snippet
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        logger.info(data)
        return JsonResponse({'status':'ok'}, status=200)
