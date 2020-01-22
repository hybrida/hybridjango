from django.db import transaction
from django.shortcuts import render, redirect
from django.db.models import Max, Min
from .models import CakeMaker, MeetingReport, Project, Guide
from .forms import ProjectForm, MeetingReportForm
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.views.generic.edit import CreateView
from os import path, listdir
from hybridjango import settings
from hybridjango.utils import group_test
import re
from django.http import HttpResponse, HttpResponseNotFound
from io import StringIO
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from hybridjango.utils import drive


@permission_required(['vevkom.add_project'])
def index(request):
    cake_makers = CakeMaker.objects.all()
    referats = MeetingReport.objects.all().order_by('date').reverse()
    Projects = Project.objects.all()
    guides = Guide.objects.all()
    dump_filenames = drive.get_backup_filenames()

    return render(request, "internside/internside.html", {
        "cake_makers": cake_makers,
        "referats": referats,
        "Projects": Projects,
        "guides": guides,
        "dump_filenames": dump_filenames
    })


@permission_required(['vevkom.add_project'])
def upList(request, pk):
    cake_maker = CakeMaker.objects.get(pk=pk)
    cake_maker_number = cake_maker.number_on_list
    next_maker = CakeMaker.objects.filter(number_on_list__gt=cake_maker_number).last()
    if next_maker:
        with transaction.atomic():
            cake_maker.number_on_list = -1
            cake_maker.save()
            cake_maker.number_on_list = next_maker.number_on_list
            next_maker.number_on_list = cake_maker_number
            next_maker.save()
            cake_maker.save()
    return redirect('internside:index')


@permission_required(['vevkom.add_project'])
def downList(request, pk):
    cake_maker = CakeMaker.objects.get(pk=pk)
    cake_maker_number = cake_maker.number_on_list
    next_maker = CakeMaker.objects.filter(number_on_list__lt=cake_maker_number).first()
    if next_maker:
        with transaction.atomic():
            cake_maker.number_on_list = -1
            cake_maker.save()
            cake_maker.number_on_list = next_maker.number_on_list
            next_maker.number_on_list = cake_maker_number
            next_maker.save()
            cake_maker.save()

    return redirect('internside:index')


@permission_required(['vevkom.add_project'])
def bottom(request, pk):
    from .models import CakeMaker
    cake_maker = CakeMaker.objects.get(pk=pk)
    cake_makers = CakeMaker.objects.all().order_by('number_on_list')
    cake_maker_number = cake_maker.number_on_list
    for i in range(cake_maker_number, cake_makers.__sizeof__()):
        downList(request, pk)

    return redirect('internside:index')

@permission_required(['vevkom.add_project'])
def top(request, pk):
    from .models import CakeMaker
    cake_maker = CakeMaker.objects.get(pk=pk)
    cake_makers = CakeMaker.objects.all().order_by('number_on_list')
    cake_maker_number = cake_maker.number_on_list
    for i in range(0, cake_makers.__sizeof__()):
        upList(request, pk)

    return redirect('internside:index')


@permission_required(['vevkom.add_project'])
def edit_todo(request, pk):
    projects = Project.objects.all()
    user = request.user
    if request.POST:
        print(request.POST.get('statusForm'))

        text = request.POST['text']
        company_id = request.POST['Project_id']
        status = request.POST.get('statusForm', False)
        priority = request.POST.get('priorityForm', False)

        if user.is_authenticated:
                project = projects.get(pk=company_id)
                project.status = status
                project.priority = priority
                project.description = text
                project.save()
    return redirect('internside:index')


def AddProject(request):
    form = ProjectForm(request.POST)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect('internside:index')

    return render(request, 'vevkom/project_form.html', {
        'form':form,
    })


def AddMeetingReport(request):
        form = MeetingReportForm(request.POST)
        if request.method == 'POST':
            form = MeetingReportForm(request.POST)
            if form.is_valid():
                application = form.save(commit=False)
                application.user = request.user
                application.save()
                return redirect('internside:index')

        return render(request, 'internside/meetingreport_form.html', {
            'form': form,
        })


@user_passes_test(group_test("Vevkom"))
def serve_data_dump(request):
    # get password and filename from form (see internside.html)
    password = request.GET.get("password", None)
    filename = request.GET.get("filename", None)
    files = drive.get_backup_filenames()
    if filename is None or filename not in files:
        return HttpResponseNotFound("Not a valid file")
    if password is None:
        return HttpResponseNotFound("You must provide a default password")
    # hash the password given in request
    hasher = PBKDF2PasswordHasher()
    default_password = hasher.encode(password, hasher.salt(), iterations=100000)
    # write new file content to stream
    input_stream = drive.get_backup_from_filename(filename)
    output_stream = StringIO()
    for line in input_stream.readlines():
        # decode bytes to str
        line_str = line.decode('UTF-8')
        # use regex to replace passwords with hashed password
        output_stream.write(re.sub(r'(\s*"password":) ".*"', r'\1 "{}"'.format(default_password), line_str))
    # reset stream to start so that we can read it
    output_stream.seek(0)
    # create response from stream
    new_file_name = filename.split('.')[0] + '_SAFE.json'
    response = HttpResponse(output_stream.read(), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(new_file_name)
    return response
