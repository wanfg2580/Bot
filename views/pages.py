from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = "index.html"


class BotManage(TemplateView):
    template_name = "bots/bot-manage.html"