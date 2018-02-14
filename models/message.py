from django.db import models


class TeleMessage(models.Model):
    msg_id = models.CharField('telegram 消息编号', primary_key=True)
    is_group = models.BooleanField('是否是群消息')
    group_id = models.CharField('群id,非群消息为空')
    groud_name = models.CharField('群组名', max_length=255)
    group_type = models.CharField('群组类型', max_length=20)
    content = models.TextField('消息内容')
    date = models.DateTimeField('消息发送时间')


class WechatMessage(models.Model):
    msg_id = models.CharField('微信消息编号', primary_key=True)
