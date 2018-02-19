from django.shortcuts import render
from .models import commite_member, referat
# Create your views here.
def index(request):
    commite_members = commite_member.objects.all()
    referats = referat.objects.all().order_by('date').reverse()


    return render(request,internside.html, {"commite_members": commite_members, "referats": referats })


def cake_list(request):

    list = commite_member.objects.all().order_by('number_on_list')


