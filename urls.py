from django.conf.urls import url
from wechat_bot.views import bots, messages, pages

urlpatterns = [
    # Pages
    url(r'^$', pages.HomePage.as_view(), name='home-page'),
    url(r'^tele_bot/$', pages.TeleBot.as_view(), name='bot-manage'),
    url(r'^wechat_admin/$', pages.WechatAdmin.as_view(), name='bot-manage'),
    url(r'^wechat_messages/$', pages.WechatMessage.as_view(), name='bot-manage'),

    url(r'^messages/$', messages.Message.messages, name='message-url'),
    url(r'^wechat_admin/admin_list/$', bots.WechatBot.get_admin_list, name='get admin list'),
    url(r'^wechat_admin/add_admin/$', bots.WechatBot.add_admin, name='add wechat admin'),
    url(r'^wechat_admin/edit_admin/$', bots.WechatBot.edit_admin, name='edit wechat admin'),
    url(r'^wechat_admin/remove_admin/$', bots.WechatBot.remove_admin, name='edit wechat admin'),
    url(r'^wechat_admin/delete_admin/$', bots.WechatBot.delete_admin, name='delete wechat admin'),
    url(r'^wechat_admin/friends_list/$', bots.WechatBot.get_friends_list, name='delete wechat admin'),
    url(r'^wechat_admin/chatroom_list/$', bots.WechatBot.get_groups_list, name='delete wechat admin'),
]
