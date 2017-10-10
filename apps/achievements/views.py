from django.shortcuts import render

def overview(request):
    return render(request, '../templates/achievments/achievments_overview.html',)