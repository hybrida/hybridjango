from django.contrib import admin

from apps.bedkom.models import Bedpress
from .models import Event, Attendance, Participation


class ParticipationInline(admin.TabularInline):
    model = Participation


class AttendanceAdmin(admin.ModelAdmin):
    model = Attendance
    filter_horizontal = ('participants', 'specializations')
    inlines = [
        ParticipationInline,
    ]


class AttendanceInline(admin.StackedInline):
    model = Attendance
    filter_horizontal = ('participants', 'specializations')  # TODO: participants won't show up
    extra = 0


class BedpressInline(admin.TabularInline):
    model = Bedpress
    extra = 0


class EventAdmin(admin.ModelAdmin):
    inlines = [
        AttendanceInline,
        BedpressInline,
    ]
    exclude = ('timestamp',)



admin.site.register(Event, EventAdmin)
admin.site.register(Attendance, AttendanceAdmin)
