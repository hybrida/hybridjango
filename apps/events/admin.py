from django.contrib import admin

from apps.bedkom.models import Bedpress
from .models import EventType, Event, Attendance, Participation, ParticipationSecondary, Mark, MarkPunishment, Delay, Rule, TPEvent


class ParticipationInline(admin.TabularInline):
    model = Participation


class ParticipationSecondaryInline(admin.TabularInline):
    model = ParticipationSecondary


class AttendanceAdmin(admin.ModelAdmin):
    model = Attendance
    filter_horizontal = ('participants', 'specializations')
    inlines = [
        ParticipationInline,
        ParticipationSecondaryInline,
    ]


class AttendanceInline(admin.StackedInline):
    model = Attendance
    filter_horizontal = ('participants', 'specializations', 'groups')  # TODO: participants won't show up
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


class DelayInline(admin.TabularInline):
    model = Delay


class RuleInline(admin.TabularInline):
    model = Rule


class MarkPunishmentAdmin(admin.ModelAdmin):
    inlines = [
        DelayInline,
        RuleInline,
    ]
    exclude = ('delay', 'rules', )


admin.site.register(EventType)
admin.site.register(Event, EventAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Mark)
admin.site.register(MarkPunishment, MarkPunishmentAdmin)
admin.site.register(TPEvent)
