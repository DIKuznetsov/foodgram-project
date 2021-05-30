from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'username',)
    fieldsets = (
        (None,
         {'fields': (
             'email', 'username', 'role')}),
    )


admin.site.register(User, UserAdminConfig)
