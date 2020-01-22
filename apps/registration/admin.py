from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Hybrid, Specialization, ContactPerson, Subject


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
            'card_key'
        )}),
    )


class ContactPersonAdmin(admin.ModelAdmin):
    model = ContactPerson
    list_display = ('title', 'search_name')


admin.site.register(Hybrid, MyUserAdmin)
admin.site.register(Specialization)
admin.site.register(ContactPerson, ContactPersonAdmin)
admin.site.register(Subject)
