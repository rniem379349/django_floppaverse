from django.contrib import admin

from blog.models import BlogPost, NewsletterSubscription

admin.site.register(BlogPost, admin.ModelAdmin)
admin.site.register(NewsletterSubscription, admin.ModelAdmin)
