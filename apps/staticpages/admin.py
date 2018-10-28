from django.contrib import admin

from .models import BoardReport, Protocol, Application, CommiteApplication, Ktv_report, BoardReportSemester


admin.site.register(BoardReport)
admin.site.register(Protocol)
admin.site.register(Application)
admin.site.register(CommiteApplication)
admin.site.register(Ktv_report)
admin.site.register(BoardReportSemester)
