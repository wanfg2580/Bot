from django.db import models


class WechatMessage(models.Model):
    id = models.IntegerField('编号', primary_key=True)
    msg_id = models.CharField('微信消息编号', max_length=255)
    user_name = models.CharField('用户昵称', max_length=100)
    user_id = models.CharField('用户编号', max_length=255)
    is_group = models.BooleanField('是否是群消息')
    group_id = models.CharField('群编号', max_length=255)
    group_name = models.CharField('群名', max_length=50)
    msg_content = models.TextField('消息内容')
    created_at = models.DateField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'wxmessages'

    @staticmethod
    def add_message(msg_id, user_name, user_id, is_group, group_id, group_name, msg_content):
        WechatMessage.objects.create(msg_id=msg_id, user_name=user_name, user_id=user_id, is_group=is_group, group_id=group_id, group_name=group_name, msg_content=msg_content)

    @staticmethod
    def get_msg_list(start, end):
        return WechatMessage.objects.all()[start: end]

    @staticmethod
    def get_msg_size():
        return WechatMessage.objects.all().count()


class TeleMessage(models.Model):
    id = models.IntegerField('编号', primary_key=True)
    msg_id = models.CharField('telegram 消息编号', max_length=255)
    is_group = models.BooleanField('是否是群消息')
    group_id = models.CharField('群id,非群消息为空' , max_length=255)
    groud_name = models.CharField('群组名', max_length=255)
    group_type = models.CharField('群组类型', max_length=20)
    msg_content = models.TextField('消息内容')
    date = models.DateTimeField('消息发送时间')
