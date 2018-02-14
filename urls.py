from django.conf.urls import url, include
from views import messages, bots, pages

urlpatterns = [
    # Pages
    url(r'^$', pages.HomePage.as_view(), name='home-page'),
    url(r'^tele_bot/$', pages.TeleBot.as_view(), name='bot-manage'),
    url(r'^wechat_admin/$', pages.WechatAdmin.as_view(), name='bot-manage'),
    url(r'^wechat_messages/$', pages.WechatMessage.as_view(), name='bot-manage'),

    url(r'^messages/$', messages.Message.messages, name='message-url'),
    url(r'^initBot/$', bots.Bot.init_bot, name='init bot'),
]