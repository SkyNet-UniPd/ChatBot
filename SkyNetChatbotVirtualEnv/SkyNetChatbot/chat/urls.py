from django.urls import re_path
from django.contrib import admin
from chat.views import ChatterBotApiView

urlpatterns = [
    re_path(r'^admin/', admin.site.urls, name='admin'),
    re_path(r'^api/chatterbot/', ChatterBotApiView.as_view(), name='chatterbot'),
]