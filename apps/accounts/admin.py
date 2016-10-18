from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from apps.accounts.models import Hybrid


class UserInline(admin.TabularInline):
    model = Hybrid
    fk_name = 'user'
    can_delete = False
    max_num = 1
    verbose_name_plural = 'extra'


class HybUser(UserAdmin):
    inlines = (UserInline,)


admin.site.unregister(User)
admin.site.register(User, HybUser)
