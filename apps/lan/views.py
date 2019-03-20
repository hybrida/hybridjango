from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from .models import Result
from .forms import ResultForm

class CreateResult(CreateView):
    form_class = ResultForm
    success_url = reverse_lazy('create_result')


class DeleteResult(DeleteView):
    model = Result
    success_url = reverse_lazy('list_results')

class ListResults(ListView):
    model = Result
    ordering = 'time' 