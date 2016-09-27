from django.http import HttpResponse
from django.shortcuts import render
from .models import Bedrift

# Create your views here.

bedrifter = [
    Bedrift("Norconsult", "Jonas", "Anna Malmø"),
    Bedrift("Norconsult", "Jonas", "Anna Malmø"),
    Bedrift("Norconsult", "Jonas", "Anna Malmø"),
    Bedrift("Norconsult", "Jonas", "Anna Malmø"),
    Bedrift("Norconsult", "Jonas", "Anna Malmø"),
]


def index(request):
    if(request in bedrifter):
        print(request.GET["ansvarlig"])
    return render(request, "bedkom/bedrifter.html", {"bedrifter": bedrifter})
