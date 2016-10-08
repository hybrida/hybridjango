from .models import User
from django.views import generic
from django.shortcuts import redirect


class Profile(generic.DetailView):
    model = User
    template_name = 'accounts/profile.html'


def redirect_to_profile(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.id)
    else:
        return redirect('login')

