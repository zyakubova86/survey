from django.urls import path
from mainapp.views import *

urlpatterns = [
    path('', index, name='index_uz'),
    path('ru/', index, name='index_ru'),
    path('message/', message, name='message'),
    path('thank-you/', thank_you, name='thank_you_uz'),
    path('ru/thank-you/', thank_you, name='thank_you_ru'),
    # path('admin/', admin, name='admin'),
    # path('admin/auth/', admin_auth, name='admin_auth'),
]
