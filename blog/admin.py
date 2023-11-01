from django.contrib import admin
from blog.models import UserMedia, Post, Comment

# Register your models here.

admin.site.register(UserMedia)
admin.site.register(Post)
admin.site.register(Comment)