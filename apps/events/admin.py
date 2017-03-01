from django.contrib import admin

from apps.bedkom.models import Bedpress
from .models import Event, Attendance


class AttendanceInline(admin.StackedInline):
    model = Attendance
    filter_horizontal = ('participants', 'specializations')
    extra = 0


class BedpressInline(admin.TabularInline):
    model = Bedpress
    extra = 0


class EventAdmin(admin.ModelAdmin):
    inlines = [
        AttendanceInline,
        BedpressInline,
    ]


admin.site.register(Event, EventAdmin)
