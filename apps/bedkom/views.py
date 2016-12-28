
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import DateField
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from apps.bedkom.forms import CompanyForm
from apps.events.models import Event
from .models import Company, CompanyComment, Bedpress


def index(request):
    companies = Company.objects.all()
    for company in companies:
        company.last_comment = company.companycomment_set.order_by('timestamp').last()
    return render(request, "bedkom/bedrifter.html", {"companies": companies})


def bedrift(request, pk):
    companies = Company.objects.all()
    bedpresses = Bedpress.objects.filter(company_id=pk)
    return render(request, "bedkom/bedrift.html", {"company": companies.get(pk=pk), "bedpresses": bedpresses})


def comment(request, pk):
    companies = Company.objects.all()
    for company in companies:
        company.last_comment = company.companycomment_set.order_by('timestamp').last()
    return render(request, "bedkom/bedrifter.html", {"companies": companies})


def bedpress(request, pk):
    bedpresses = Bedpress.objects.all()
    bedpress = bedpresses.get(pk=pk)
    return render(request, "bedkom/bedpress.html", {"bedpress": bedpress})


class BedriftEndre(LoginRequiredMixin, generic.UpdateView):
    model = Company
    form_class = CompanyForm

    def get_success_url(self):
        return reverse('bedrift', kwargs={'pk': self.object.pk})


class BedriftLag(LoginRequiredMixin, generic.CreateView):
    model = Company
    form_class = CompanyForm

    def get_success_url(self):
        return reverse('bedrift', kwargs={'pk': self.object.pk})



