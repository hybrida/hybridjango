from django.contrib import admin

# Register your models here.
from .models import commite_member, referat

admin.site.register(commite_member)
admin.site.register(referat)
