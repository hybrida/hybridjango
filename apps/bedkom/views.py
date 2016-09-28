from django.http import HttpResponse
from django.shortcuts import render
from .models import Bedrift

# Create your views here.

bedrifter = [
    Bedrift("Norconsult", "Jonas", "Anna Malmø", "Heihei, detter er en veldig lang kommentar"),
    Bedrift("Norconsult", "Jonas", "Anna Malmø", "Heihei, detter er en veldig lang kommentar"),
    Bedrift("Norconsult", "Jonas", "Anna Malmø", "Heihei, detter er en veldig lang kommentar"),
    Bedrift("Norconsult", "Jonas", "Anna Malmø", "Heihei, detter er en veldig lang kommentar"),
    Bedrift("Norconsult", "Jonas", "Anna Malmø", "Heihei, detter er en veldig lang kommentar"),
    Bedrift("Norconsult", "Jonas", "Anna Malmø", "Heihei, detter er en veldig lang kommentar"),

]


def index(request):
    if(request in bedrifter):
        print(request.GET["ansvarlig"])
    return render(request, "bedkom/bedrifter.html", {"bedrifter": bedrifter})
