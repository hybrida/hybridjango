from django.contrib import admin
from .models import Company, CompanyComment, Bedpress, Contact_person

admin.site.register(Company)
admin.site.register(CompanyComment)
admin.site.register(Bedpress)
admin.site.register(Contact_person)