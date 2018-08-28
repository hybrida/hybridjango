from django.contrib import admin

from .models import BoardReport, Protocol, Application, CommiteApplication

admin.site.register(BoardReport)
admin.site.register(Protocol)
admin.site.register(Application)
admin.site.register(CommiteApplication)
