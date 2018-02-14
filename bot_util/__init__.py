import threading

import itchat
from . import wechat_util


def wechat_start():
    itchat.auto_login(True)
    itchat.run(True)
    wechat_util.do_init()


print('thread %s is running...' % threading.current_thread().name)
# t = threading.Thread(target=wechat_start, name='WechatThread')
# t.start()