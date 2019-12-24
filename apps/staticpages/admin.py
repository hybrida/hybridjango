from django.contrib import admin

from .models import BoardReport, Protocol, Application, CommiteApplication, Ktv_report, BoardReportSemester, Statute, Updatek

admin.site.register(BoardReport)
admin.site.register(Statute)
admin.site.register(Protocol)
admin.site.register(Application)
admin.site.register(CommiteApplication)
admin.site.register(Ktv_report)
admin.site.register(BoardReportSemester)
admin.site.register(Updatek)
