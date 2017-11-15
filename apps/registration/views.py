from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import redirect_to_login
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import generic
from apps.achievements.models import Badge
from apps.achievements.signals.signals import *

from .models import Hybrid, RecoveryMail
from .forms import HybridForm




class Profile(LoginRequiredMixin, generic.DetailView):
    model = Hybrid
    slug_field = 'username'
    template_name = 'registration/profile.html'
    achievements = Badge.objects.order_by().values('user__username').distinct()



class EditProfile(generic.UpdateView):
    model = Hybrid
    slug_field = 'username'
    template_name = 'registration/profile_form.html'
    form_class = HybridForm

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated() and self.get_object() == request.user):
            return redirect_to_login(request.get_full_path())
        return super(EditProfile, self).dispatch(
            request, *args, **kwargs)


def redirect_to_profile(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user)
    else:
        return redirect('login')


token_generator = PasswordResetTokenGenerator()


def register(request):
    successful = False
    if request.method == 'POST':
        username = request.POST.get('username').lower()
    else:
        username = None
    context = {
        'username': username,
    }
    user = Hybrid.objects.filter(username=username).first()
    if user:
        last_mail = RecoveryMail.objects.filter(hybrid=user).first()
        if last_mail and last_mail.timestamp + timezone.timedelta(minutes=10) > timezone.now():
            successful = False
            time_to_wait = last_mail.timestamp + timezone.timedelta(minutes=10)
            context['time_to_wait'] = time_to_wait
        else:
            mails = ['{}@stud.ntnu.no'.format(username)]
            if user.email: mails.append(user.email)
            successful = send_mail(
                'Lag Hybrida.no bruker',
                'Hei {name},\n\nåpne denne linken for å (gjen)opprette brukeren {username}:\n'
                'http{s}://{host}{generated}'.format(
                    name=user.first_name,
                    username=username,
                    s='s' if request.is_secure() else '',
                    host=request.get_host(),
                    generated=reverse('complete_registration', kwargs={
                        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': token_generator.make_token(Hybrid.objects.get(username=username))})),
                'robot@hybrida.no',
                mails,
            )
    if successful: RecoveryMail.objects.create(hybrid=user)
    context['successful'] = successful
    return render(request=request, template_name='registration/register.html', context=context)


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
    return render(request, 'registration/reset_password.html', {'valid': valid, 'form': form})



