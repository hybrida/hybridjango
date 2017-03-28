from django.contrib import admin

from .models import Appearances

admin.site.register(Appearances, admin.ModelAdmin)
