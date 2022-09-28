from django.contrib import admin

from accounts.models import CustomUser, Comment, Profile

admin.site.register([CustomUser, Profile, Comment])
