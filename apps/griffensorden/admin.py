from django.contrib import admin
from .models import Ridder, Honary_member


# classes for customization on the admin pages
class RidderAdmin(admin.ModelAdmin):

    fields = ['hybrid','finished','awarded','description']
    list_display = ('hybrid', 'awarded')
        #need a full name viewing function


# Register your models here.
admin.site.register(Ridder, RidderAdmin)
admin.site.register(Honary_member)