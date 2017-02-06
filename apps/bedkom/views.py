from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render
from .models import Company, CompanyComment, Bedpress

@permission_required(['bedkom.add_company'])
def index(request):
    companies = Company.objects.all()
    for company in companies:
        company.last_comment = company.companycomment_set.order_by('timestamp').last()
    return render(request, "bedkom/bedrifter.html", {"companies": companies})

@permission_required(['bedkom.add_company'])
def bedrift(request, pk):
    companies = Company.objects.all()
    bedpresses = Bedpress.objects.filter(company_id=pk)
    return render(request, "bedkom/bedrift.html", {"company": companies.get(pk=pk), "bedpresses": bedpresses})


@permission_required(['bedkom.add_company'])
def comment(request, pk):
    companies = Company.objects.all()
    for company in companies:
        company.last_comment = company.companycomment_set.order_by('timestamp').last()
    return render(request, "bedkom/bedrifter.html", {"companies": companies})


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

