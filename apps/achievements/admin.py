from django.contrib import admin
from apps.achievements.models import Badge, BadgeForslag, BadgeRequest
from apps.registration.models import *

class BadgeAdmin(admin.ModelAdmin):

    filter_horizontal = ('user',)
    list_display = ('name',)


# Register your models here.
admin.site.register(Badge, BadgeAdmin)
admin.site.register(BadgeForslag)
admin.site.register(BadgeRequest)

