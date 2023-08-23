from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .models import *
from django.db import connection

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


def LoanPaymentCheckList(request):
    def PaymentDayCheck():
        query = f"""
                SELECT LO.userName, L.id, L.LoanAmount, L.LoanGivenDate, L.InterestPay, (SELECT LI.InstallmentDate  FROM loaner_loanmonthlyinstallment AS LI WHERE LI.Loan_id = L.id ORDER BY LI.InstallmentMonth DESC LIMIT 1) AS LastInstammentDate,
                (SELECT LI.MarginDate  FROM loaner_loanmonthlyinstallment AS LI WHERE LI.Loan_id = L.id ORDER BY LI.InstallmentMonth DESC LIMIT 1) AS MarginDate,
                IF(
                    (SELECT LI.InstallmentMonth  FROM loaner_loanmonthlyinstallment AS LI WHERE LI.Loan_id = L.id ORDER BY LI.InstallmentMonth DESC LIMIT 1), 
                    DATEDIFF(NOW(),  (SELECT LI.MarginDate  FROM loaner_loanmonthlyinstallment AS LI WHERE LI.Loan_id = L.id ORDER BY LI.InstallmentMonth DESC LIMIT 1)), DATEDIFF(NOW(), L.LoanGivenDate)
                ) AS DaysDiffrenetFromNow
                FROM loaner_loaner AS LO
                LEFT JOIN loaner_loan AS L ON LO.id = L.Loaner_id
                WHERE L.isClosed = 0
            """
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            results = cursor.fetchall()
            rows_as_dict = []
            for row in results:
                row_dict = dict(zip(columns, row))
                rows_as_dict.append(row_dict)
            return rows_as_dict

    LoanPaymentCheckList = PaymentDayCheck()

    return render(
        request,
        "LoanPaymentCheckList.html",
        {"LoanPaymentCheckList": LoanPaymentCheckList},
    )
