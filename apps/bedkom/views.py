from django.http import HttpResponse
from django.shortcuts import render
from .models import Company, CompanyComment


def index(request):
    companies = Company.objects.all()
    for company in companies:
        company.last_comment = company.companycomment_set.order_by('timestamp').last()
    return render(request, "bedkom/bedrifter.html", {"companies": companies})
