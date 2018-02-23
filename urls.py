from django.conf.urls import url
from wechat_bot.views import bots, messages, pages

urlpatterns = [
    # Pages
    url(r'^$', pages.HomePage.as_view(), name='home-page'),
    url(r'^tele_bot/$', pages.TeleBot.as_view(), name='bot-manage'),
    url(r'^wechat_admin/$', pages.WechatAdmin.as_view(), name='bot-manage'),
    url(r'^wechat_messages/$', pages.WechatMessage.as_view(), name='bot-manage'),

    url(r'^messages/$', messages.Message.messages, name='message-url'),
    url(r'^initBot/$', bots.Bot.init_bot, name='init bot'),
    url(r'^wechat_admin/admin_list/$', bots.Bot.get_admin_list, name='get admin list'),
    url(r'^wechat_admin/add_admin/$', bots.Bot.add_admin, name='add wechat admin'),
    url(r'^wechat_admin/edit_admin/$', bots.Bot.edit_admin, name='edit wechat admin'),
    url(r'^wechat_admin/remove_admin/$', bots.Bot.remove_admin, name='edit wechat admin'),
    url(r'^wechat_admin/delete_admin/$', bots.Bot.delete_admin, name='edit wechat admin'),
]
