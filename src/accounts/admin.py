from django.contrib import admin
from djongo.admin import ModelAdmin

from accounts.models import Comment, CustomUser, Profile

admin.site.register([Profile, Comment])


class ProfileInline(admin.StackedInline): 
    model = Profile


@admin.register(CustomUser)
class CustomUser(ModelAdmin):
    inlines = [ProfileInline]
    date_hierarchy = 'date_joined'
    ordering = ('id',)
    list_display = ('email', )
    list_display_links = ('email', )
    search_fields = ('email', )
    




