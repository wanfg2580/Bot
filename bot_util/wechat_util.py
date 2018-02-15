# coding=utf-8
import logging
import re
import time

import itchat

from itchat.content import *

from wechat_bot.models import Admin

logger = logging.getLogger('django')

admin_names = ['DVN榕树网络-微信小秘书', 'Norman', '小明同学', '鸡腿真好吃', '高瑞鑫']
target_admin_objs = []
target_admin_uns = []
admin_info_dic = {}
group_names = ['BBN-Fans-Team-No.1', 'BBN-Fans-Team-No.2', 'BBN-Fans-Team-No.3',
               'BBN-Fans-Team-No.4', 'BBN-Fans-Team-No.5', 'BBN-Fans-Team-No.6',
               'BBN-Fans-Team-No.7', 'BBN-Fans-Team-No.8', 'BBN-Fans-Team-No.9',
               'BBN-Fans-Team-No.10', 'BBN-Fans-Team-No.11', 'BBN-Fans-Team-No.12',
               'BBN-Fans-Team-No.13', 'BBN-Fans-Team-No.14', 'BBN-Fans-Team-No.15']
target_group_objs = []
target_group_uns = []
group_info_dic = {}

invite_ptn = re.compile(r'邀请"(.*?)"加入了群聊')
newfriend_ptn1 = re.compile(r'(.*?)刚刚把你添加到通讯录，现在可以开始聊天了。')
newfriend_ptn2 = re.compile(r'你已添加了(.*?)，现在可以开始聊天了。')


# 群消息
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    logger.info('[%s@%s\t]:%s' % (
        msg['ActualNickName'], itchat.search_chatrooms(userName=msg['FromUserName'])['NickName'], msg['Text']))
    if msg['ActualUserName'] in target_admin_uns:
        logger.info('处理管理员消息')
        return handle_admin_operation(msg)

    # 如果是目标群
    # if msg['FromUserName'] in target_group_uns:
    #     # TODO 对目标群进行操作
    #     if msg['ActualUserName'] in target_admin_uns:
    #         logger.info('处理管理员消息')
    #         return handle_admin_operation(msg)
    # elif msg['IsAt']:
    #     # TODO 其他群@我的消息
    #     pass
    # else:
    #     # TODO 其他群未@我的消息
    #     pass
    # elif '@' in msg['T']:


# 群通知
@itchat.msg_register(NOTE, isGroupChat=True)
def group_note(msg):
    # 如果是目标群
    if msg['FromUserName'] in target_group_uns:
        data = msg['Text']
        invite = invite_ptn.search(data)
        if invite:
            # a = invite.group(1)  # 邀请人名字
            time.sleep(2)
            b = invite.group(1)  # 被邀请人名字
            # TODO update group list
            return '欢迎@%s\u2005加入榕树~ 榕树网络' \
                   '是全球首个由大数据领域资深团队' \
                   '及行业参与者共建的分布式数据经济生态。' \
                   '点击直达官网，深度了解榕树：' \
                   'http://www.banyanbbt.org/ ' % b


# 个人系统消息
# @itchat.msg_register(NOTE)
# def person_note(msg):
#     # 处理新加朋友消息
#     if msg['Text'].endswith('聊天了。'):
#         handle_new_friend(msg)


def do_init():
    global target_admin_objs, target_group_objs, target_admin_uns, target_group_uns
    logger.info('init target Admins and Groups...')
    admin_list = Admin.list_all_admin()

    if admin_list is not None:
        for admin in admin_list:
            admin_dict = admin.__dict__
            print(admin_dict)
            print(admin_dict['name'])
    # for admin in admin_names:
    #     target_admin_objs += itchat.search_friends(admin)
    # target_admin_uns = [admin['UserName'] for admin in target_admin_objs]
    # for group in group_names:
    #     target_group_objs += itchat.search_chatrooms(group)
    # target_group_uns = [group['UserName'] for group in target_group_objs]

    logger.info('初始化管理员[%s人]&群[%s个]成功！' % (len(target_admin_uns), len(target_group_uns)))
    logger.info('%s' % repr([group['NickName'] for group in target_group_objs]))

    # itchat.update_chatroom(target_group_uns)
    logger.info('Update群员信息成功！')


def handle_admin_operation(msg):
    text = msg['Text']
    logger.info('开始犹豫管理员消息中是否含有命令...')
    # if msg['Text'].endswith('踢'):
    ti_ptn = re.search(r'^@(.*?).bbn$', text)
    if ti_ptn:
        kickee = ti_ptn.group(1)
        logger.info('已确认是踢人操作，被踢人：%s.' % kickee)
        ml = msg['User']['MemberList'] if msg['User'].get('MemberList') else []
        for member in ml:
            if member['NickName'] == kickee:
                result = itchat.delete_member_from_chatroom(msg['FromUserName'], [member])
                if result['BaseResponse']['Ret'] == 0:
                    return '\U0001f333%s,亲，系统记录到您违反社区规则，将被暂时移除列入广告灰名单,无法获取榕树最新信息哦~多谢亲们的理解。' % kickee
                    # return '太可惜了，本群永远失去了%s～' % kickee
    # if text.lstrip().startswith('\U0001f333\U0001f333\U0001f333'):
    #     logger.info '已确认是多群群发，正在发送中...'
    #     for i in target_group_uns:
    #         itchat.send(msg=text, toUserName=i)
    #         time.sleep(random.randint(6, 10))
    #     logger.info '发送结束'
    #     return '多群发送结束，小榕给您按摩按摩，辛苦啦么么哒～'
    # logger.info '好吧，没有命令。。。'

# if __name__ == '__main__':
#     init()