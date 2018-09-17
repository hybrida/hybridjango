from django.db import transaction
from django.shortcuts import render, redirect
from django.db.models import Max, Min
from .models import CakeMaker, MeetingReport, Project, Guide
from .forms import ProjectForm, MeetingReportForm
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView


@permission_required(['vevkom.add_project'])
def index(request):
    cake_makers = CakeMaker.objects.all()
    referats = MeetingReport.objects.all().order_by('date').reverse()
    Projects = Project.objects.all()
    guides = Guide.objects.all()

    return render(request, "internside/internside.html", {"cake_makers": cake_makers, "referats": referats, "Projects": Projects,"guides": guides })


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
    for i in range(cake_maker_number, cake_makers.__sizeof__()):
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