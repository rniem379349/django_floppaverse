from django.contrib import admin

from users.models import Profile, UserReport

admin.site.register(Profile, admin.ModelAdmin)
admin.site.register(UserReport, admin.ModelAdmin)
