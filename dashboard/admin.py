from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.profile_picture:
            return format_html(
                '<img src="{}" width="30" style="border-radius:50%;">'.format(
                    object.profile_picture.url
                )
            )
        return None

    thumbnail.short_description = 'عکس پروفایل'
    list_display = ('user', 'thumbnail', 'city', 'state')


admin.site.register(UserProfile, UserProfileAdmin)
