from django.contrib import admin

# Register your models here.
from .models import CakeMaker, MeetingReport, Project

admin.site.register(CakeMaker)
admin.site.register(MeetingReport)
admin.site.register(Project)