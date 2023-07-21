from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .models import *

# Create your views here.


def loanerList(request):
    LoanerList = Loaner.objects.all()

    return render(request, "loaner.html", {"LoanerList": LoanerList})


def loanList(request):
    loanList = Loan.objects.all()

    return render(request, "loanList.html", {"loanList": loanList})


def LoanHistory(request, id):
    LoanHistory = LoanReturn.objects.filter(Loan=id)

    return render(request, "LoanHistory.html", {"LoanHistory": LoanHistory})


def LoanInstallmentHistory(request, id):
    LoanInstallmentHistory = LoanMonthlyInstallment.objects.filter(Loan=id)

    return render(
        request,
        "LoanInstallmentHistory.html",
        {"LoanInstallmentHistory": LoanInstallmentHistory},
    )


def ReferenceBonusList(request):
    ReferenceBonusList = ReferenceBonus.objects.all()

    return render(
        request,
        "ReferenceBonusList.html",
        {"ReferenceBonusList": ReferenceBonusList},
    )
