from django.contrib import admin
from .models import User, Chat
# Register your models here.
from django.contrib.admin import display
from tbot_base.models import BotConfig
from django.utils.html import format_html


@admin.register(Chat)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ['chats',]
    list_display = ['pk', 'name', ]
    fields = ['name', 'user_id', 'username', 'get_refer', 'get_chats', 'get_refer_of']
    readonly_fields = ['name', 'user_id', 'username', 'get_refer', 'get_chats', 'get_refer_of']
    search_fields = ['user_id', 'username', 'name']

    @display(description='Рекомендація від')
    def get_refer(self, obj):
        server_url = BotConfig.objects.filter(is_active=True).first()
        if server_url:
            server_url = server_url.server_url + f'/admin/tbot/user/{obj.refer.pk}/change/'
        else:
            server_url = 1
        return format_html(
                f'<a href="{server_url}">{str(obj.refer.name) + " " + str(obj.refer.username) + " " + obj.refer.user_id}</a>'
            )

    @display(description='Чати')
    def get_chats(self, obj):
        chats = obj.chats.all()
        text = ''
        for chat in chats:
            text = text + chat.name + '\n'
        return text

    @display(description='Рекомендував')
    def get_refer_of(self, obj):
        server_url = BotConfig.objects.filter(is_active=True).first()
        users = obj.user_set.all()
        text = ''
        url = server_url.server_url + f'/admin/tbot/user/'
        for user in users:
            print(user)
            server_url = url + str(user.pk)
            print(1)
            print(f'<a href="{server_url}">{str(user.name)} {str(user.username)}</a>\n')
            text += f'<a href="{server_url}">{str(user.name)}  {str(user.username)}</a>\n\n'
        return format_html(text)