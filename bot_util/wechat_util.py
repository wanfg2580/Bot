# coding=utf-8
import logging
import re
import itchat
from itchat.content import TEXT
from wechat_bot.models import Admin

logger = logging.getLogger('django')

invite_ptn = re.compile(r'邀请"(.*?)"加入了群聊')
newfriend_ptn1 = re.compile(r'(.*?)刚刚把你添加到通讯录，现在可以开始聊天了。')
newfriend_ptn2 = re.compile(r'你已添加了(.*?)，现在可以开始聊天了。')

target_admin_objs = []
target_admin_uns = {}


def do_init():
    """
    初始化管理员管理级别
    :return:
    """
    global target_admin_objs, target_admin_uns
    logger.info('init target Admins and Groups...')
    admin_list = Admin.list_all_admin()

    if admin_list is not None:
        for admin in admin_list:
            admin_dict = admin.__dict__
            admin_info = itchat.search_friends(nickName=admin_dict['name'])
            group_info = itchat.search_chatrooms(admin_dict['group_name']) if admin_dict['group_name'] is not None else []
            target_admin_uns[admin_info[0]['UserName']] = []
            target_admin_uns[admin_info[0]['UserName']].append(group_info[0]['UserName'] if len(group_info) > 0 else '0')

    logger.info('初始化管理员[%s人]成功！' % (len(target_admin_uns)))


def handle_admin_operation(msg):
    """
    处理管理员命令
    :param msg:
    :return: 踢人结束发送消息
    """
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


def add_admin(nick_name, group_name=0):
    """
    添加管理员
    :param nick_name: 管理员昵称
    :param group_name: 群名
    :return:
    """
    admin_info = itchat.search_friends(nickName=nick_name)
    if admin_info[0]['UserName'] not in target_admin_uns.keys():
        target_admin_uns[admin_info[0]['UserName']] = []
    if group_name != 0:
        group_info = itchat.search_chatrooms(group_name)
        target_admin_uns[admin_info[0]['UserName']].append(group_info[0]['UserName'])
    else:
        target_admin_uns[admin_info[0]['UserName']].append('0')


# 群消息
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    logger.info('[%s@%s\t]:%s' % (
        msg['ActualNickName'], itchat.search_chatrooms(userName=msg['FromUserName'])['NickName'], msg['Text']))
    if msg['ActualUserName'] in target_admin_uns.keys() \
            and (msg['FromUserName'] in target_admin_uns[msg['ActualUserName']]
                 or '0' in target_admin_uns[msg['ActualUserName']]):
        logger.info('处理管理员消息')
        return handle_admin_operation(msg)
