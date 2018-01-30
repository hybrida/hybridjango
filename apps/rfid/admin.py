from django.contrib import admin

from .models import Appearances, GeneralAssembly


class AppearancesAdmin(admin.ModelAdmin):
    filter_horizontal = ('users',)


class GeneralAssemblyAdmin(admin.ModelAdmin):
    filter_horizontal = ('users',)


admin.site.register(Appearances, AppearancesAdmin)
admin.site.register(GeneralAssembly, GeneralAssemblyAdmin)

