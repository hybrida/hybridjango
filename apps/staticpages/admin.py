from django.contrib import admin

from .models import BoardReport, Protocol, Application

admin.site.register(BoardReport)
admin.site.register(Protocol)
admin.site.register(Application)
