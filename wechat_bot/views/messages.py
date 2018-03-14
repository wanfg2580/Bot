import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from wechat_bot.models import WechatMessage

logger = logging.getLogger('django')


class Message:
    @csrf_exempt
    def messages(request):
        """
        提供给telegram的webhook
        :return:
        """
        if request.method == 'POST':
            data = JSONParser().parse(request)
            logger.info(data)
            return JsonResponse({'status': 'ok'}, status=200)

    @csrf_exempt
    def get_wechat_messages(request):
        """
        获取消息列表
        :return:
        """
        if request.method == 'GET':
            page = int(request.GET['id'])
            page_size = int(request.GET['page_size'])
            group_id = request.GET['group_id']
            start = page_size * (page - 1)
            end = page_size * page
            if group_id is '0':
                msg_list = WechatMessage.get_msg_list(start=start, end=end)
                msg_size = WechatMessage.get_msg_size()
            else:
                msg_list = WechatMessage.get_group_message(group_id=group_id, start=start, end=end)
                msg_size = WechatMessage.get_group_msg_size(group_id=group_id)
            max_length = msg_size / page_size
            response = []
            if msg_list is not None:
                for admin in msg_list:
                    admin = admin.__dict__
                    admin.pop('_state')
                    response.append(admin)
            return JsonResponse({'code': '0000', 'msg_list': response, 'size': max_length}, status=200)

    @csrf_exempt
    def get_message_group(request):
        """
        获取消息群组列表
        :return:
        """
        if request.method == 'GET':
            group_list = WechatMessage.get_group_list()
            response = []
            if group_list is not None:
                for group in group_list:
                    response.append(group)
            return JsonResponse({'code': '0000', 'group_list': response}, status=200)
