from .message import *
from .admin import *

import threading
import itchat
from bot_util import wechat_util


def wechat_start():
    itchat.auto_login(True)
    itchat.run(True)
    wechat_util.do_init()


print('thread %s is running...' % threading.current_thread().name)
# t = threading.Thread(target=wechat_start, name='WechatThread')
# t.start()
wechat_util.do_init()