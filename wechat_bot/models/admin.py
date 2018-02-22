from django.db import models


class Admin(models.Model):
    id = models.IntegerField('编号', primary_key=True)
    name = models.CharField('管理员昵称', max_length=255)
    right_level = models.IntegerField('权限等级，0为全局管理员，1为单群管理员')
    group_name = models.CharField('该管理员管理群组名，全局管理员为空', max_length=255)
    status = models.IntegerField('管理员状态，0可用，-1不可用')
    created_at = models.DateField('创建时间', auto_now_add=True)
    updated_at = models.DateField('修改时间', auto_now_add=True)

    class Meta:
        db_table = 'wxadmins'

    @staticmethod
    def list_all_admin():
        return Admin.objects.all()

    @staticmethod
    def add_admin(name, right_level, group_name=None, status=0):
        return Admin.objects.create(name=name, right_level=right_level, group_name=group_name, status=status)

    @staticmethod
    def change_status(id, status):
        return Admin.objects.filter(id=id).update(status=status)

    @staticmethod
    def update_admin(id, name, right_level, group_name=None, status=0):
        return Admin.objects.filter(id=id).update(name=name, right_level=right_level, group_name=group_name, status=status)

    @staticmethod
    def find_by_id(id):
        return Admin.objects.filter(id=id).first()