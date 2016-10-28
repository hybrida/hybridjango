from django.shortcuts import redirect
from django.views import generic

from .models import User


class Profile(generic.DetailView):
    model = User
    template_name = 'registration/profile.html'


def redirect_to_profile(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.id)
    else:
        return redirect('login')

