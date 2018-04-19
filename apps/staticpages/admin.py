from django.contrib import admin

from .models import BoardReport, Protocol, Application, ComApplication

admin.site.register(BoardReport)
admin.site.register(Protocol)
admin.site.register(Application)
admin.site.register(ComApplication)
