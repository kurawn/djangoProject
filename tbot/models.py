from django.db import models


class Chat(models.Model):
    name = models.CharField(verbose_name="Ім'я чату", max_length=500, blank=True, null=True)
    chat_id = models.CharField(max_length=500, blank=True, null=True)


class User(models.Model):
    user_id = models.CharField(max_length=500, verbose_name="Телеграм id", blank=True, null=True)
    username = models.CharField(max_length=500, verbose_name='Нікнайм', blank=True, null=True)
    name = models.CharField(max_length=500, verbose_name="Ім'я користувача", blank=True, null=True)
    chats = models.ManyToManyField(Chat, verbose_name='Чати', null=True, blank=True)
    refer = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        from tbot_base.bot import tbot
        for chat in self.chats.all():
            print(tbot.kick_chat_member(chat_id=chat.chat_id, user_id=self.user_id))
        for user in self.user_set.all():
            user.delete()
        super().delete(using, keep_parents)
