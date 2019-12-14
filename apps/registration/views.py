from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import generic
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View

from apps.achievements.models import Badge
from .forms import HybridForm, GroupForm
from .models import Hybrid, RecoveryMail
from apps.events.models import Event, Attendance


class Profile(LoginRequiredMixin, generic.DetailView):
    model = Hybrid
    slug_field = 'username'
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attendance_list_chronological = []
        for attendance in Attendance.objects.all():
            if (attendance.is_waiting(self.request.user) or attendance.is_signed(
                    self.request.user)) and attendance.event.event_start > timezone.now():
                attendance_list_chronological.append(attendance)
        context['attendance_list_chronological'] = attendance_list_chronological
        return context


# def post(self, request, *args, **kwargs): midlertidig fjernet
#    if 'update' in self.request.POST:
#       hybrid = self.request.POST.get('update')
#      year_status_change.send(sender=Hybrid, instance=hybrid)
#     return redirect('profile', hybrid)


class EditProfile(generic.UpdateView):
    model = Hybrid
    slug_field = 'username'
    template_name = 'registration/profile_form.html'
    form_class = HybridForm

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and self.get_object() == request.user):
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
                        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
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


class ManageGroups(UserPassesTestMixin, TemplateResponseMixin, ContextMixin, View):
    template_name = 'registration/group_management.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Styret').exists() or \
               self.request.user.groups.filter(name='Redaktør').exists()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        users = Hybrid.objects.all().order_by('first_name')
        groups = Group.objects.all().order_by('name')
        all_groups_and_members = []
        committees = ['Arrkom', 'Bedkom', 'Jentekom', 'Redaksjonen', 'Vevkom']
        for group in groups:
            form = GroupForm()
            is_committee = False
            group_members = users.filter(groups__name=group.name)
            if group.name in committees:
                is_committee = True
            all_groups_and_members.append([group, group_members, is_committee, form])

        context.update({
            'all_groups_and_members': all_groups_and_members,
        })
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = GroupForm(request.POST)
