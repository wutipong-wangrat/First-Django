from django.contrib import admin
from usersapp.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "image"]


# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
