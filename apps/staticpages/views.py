import json
import os
from itertools import chain
from os import path

from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import resolve, reverse_lazy
from django.utils import timezone
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from django.views.generic.edit import CreateView, DeleteView
from django.core.mail import send_mail

from hybridjango.settings import STATIC_FOLDER
from apps.events.models import Event, TPEvent
from apps.events.views import EventList
from apps.jobannouncements.models import Job
from apps.registration.models import Hybrid, ContactPerson, get_graduation_year
from .forms import CommiteApplicationForm, ApplicationForm, UpdatekForm, StatuteForm
from .models import Application, BoardReport, BoardReportSemester, CommiteApplication, Ktv_report, Protocol, Statute, \
    Updatek


class FrontPage(EventList):
    model = EventList.model
    queryset = EventList.queryset

    def get_context_data(self, **kwargs):
        tp_events = TPEvent.objects.filter(event_start__gte=timezone.now())

        context = super(EventList, self).get_context_data(**kwargs)
        event_list_chronological = Event.objects.filter(
            event_start__gte=timezone.now(), bedpress__isnull=True, hidden=False
        )
        bedpress_list_chronological = Event.objects.filter(event_start__gte=timezone.now(), bedpress__isnull=False,
                                                           hidden=False)
        if not self.request.user.is_authenticated:
            event_list_chronological = event_list_chronological.filter(public=True)
            bedpress_list_chronological = bedpress_list_chronological.filter(public=True)

        context['event_list_chronological'] = event_list_chronological.order_by('event_start')[:7]
        context['bedpress_list_chronological'] = sorted(chain(bedpress_list_chronological.order_by('event_start')[:7],
                                                              [tp_event for tp_event in tp_events
                                                               if tp_event.event_start > timezone.now()]
                                                              ), key=lambda event: event.event_start)[:7]

        prioritized_jobs = Job.objects.filter(deadline__gte=timezone.now(), priority=True)
        context['job_list_priority'] = prioritized_jobs.order_by('-weight', 'deadline')
        job_rows_left = max(0, 7 - prioritized_jobs.count())
        context['job_list_others'] = Job.objects.filter(deadline__gte=timezone.now()).order_by('-weight',
                                                                                               'deadline').filter(
            priority=False)[:job_rows_left]

        try:
            with open(path.join(settings.MEDIA_ROOT, 'ScoreboardCurrent.json'), encoding='utf-8') as data_file:
                scorelist = json.loads(data_file.read())
            context['Scorelist'] = scorelist
        except FileNotFoundError:
            context['Scorelist'] = []

        return context


aboutpages = [
    ('about', "Om Hybrida"),
    ('history', "Hybridas historie"),
    ('board', "Styret"),
    ('committees', "Komiteer"),
    ('griffensorden', "Griffens Orden"),
    ('statutter', "Statutter"),
    ('tillitsvalgte', 'Tillitsvalgte'),
    ('studiet', "Studiet I&IKT"),
    ('holte', "Holte Consulting"),
    ('lyrics', "Sangtekster"),
    ('for_companies', "For bedrifter"),
    ('contact_us', "Kontakt oss"),
]


class AboutView(TemplateResponseMixin, ContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'active_page' in context.keys():
            active_page = context['active_page']
        else:
            active_page = resolve(request.path_info).url_name
        before_pages = []
        after_pages = []
        page_found = False
        for page in aboutpages:
            if page_found:
                after_pages.append(page)
            else:
                before_pages.append(page)
                if page[0] == active_page:
                    page_found = True

        context['before_pages'] = before_pages
        context['after_pages'] = after_pages
        board_search_names = [
            'leder',
            'nestleder',
            'skattmester',
            'festivalus',
            'bksjef',
            'vevsjef',
            'jentekomsjef',
            'prokomsjef',
        ]
        elected_representatives_search_names = [
            'itv1',
            'itv2',
            'forste_ktv1',
            'forste_ktv2',
            'andre_ktv1',
            'andre_ktv2',
            'tredje_ktv1',
            'tredje_ktv2',
            'fjerde_ktv1',
            'fjerde_ktv2',
            'femte_ktv1',
            'femte_ktv2',
        ]
        # in_bulk returns a dict of the form {field_value: obj}, i.e. {search_name: contact_person}
        board_dict = ContactPerson.objects.in_bulk(board_search_names, field_name='search_name')
        elected_dict = ContactPerson.objects.in_bulk(elected_representatives_search_names, field_name='search_name')
        context.update({
            # map titles to ContactPerson objects, used instead of board_dict.values() to preserve order
            'board': [*map(board_dict.get, board_search_names)],
            # ** operator unpacks board dict, adding its mapped contents to the context dict
            **board_dict,
            'elected': [*map(elected_dict.get, elected_representatives_search_names)],
            **elected_dict,
            'redaktor': ContactPerson.objects.get(search_name='redaktor'),
            'faddersjef': ContactPerson.objects.get(search_name='faddersjef'),
        })
        return self.render_to_response(context)


ringenpages = [
    ('ringen', "Ringen"),
    ('ringen_IIKT', 'Studiet I&IKT'),
    ('ringen_visjon', 'Visjon'),
    ('ringen_styret', 'Styret'),
    ('ringen_medlemmer', 'Medlemmer'),
    ('ringen_promotering', 'Promotering'),
    ('ringen_kontakt', 'Kontaktinformasjon'),
]


def members(request):
    if request.method == 'GET':
        endyear = get_graduation_year(1)
    elif request.method == 'POST':
        endyear = get_graduation_year(request.POST.get("grade"))
    return render(request, "staticpages/students.html",
                  {'students': Hybrid.objects.filter(graduation_year=endyear).order_by('last_name')})


class StatutesView(LoginRequiredMixin, AboutView):
    def get_context_data(self, **kwargs):
        context = super(StatutesView, self).get_context_data(**kwargs)
        context['statute'] = Statute.objects.all().last()
        context['active_page'] = 'statutter'
        return context


class StatuteCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'staticpages.add_statute'
    model = Statute
    form_class = StatuteForm
    success_url = reverse_lazy('statutter')


class ProtocolView(LoginRequiredMixin, AboutView):
    def get_context_data(self, **kwargs):
        context = super(ProtocolView, self).get_context_data(**kwargs)
        context['protocols'] = Protocol.objects.all().order_by('date').reverse()
        context['active_page'] = 'statutter'
        return context


class BoardReportView(LoginRequiredMixin, AboutView):
    def get_context_data(self, **kwargs):
        context = super(BoardReportView, self).get_context_data(**kwargs)
        context['reports'] = BoardReport.objects.all().order_by('date').reverse()
        context['active_page'] = 'board'
        context['reportsemseters'] = BoardReportSemester.objects.all().order_by('pk').reverse()
        return context


class RingenView(TemplateResponseMixin, ContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        active_page = resolve(request.path_info).url_name
        before_pages = []
        after_pages = []
        page_found = False
        for page in ringenpages:
            if page_found:
                after_pages.append(page)
            else:
                before_pages.append(page)
                if page[0] == active_page:
                    page_found = True

        context['before_pages'] = before_pages
        context['after_pages'] = after_pages
        context['ringen'] = 'img/bannerIKT.png'
        return self.render_to_response(context)


class UpdatekView(TemplateResponseMixin, ContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        updateks = Updatek.objects.all().order_by('-school_year', 'edition')
        year = ''
        editions = []
        years_with_editions = []
        for updatek in updateks:
            if updatek.school_year == year:
                editions.append(updatek)
            else:
                if year != '':
                    years_with_editions.append([year, editions])
                year = updatek.school_year
                editions = []
                editions.append(updatek)
        years_with_editions.append([year, editions])
        context['updatek'] = years_with_editions
        return self.render_to_response(context)


class UpdatekCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'staticpages.add_updatek'
    model = Updatek
    form_class = UpdatekForm
    success_url = reverse_lazy('updatek')


@login_required
def search(request):
    query = request.GET['tekst']
    from itertools import chain
    event_object = Event.objects.filter(title__icontains=query)
    job_object_title = Job.objects.filter(title__icontains=query)
    job_object_company = Job.objects.filter(company__name__icontains=query)
    user_object_username = Hybrid.objects.filter(username__icontains=query)

    complete_list = list(chain(event_object, job_object_title, job_object_company, user_object_username, ))
    print(complete_list)

    context = {
        'object_list': complete_list,

    }
    return render(request, 'staticpages/search.html', context)


@permission_required(['staticpages.add_application'])
def application_table(request):
    applications = Application.objects.all().order_by('pk').reverse()
    return render(request, 'staticpages/application_table.html', {"applications": applications})


@permission_required(['staticpages.add_commiteapplication'])
def commiteapplications(request):
    comapplications = CommiteApplication.objects.all()

    return render(request, 'staticpages/commite_applications.html', {"comapplications": comapplications})


def application(request):
    form = ApplicationForm(request.POST)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application_form = form.save(commit=False)
            application_form.save()
            mail = ['skattmester@hybrida.no']
            sucsessful = send_mail('Søknad om støtte fra styret',
                                   'Navn: {navn}\n{beskrivelse}'
                                   .format(navn=application_form.name, beskrivelse=application_form.description),
                                   'robot@hybrida.no',
                                   mail,
                                   )

            return redirect('about')

    return render(request, 'staticpages/application_form.html', {
        'form': form,
    })


def edit_application(request, pk):
    applications = Application.objects.all()
    user = request.user
    if request.POST:
        print(request.POST.get('applicationForm'))

        comment = request.POST['text']
        application_id = request.POST['Application_id']
        granted = request.POST.get('grantForm', False)

        if user.is_authenticated:
            application_form = applications.get(pk=application_id)
            application_form.granted = granted
            application_form.comment = comment
            application_form.save()
    return redirect('application_table')


class DeleteApplication(DeleteView):
    model = Application
    success_url = reverse_lazy('application_table')


@login_required
def AddComApplication(request):
    form = CommiteApplicationForm(request.POST)
    if request.method == 'POST':
        form = CommiteApplicationForm(request.POST)
        if form.is_valid():
            ComApplication = form.save(commit=False)
            ComApplication.navn = request.user
            ComApplication.save()
            return redirect('about')

    return render(request, 'staticpages/comapplication_form.html', {
        'form': form,
    })


def NewStudent(request):
    return render(request, 'staticpages/new_student.html', {
        'faddersjef': ContactPerson.objects.get(search_name='faddersjef'),
    })


def ChangeAcceptedStatus(request):
    request.user.accepted_conditions = True
    request.user.save()
    return redirect('/')


class KTVReportView(LoginRequiredMixin, AboutView):
    def get_context_data(self, **kwargs):
        context = super(KTVReportView, self).get_context_data(**kwargs)
        context['reports'] = Ktv_report.objects.all().order_by('date').reverse()
        context['active_page'] = 'tillitsvalgte'
        return context
