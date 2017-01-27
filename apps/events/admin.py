from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    filter_horizontal = ('participants',)

admin.site.register(Event, EventAdmin)
