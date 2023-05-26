from django.contrib import admin
from .models import Message
from django.conf.locale.es import formats as es_formats


# Register your models here.
@admin.register(Message)
class PortalAdmin(admin.ModelAdmin):

    def date_time_display(self, obj):
        return obj.created.strftime("%d-%m-%Y %H:%M")

    date_time_display.short_description = 'Дата'

    list_display = ('name', 'department', 'phone', 'msg_text', 'created')
    list_filter = ('name', "department", 'created')

    class Meta:
        ordering = ('-created',)
        verbose_name = "Портал"
        verbose_name_plural = "Портал"
