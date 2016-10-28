from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
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


token_generator = PasswordResetTokenGenerator()


def register(request):
    successful = False
    username = request.POST.get('username')
    user = User.objects.filter(username=username).first()
    if user:
        successful = send_mail(
            'Lag Hybrida.no bruker',
            'Hei {name},\n\nåpne på denne linken for å opprette brukeren {username}:\n'
            'http{s}://{host}{generated}'.format(
                name=user.first_name,
                username=username,
                s='s' if request.is_secure() else '',
                host=request.get_host(),
                generated=reverse('complete_registration', kwargs={
                    'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token_generator.make_token(User.objects.get(username=username))})),
            'robot@hybrida.no',
            ['{}@stud.ntnu.no'.format(username), ],
        )
    return render(request, 'accounts/register.html', {'username': username, 'successful': successful})


def complete_registration(request, uidb64, token):
    UserModel = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    valid = (user is not None and token_generator.check_token(user, token))
    if valid:
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = SetPasswordForm(user)
    else:
        form = None
    return render(request, 'accounts/reset_password.html', {'valid': valid, 'form': form})
