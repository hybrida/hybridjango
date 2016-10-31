from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Hybrid


class MyUserAdmin(UserAdmin):
    model = Hybrid

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': (
            'middle_name',
            'member',
            'graduation_year',
            'image',
            'gender',
            'specialization',
            'date_of_birth',
            'title',
        )}),
    )

admin.site.register(Hybrid, MyUserAdmin)
