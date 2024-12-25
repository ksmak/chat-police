from django.contrib import admin

from .models import Chat, Message, Reader, OnlineUser

admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Reader)
admin.site.register(OnlineUser)
