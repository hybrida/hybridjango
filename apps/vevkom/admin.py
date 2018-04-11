from django.contrib import admin

# Register your models here.
from .models import CakeMaker, MeetingReport, Project, Guide

admin.site.register(CakeMaker)
admin.site.register(MeetingReport)
admin.site.register(Project)
admin.site.register(Guide)
