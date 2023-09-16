from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from .models import *
from loaner.models import *
from general.models import *
from django.db.models import Sum, Value
from django.db.models.functions import Concat

from django.utils import timezone
from datetime import date, datetime

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
    totalShareHolderActive = ShareHolder.objects.filter(isActive=1).count()
    totalShareHolder = ShareHolder.objects.all().count()
    totalShareNoActive = (
        ShareHolderSetting.objects.select_related("shareHolder")
        .filter(shareHolder__isActive=1)
        .aggregate(sum=Sum("shareNumber"))["sum"]
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
                    AND S.isActive = 1
    """

    total_unpaid_shareNo = calculate_sum(myquery_unpaid_shareNo)
    if total_unpaid_shareNo is None:
        total_receivable_amount = 0
    else:
        if timezone.now().date() > margin_time:
            total_receivable_amount = (500 * total_unpaid_shareNo) + (
                (50 * total_unpaid_shareNo)
            )
        else:
            total_receivable_amount = (
                500 * totalShareNo
            ) - current_month_received_shareholder_installment

    LoanerCount = Loaner.objects.all().count()
    if LoanerCount is None:
        LoanerCount = 0

    LoanActiveCount = Loan.objects.filter(isClosed=0).count()
    if LoanActiveCount is None:
        LoanActiveCount = 0

    LoanClosedCount = Loan.objects.filter(isClosed=1).count()
    if LoanClosedCount is None:
        LoanClosedCount = 0

    LoanAmountActiveSum = Loan.objects.filter(isClosed=0).aggregate(
        sum=Sum("LoanAmount")
    )["sum"]
    if LoanAmountActiveSum is None:
        LoanAmountActiveSum = 0

    InterestRecievedByLoanAmount = LoanMonthlyInstallment.objects.select_related(
        "Loan"
    ).aggregate(sum=Sum("Loan__LoanAmount"))["sum"]

    LoanAmountClosedSum = Loan.objects.filter(isClosed=1).aggregate(
        sum=Sum("LoanAmount")
    )["sum"]
    if LoanAmountClosedSum is None:
        LoanAmountClosedSum = 0

    LoanReturnAmountSum = LoanReturn.objects.aggregate(sum=Sum("ReturnAmount"))["sum"]
    if LoanReturnAmountSum is None:
        LoanReturnAmountSum = 0

    InterestRecievedAmountSum = LoanMonthlyInstallment.objects.aggregate(
        sum=Sum("InstallmentAmount")
    )["sum"]
    if InterestRecievedAmountSum is None:
        InterestRecievedAmountSum = 0

    RefBonusPaidAmountSum1 = ReferenceBonus.objects.filter(isPaid=1).aggregate(
        sum=Sum("BonusAmount1")
    )["sum"]
    if RefBonusPaidAmountSum1 is None:
        RefBonusPaidAmountSum1 = 0
    RefBonusPaidAmountSum2 = ReferenceBonus.objects.filter(isPaid=1).aggregate(
        sum=Sum("BonusAmount2")
    )["sum"]
    if RefBonusPaidAmountSum2 is None:
        RefBonusPaidAmountSum2 = 0

    RefBonusPaidAmountSum = RefBonusPaidAmountSum1 + RefBonusPaidAmountSum2

    RefBonusUnPaidAmountSum1 = ReferenceBonus.objects.filter(isPaid=0).aggregate(
        sum=Sum("BonusAmount1")
    )["sum"]
    if RefBonusUnPaidAmountSum1 is None:
        RefBonusUnPaidAmountSum1 = 0

    RefBonusUnPaidAmountSum2 = ReferenceBonus.objects.filter(isPaid=0).aggregate(
        sum=Sum("BonusAmount2")
    )["sum"]
    if RefBonusUnPaidAmountSum2 is None:
        RefBonusUnPaidAmountSum2 = 0

    RefBonusUnPaidAmountSum = RefBonusUnPaidAmountSum1 + RefBonusUnPaidAmountSum2

    InterestAfterBonusGiven = InterestRecievedAmountSum - RefBonusPaidAmountSum

    ExpenseAmountSum = Expense.objects.aggregate(sum=Sum("ExpenseAmount"))["sum"]
    if ExpenseAmountSum is None:
        ExpenseAmountSum = 0

    TotalCollection = totalAmountShareHolder + InterestAfterBonusGiven

    TotalBalance = (
        totalAmountShareHolder
        - (LoanAmountActiveSum + LoanAmountClosedSum)
        + (InterestRecievedAmountSum - RefBonusPaidAmountSum)
        + LoanReturnAmountSum
        - ExpenseAmountSum
    )

    template = loader.get_template("index.html")

    context = {
        "totalShareHolder": totalShareHolder,
        "totalShareNo": totalShareNo,
        "totalRegistrationAmount": totalRegistrationAmount,
        "current_month_received_shareholder_installment": current_month_received_shareholder_installment,
        "total_receivable_amount": total_receivable_amount,
        "totalAmountShareHolder": totalAmountShareHolder,
        "LoanerCount": LoanerCount,
        "LoanActiveCount": LoanActiveCount,
        "LoanClosedCount": LoanClosedCount,
        "LoanAmountActiveSum": LoanAmountActiveSum,
        "LoanAmountClosedSum": LoanAmountClosedSum,
        "LoanReturnAmountSum": LoanReturnAmountSum,
        "InterestRecievedAmountSum": InterestRecievedAmountSum,
        "InterestAfterBonusGiven": InterestAfterBonusGiven,
        "RefBonusPaidAmountSum": RefBonusPaidAmountSum,
        "RefBonusUnPaidAmountSum": RefBonusUnPaidAmountSum,
        "TotalBalance": TotalBalance,
        "totalShareHolderActive": totalShareHolderActive,
        "totalShareNoActive": totalShareNoActive,
        "ExpenseAmountSum": ExpenseAmountSum,
        "InterestRecievedByLoanAmount": InterestRecievedByLoanAmount,
        "TotalCollection": TotalCollection,
    }

    return HttpResponse(template.render(context, request))


import time


def shareholder(request):
    start_time = time.time()
    myquery = """
                SELECT PS.*, PSSS.shareNumber 
                FROM shareholder_shareholder AS PS
                LEFT JOIN shareholder_shareholdersetting AS PSSS ON PS.id = PSSS.shareholder_id
            """
    mydata = custom_query(myquery)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Query execution time: {elapsed_time} seconds")

    start_time = time.time()
    getShareHolderList = ShareHolderSetting.objects.select_related(
        "shareHolder"
    ).annotate(
        full_name=Concat("shareHolder__firstName", Value(" "), "shareHolder__lastName")
    )
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Query execution time Django Format: {elapsed_time} seconds")
    start_time = time.time()
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
                    AND S.isActive = 1
    """

    total_unpaid_shareNo = calculate_sum(myquery_unpaid_shareNo)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Query execution time 2: {elapsed_time} seconds")
    start_time = time.time()
    getUnpaidShareNo = (
        ShareHolderSetting.objects.select_related("shareHolder")
        .exclude(
            shareHolder__id__in=ShareHolderInstallment.objects.values(
                "shareHolder_id"
            ).filter(
                InstallmentDate__month=datetime.now().month,
                InstallmentDate__year=datetime.now().year,
            ),
            shareHolder__isActive=1,
        )
        .aggregate(sum=Sum("shareNumber"))
    )
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Query execution time Django Format 2: {elapsed_time} seconds")
    template = loader.get_template("shareholder.html")
    context = {"myList": list(getShareHolderList), "result": getShareHolderList}
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


def ShareholderInstallmentHistory(request, id):
    InstallmentList = ShareHolderInstallment.objects.filter(shareHolder=id)

    template = loader.get_template("ShareholderInstallmentHistory.html")
    context = {
        "InstallmentList": InstallmentList,
    }
    return HttpResponse(template.render(context, request))


def SharePaymentCheckList(request):
    def PaymentDayCheck():
        query = f"""
                SELECT S.userName, SS.shareNumber, SS.installmentAmount, S.id, (SELECT SI.InstallmentDate  FROM shareholder_shareholderinstallment AS SI WHERE SI.shareHolder_id = S.id ORDER BY SI.MarginDate DESC LIMIT 1) AS LastInstammentDate,
                    IF(
                    (SELECT SI.MarginDate  FROM shareholder_shareholderinstallment AS SI WHERE SI.shareHolder_id = S.id ORDER BY SI.MarginDate DESC LIMIT 1), 
                    DATEDIFF(NOW(),  (SELECT SI.MarginDate  FROM shareholder_shareholderinstallment AS SI WHERE SI.shareHolder_id = S.id ORDER BY SI.MarginDate DESC LIMIT 1)), DATEDIFF(NOW(), SS.DateCreated)
                ) AS DaysDiffrenetFromNow
                FROM shareholder_shareholder AS S
                LEFT JOIN shareholder_shareholdersetting AS SS ON SS.shareHolder_id = S.id
                WHERE S.isActive = 1
                ORDER BY S.userName ASC
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

    SharePaymentCheckList = PaymentDayCheck()

    return render(
        request,
        "SharePaymentCheckList.html",
        {"SharePaymentCheckList": SharePaymentCheckList},
    )
