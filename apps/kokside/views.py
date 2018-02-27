from .models import kok
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin



class index(request):
    koks = kok.objects.all()
    return render(request, kokside/kokside.html )

class Kokview(LoginRequiredMixin, AboutView):
    def get_context_data(self, **kwargs):
        context = super(KokView, self).get_context_data(**kwargs)
        context['reports'] = kok.objects.all()
        context['active_page'] = 'board'
        return context