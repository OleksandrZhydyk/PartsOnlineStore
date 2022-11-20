from django.contrib import admin
from django.utils.html import format_html
from djongo.admin import ModelAdmin

from accounts.models import Comment, CustomUser, Profile


class ProfileInlineAdmin(admin.StackedInline):
    model = Profile


@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    inlines = [ProfileInlineAdmin]
    date_hierarchy = "date_joined"
    ordering = ("id",)
    list_display = ("email",)
    list_display_links = ("email",)
    search_fields = ("email",)


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    date_hierarchy = "date_created"
    ordering = ("date_created",)
    list_display = ("avatar", "email", "first_name", "last_name", "phone_number", "address")
    list_display_links = ("avatar",)
    search_fields = ("email", "phone_number", "last_name", "first_name", "address")

    def avatar(self, obj):
        if obj.photo:
            photo = f"<img src='{obj.photo.url}' style='width:150px;height:150px;' alt='Avatar'>"
            return format_html(photo)
        return "No avatar"


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    date_hierarchy = "created"
    ordering = ("created",)
    list_display = ("created", "user", "part")
    list_display_links = ("created",)
    search_fields = ("created", "user", "part")
