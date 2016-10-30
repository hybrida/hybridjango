from django.contrib import admin
from .models import Company, CompanyComment, EarlierBedpresses, Bedpress

admin.site.register(Company)
admin.site.register(CompanyComment)
admin.site.register(EarlierBedpresses)
admin.site.register(Bedpress)