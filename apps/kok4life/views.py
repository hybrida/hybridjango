from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def firstPage(request):
    return render(request, "Kok4life/firstPage.html")
