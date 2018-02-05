from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

import logging

logger = logging.getLogger('default')


@csrf_exempt
def snippet_list(request):
    """
    列出所有已经存在的snippet或者创建一个新的snippet
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        logging.warning(data)
        return JsonResponse({'test':'test'}, status=400)
