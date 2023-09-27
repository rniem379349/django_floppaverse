from django.contrib import admin

from chat.models import ChatMessage, ChatRoom

admin.site.register(ChatRoom, admin.ModelAdmin)
admin.site.register(ChatMessage, admin.ModelAdmin)
