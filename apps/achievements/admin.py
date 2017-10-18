from django.contrib import admin
from apps.achievements.models import Badge, Prerequisites

# Register your models here.
admin.site.register(Badge)
admin.site.register(Prerequisites)
