from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = "index.html"


class TeleBot(TemplateView):
    template_name = "bots/tele-bot.html"


class WechatAdmin(TemplateView):
    template_name = "bots/wechat-admin.html"


class WechatMessage(TemplateView):
    template_name = "bots/wechat-messages.html"
