from django.db import models


class Admin:
    id = models.IntegerField('编号', primary_key=True)
    name = models.CharField('管理员姓名')
    right_level = models.IntegerField('权限等级，0为全局管理员，1为单群管理员')
    group_name = models.CharField('该管理员管理群组名，全局管理员为空')
    status = models.IntegerField('管理员状态，0可用，-1不可用')
    position = models.IntegerField('优先级位置')
    create_time = models.DateField('创建时间')
    modify_time = models.DateField('修改时间')
