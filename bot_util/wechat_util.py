# coding=utf-8
import logging
import re
import itchat
from itchat.content import TEXT
from wechat_bot.models import Admin
from wechat_bot.models import WechatMessage

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
            if admin.status == 0:
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


def add_admin(user_id, group_id=0):
    """
    添加管理员
    :param nick_id: 管理员编号
    :param group_id: 群编号
    :return:
    """
    if user_id not in target_admin_uns.keys():
        target_admin_uns[user_id] = []
    if group_id != 0:
        target_admin_uns[user_id].append(group_id)
    else:
        target_admin_uns[user_id].append('0')
    return True


def remove_admin(nick_name):
    """
    移除管理员信息
    :param nick_name: 昵称
    :param group_name: 群名
    :return:
    """
    admin_info = itchat.search_friends(nickName=nick_name)
    if len(admin_info) <= 0:
        return False
    if admin_info[0]['UserName'] in target_admin_uns.keys():
        target_admin_uns.pop(admin_info[0]['UserName'])
        return True
    else:
        return False


def get_friends_list():
    friend_list = itchat.get_friends()
    result = []
    for friend in friend_list:
        wechat_friend = {'UserName': friend['UserName'], 'NickName': friend['NickName']}
        result.append(wechat_friend)
    return result


def get_groups_list():
    chatroom_list = itchat.get_chatrooms()
    groups_result = []
    for chatroom in chatroom_list:
        wechat_friend = {'UserName': chatroom['UserName'], 'NickName': chatroom['NickName']}
        groups_result.append(wechat_friend)
    return groups_result


# 群消息
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    group_name = itchat.search_chatrooms(userName=msg['FromUserName'])['NickName']
    logger.info('[%s@%s\t]:%s' % (
        msg['ActualNickName'], group_name, msg['Text']))

    WechatMessage.add_message(msg_id=msg['NewMsgId'], user_name=msg['ActualNickName'], user_id=msg['ToUserName'], is_group=True,
                              group_id=msg['FromUserName'], group_name=group_name, msg_content=msg['Text'])

    if msg['ActualUserName'] in target_admin_uns.keys() \
            and (msg['FromUserName'] in target_admin_uns[msg['ActualUserName']]
                 or '0' in target_admin_uns[msg['ActualUserName']]):
        logger.info('处理管理员消息')
        return handle_admin_operation(msg)
