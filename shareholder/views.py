from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from .models import *
from loaner.models import *
from django.db.models import Sum

from django.utils import timezone
from datetime import date

from django.db import connection

current_month = timezone.now().month
current_year = timezone.now().year


def custom_query(query):
    # Perform the custom query
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        results = cursor.fetchall()
        rows_as_dict = []
        for row in results:
            row_dict = dict(zip(columns, row))
            rows_as_dict.append(row_dict)
        return rows_as_dict


def calculate_sum(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()[0]  # Fetch the first column of the first row

    return result


# Create your views here.
def index(request):
    totalShareHolder = ShareHolder.objects.all().count()
    total_recieable_shareholder_installment_count = (
        ShareHolderInstallment.objects.filter(
            InstallmentDate__month=current_month, InstallmentDate__year=current_year
        ).count()
    )
    totalShareNo = ShareHolderSetting.objects.aggregate(sum=Sum("shareNumber"))["sum"]
    totalRegistrationAmount = ShareHolderSetting.objects.aggregate(
        sum=Sum("registrationAmount")
    )["sum"]
    totalAmountShareHolder = (
        ShareHolderInstallment.objects.aggregate(sum=Sum("InstallmentAmount"))["sum"]
        + totalRegistrationAmount
    )
    current_month_received_shareholder_installment = (
        ShareHolderInstallment.objects.filter(
            InstallmentDate__month=current_month, InstallmentDate__year=current_year
        ).aggregate(Sum("InstallmentAmount"))["InstallmentAmount__sum"]
    )
    if current_month_received_shareholder_installment is None:
        current_month_received_shareholder_installment = 0

    margin_time = date(current_year, current_month, 10)
    myquery_unpaid_shareNo = """
        SELECT SUM(SS.shareNumber) AS sumunpaid
                FROM shareholder_shareholder AS S
                left join shareholder_shareholdersetting AS SS ON SS.shareHolder_id = S.id
                WHERE S.id NOT IN (
                    SELECT SI.shareholder_id
                    FROM shareholder_shareholderinstallment AS SI
                        WHERE MONTH(SI.InstallmentDate) = MONTH(CURDATE())
                            AND YEAR(SI.InstallmentDate) = YEAR(CURDATE())
                    )
    """

    total_unpaid_shareNo = calculate_sum(myquery_unpaid_shareNo)

    if timezone.now().date() > margin_time:
        total_receivable_amount = (500 * total_unpaid_shareNo) + (
            (50 * total_unpaid_shareNo)
        )
    else:
        total_receivable_amount = (
            500 * totalShareNo
        ) - current_month_received_shareholder_installment

    template = loader.get_template("index.html")

    context = {
        "totalShareHolder": totalShareHolder,
        "totalShareNo": totalShareNo,
        "totalRegistrationAmount": totalRegistrationAmount,
        "current_month_received_shareholder_installment": current_month_received_shareholder_installment,
        "total_receivable_amount": total_receivable_amount,
        "totalAmountShareHolder": totalAmountShareHolder,
    }

    return HttpResponse(template.render(context, request))


def shareholder(request):
    myquery = """
                SELECT PS.*, PSSS.shareNumber 
                FROM shareholder_shareholder AS PS
                LEFT JOIN shareholder_shareholdersetting AS PSSS ON PS.id = PSSS.shareholder_id
            """
    mydata = custom_query(myquery)
    template = loader.get_template("shareholder.html")
    context = {
        "myList": mydata,
    }
    return HttpResponse(template.render(context, request))


def sMonthlyPaid(request):
    myquery = """
                SELECT S.userName, S.mobile, SS.shareNumber, SI.InstallmentAmount, SI.InstallmentDate, SS.id
                FROM shareholder_shareholder AS S
                LEFT JOIN shareholder_shareholdersetting AS SS ON S.id = SS.shareholder_id
                LEFT JOIN shareholder_shareholderinstallment AS SI ON S.id = SI.shareholder_id
                    WHERE MONTH(SI.InstallmentDate) = MONTH(CURDATE())
                        AND YEAR(SI.InstallmentDate) = YEAR(CURDATE());
            """
    mydata = custom_query(myquery)
    getStudentList = ShareHolder.objects.values_list("userName", flat=True)
    column_list = list(getStudentList)

    template = loader.get_template("sMonthlyPaid.html")
    context = {
        "myList": mydata,
    }
    return HttpResponse(template.render(context, request))


def sMonthlyUnPaid(request):
    myquery = """
                SELECT S.* 
                FROM shareholder_shareholder AS S
                WHERE ID NOT IN (
                    SELECT SI.shareholder_id
                    FROM shareholder_shareholderinstallment AS SI
                        WHERE MONTH(SI.InstallmentDate) = MONTH(CURDATE())
                            AND YEAR(SI.InstallmentDate) = YEAR(CURDATE())
                    )
            """
    mydata = custom_query(myquery)

    template = loader.get_template("sMonthlyUnPaid.html")
    context = {
        "myList": mydata,
    }
    return HttpResponse(template.render(context, request))


def loanerList(request):
    LoanerList = Loaner.objects.all()

    return render(request, "loaner/loaner.html", {"LoanerList": LoanerList})


def loanList(request):
    loanList = Loan.objects.all()

    return render(request, "loaner/loanList.html", {"loanList": loanList})


def LoanHistory(request, id):
    LoanHistory = LoanReturn.objects.filter(Loan=id)

    return render(request, "loaner/LoanHistory.html", {"LoanHistory": LoanHistory})


def ShareholderInstallmentHistory(request, id):
    InstallmentList = ShareHolderInstallment.objects.filter(shareHolder=id)

    template = loader.get_template("ShareholderInstallmentHistory.html")
    context = {
        "InstallmentList": InstallmentList,
    }
    return HttpResponse(template.render(context, request))


def LoanInstallmentHistory(request, id):
    LoanInstallmentHistory = LoanMonthlyInstallment.objects.filter(Loan=id)

    return render(
        request,
        "loaner/LoanInstallmentHistory.html",
        {"LoanInstallmentHistory": LoanInstallmentHistory},
    )
