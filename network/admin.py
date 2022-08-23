from django.contrib import admin

from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email", "show_followers", "show_following", "show_liked_posts"]

class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "post_content", "creation_date"]

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)