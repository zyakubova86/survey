from django.db import models


# Create your models here.
class Message(models.Model):
    name = models.CharField(max_length=200, null=True, verbose_name='Имя')
    department = models.CharField(max_length=200, null=True, verbose_name='Отдел')
    phone = models.CharField(max_length=200, null=True, verbose_name='Телефон')
    msg_text = models.TextField(verbose_name='Жалоба или предложение')
    created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата')

    class Meta:
        verbose_name = "Жалоба или предложение"
        verbose_name_plural = 'Жалобы или предложения'
