from django.contrib import admin

# Register your models here.

from .models import Bubble, Tag, Account, Comment

admin.site.register(Bubble)
admin.site.register(Tag)
admin.site.register(Account)
admin.site.register(Comment)
