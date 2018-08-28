from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CompanyForm
from .models import Company, CompanyComment, Bedpress, MeetingReport
from django.views.generic.edit import CreateView


@permission_required(['bedkom.add_company'])
def index(request):
    companies = Company.objects.all()
    for company in companies:
        company.last_comment = company.companycomment_set.order_by('timestamp').last()
    return render(request, "bedkom/bedriftsdatabase2.html", {"companies": companies})


@permission_required(['bedkom.add_company'])
def bedrift(request, pk):
    company = Company.objects.get(pk=pk)
    comments = company.companycomment_set.order_by('-timestamp')
    bedpresses = Bedpress.objects.filter(company_id=pk)
    return render(request, "bedkom/bedrift.html", {"company": company, "bedpresses": bedpresses, "comments": comments})


@permission_required(['bedkom.add_company'])
def new_company(request):
    action = 'Lag ny'
    if request.method == "POST":
        print("een")
        form = CompanyForm(request.POST)
        if form.is_valid():
            print("hhe")
            company = form.save(commit=False)
            company.save()
            return redirect('bedrift', pk=company.pk)

    form = CompanyForm(request.POST)
    return render(request, "bedkom/company_form.html", {'action': action, 'form': form, })


@permission_required(['bedkom.change_company'])
def edit_company(request, pk):
    action = "Rediger"
    company = get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            company = form.save(commit=False)
            company.save()
            return redirect('bedrift', pk=company.pk)
    else:
        form = CompanyForm(instance=company)
    return render(request, "bedkom/company_form.html", {'action': action, 'form': form, })


@permission_required(['bedkom.add_company'])
def comment(request, pk):
    companies = Company.objects.all()
    for company in companies:
        company.last_comment = company.companycomment_set.order_by('-timestamp').last()
    return render(request, "bedkom/bedriftsdatabase.html", {"companies": companies})


@permission_required(['bedkom.add_company'])
def bedpress(request, pk):
    bedpresses = Bedpress.objects.all()
    bedpress = bedpresses.get(pk=pk)
    bedpresses = Bedpress.objects.filter(company_id=pk)
    return render(request, "bedkom/bedpress.html", {"bedpress": bedpress, "bedpresses": bedpresses})


@login_required
def comment_company(request, pk):
    companies = Company.objects.all()
    user = request.user
    if request.POST:
        print(request.POST)
        company_id = request.POST['company_id']
        text = request.POST['text']
        if user.is_authenticated:
            comment = CompanyComment(author=user, company=companies.get(pk=company_id), text=text)
            print(comment.full_clean())
            comment.save()
    return redirect('bedrift', pk)


@login_required
def bedpress_company_comment(request, pk):
    companies = Company.objects.all()
    user = request.user
    if request.POST:
        print(request.POST)
        company_id = request.POST['company_id']
        text = request.POST['text']
        if user.is_authenticated:
            comment = CompanyComment(author=user, company=companies.get(pk=company_id), text=text)
            print(comment.full_clean())
            comment.save()
    return redirect('bedpress', pk)

@login_required
def comment_company2(request, pk):
    companies = Company.objects.all()
    user = request.user
    if request.POST:
        print(request.POST)
        company_id = request.POST['company_id']
        text = request.POST['text']
        if user.is_authenticated:
            comment = CompanyComment(author=user, company=companies.get(pk=company_id), text=text)
            print(comment.full_clean())
            comment.save()
    return redirect('bedkom')

@login_required
def edit_status_priority_comment(request, pk):
    companies = Company.objects.all()
    user = request.user
    if request.POST:
        print(request.POST.get('statusForm'))

        text = request.POST['text']
        company_id = request.POST['company_id']
        status = request.POST.get('statusForm', False)
        priority = request.POST.get('priorityForm', False)
        lastcomment = request.POST['lastComment']
        if user.is_authenticated:
            if lastcomment == text:
                company = companies.get(pk=company_id)
                company.status = status
                company.priority = priority
                company.save()
            else:
                company = companies.get(pk=company_id)
                comment = CompanyComment(author=user, company=companies.get(pk=company_id), text=text)
                company.status = status
                company.priority = priority
                comment.save()
                company.save()
    return redirect('bedkom')

def reports(request):
    meetingreports = MeetingReport.objects.all().order_by('date')

    return render(request, "bedkom/reports.html", {"meetingreports": meetingreports})

class AddReport(CreateView):
    model = MeetingReport
    fields = ['report', 'date', 'description']


