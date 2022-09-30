from django.contrib import admin

from accounts.models import Comment, CustomUser, Profile

admin.site.register([CustomUser, Profile, Comment])
