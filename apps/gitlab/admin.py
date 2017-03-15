from django.contrib import admin

from .models import GitlabToken


admin.site.register(GitlabToken, admin.ModelAdmin)
