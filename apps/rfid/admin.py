from django.contrib import admin

from .models import Appearances

class AppearancesAdmin(admin.ModelAdmin):
    filter_horizontal = ('users',)


admin.site.register(Appearances, AppearancesAdmin)
