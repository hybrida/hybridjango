from django.contrib import admin
from .models import Course, Evaluation


# Register your models here.
admin.site.register(Evaluation)
admin.site.register(Course)