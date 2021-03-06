import logging
import telegram
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework.parsers import JSONParser
from wechat_bot.models import Admin
from bot_util import wechat_util

logger = logging.getLogger('django')


class WechatBot(TemplateView):
    @csrf_exempt
    def get_admin_list(request):
        """
        获取管理员列表
        :return:
        """
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
        """
        添加管理员信息
        :return:
        """
        if request.method == 'POST':
            data = JSONParser().parse(request)
            name = data.get('name')
            right_level = data.get('right_level')
            status = data.get('status')
            if right_level == 0:
                if wechat_util.add_admin(name):
                    Admin.add_admin(name=name, right_level=right_level, status=status)
                else:
                    return JsonResponse({'code': '0001'}, status=200)
            else:
                group_name = data.get('group_name')
                if wechat_util.add_admin(name, group_name):
                    Admin.add_admin(name=name, right_level=right_level, group_name=group_name, status=status)
                else:
                    return JsonResponse({'code': '0001'}, status=200)
            return JsonResponse({'code': '0000'}, status=200)

    @csrf_exempt
    def edit_admin(request):
        """
        修改管理员信息
        :return:
        """
        if request.method == 'POST':
            data = JSONParser().parse(request)
            id = data.get('id')
            name = data.get('name')
            right_level = data.get('right_level')
            status = data.get('status')
            wechat_util.remove_admin(name)
            if status == -1:
                return JsonResponse({'code': '0000'}, status=200)
            if right_level == 0:
                if wechat_util.add_admin(name):
                    Admin.update_admin(id=id, name=name, right_level=right_level, status=status)
                else:
                    return JsonResponse({'code': '0001'}, status=200)
            else:
                group_name = data.get('group_name')
                if wechat_util.add_admin(name, group_name):
                    Admin.update_admin(id=id, name=name, right_level=right_level, group_name=group_name, status=status)
                else:
                    return JsonResponse({'code': '0001'}, status=200)
        return JsonResponse({'code': '0000'}, status=200)

    @csrf_exempt
    def remove_admin(request):
        """
        关停管理员
        :return:
        """
        if request.method == 'GET':
            admin = Admin.find_by_id(request.GET['id'])
            if wechat_util.remove_admin(admin.name):
                logger.info('禁止管理员%s操作成功', admin.name)
                Admin.change_status(request.GET['id'], -1)
                return JsonResponse({'code': '0000'}, status=200)
            else:
                logger.info('禁止管理员%s操作失败', admin.name)
                return JsonResponse({'code': '0001'}, status=200)

    @csrf_exempt
    def delete_admin(request):
        """
        删除管理员
        :return:
        """
        if request.method == 'GET':
            admin = Admin.find_by_id(request.GET['id'])
            if wechat_util.remove_admin(admin.name) or admin.status:
                Admin.delete_by_id(request.GET['id'])
                logger.info('删除管理员%s操作成功', admin.name)
                return JsonResponse({'code': '0000'}, status=200)
            else:
                logger.info('删除管理员%s操作失败', admin.name)
                return JsonResponse({'code': '0001'}, status=200)

    @csrf_exempt
    def get_friends_list(request):
        """
        获取好友列表
        :return:
        """
        if request.method == 'GET':
            return JsonResponse({'code': '0000', 'data': wechat_util.get_friends_list()}, status=200)

    @csrf_exempt
    def get_groups_list(request):
        """
        获取群组列表
        :return:
        """
        if request.method == 'GET':
            return JsonResponse({'code': '0000', 'data': wechat_util.get_groups_list()}, status=200)


class TelegramBot:

    @csrf_exempt
    def bot_info(request):
        telegram_bot = telegram.Bot(settings.TOKEN)
        if request.method == 'POST':
            return JsonResponse(TelegramBot.telegram_bot.get_me(), status=200)