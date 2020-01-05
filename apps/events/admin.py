from django.contrib import admin
import nested_admin

from apps.bedkom.models import Bedpress
from .models import EventType, Event, Attendance, Participation, ParticipationSecondary, Mark, MarkPunishment, Delay, \
    Rule, TPEvent


class ParticipationInline(nested_admin.NestedTabularInline):
    model = Participation


class ParticipationSecondaryInline(nested_admin.NestedTabularInline):
    model = ParticipationSecondary


class AttendanceAdmin(nested_admin.NestedModelAdmin):
    model = Attendance
    filter_horizontal = ('participants', 'participantsSecondary', 'specializations')
    inlines = [
        ParticipationInline,
        ParticipationSecondaryInline,
    ]


class AttendanceInline(nested_admin.NestedStackedInline):
    model = Attendance
    filter_horizontal = ('participants', 'participantsSecondary', 'specializations', 'groups')
    inlines = [
        ParticipationInline,
        ParticipationSecondaryInline,
    ]
    extra = 0


class BedpressInline(nested_admin.NestedTabularInline):
    model = Bedpress
    extra = 0


class EventAdmin(nested_admin.NestedModelAdmin):
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
    exclude = ('delay', 'rules',)


admin.site.register(EventType)
admin.site.register(Event, EventAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Mark)
admin.site.register(MarkPunishment, MarkPunishmentAdmin)
admin.site.register(TPEvent)
