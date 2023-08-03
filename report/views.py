import pprint
from django.shortcuts import render
from django.http import HttpResponse
import calendar
import datetime
from loaner.models import *
from shareholder.models import *
from django.db import connection

# Create your views here.


def index(request):
    return render(request, "index2.html")


def SISearch(request):
    Months = [
        {"value": month_num, "name": month_name}
        for month_num, month_name in enumerate(calendar.month_name)
        if month_num != 0
    ]
    CurrentYear = datetime.datetime.now().year
    YearList = list(range(CurrentYear - 2, CurrentYear + 10))
    CurrentMonth = datetime.datetime.now().month
    context = {
        "MonthList": Months,
        "YearList": YearList,
        "CurrentMonth": CurrentMonth,
        "CurrentYear": CurrentYear,
    }
    return render(request, "SISearch.html", context)


def SISearchResult(request):
    if request.method == "POST":
        Months = request.POST.get("month")
        Year = request.POST.get("year")
        ShareHolderList = ShareHolderInstallment.objects.select_related(
            "shareHolder"
        ).filter(InstallmentDate__month=Months, InstallmentDate__year=Year)

        def myquery(var1, var2):
            query = f"""
                SELECT S.*, SI.InstallmentAmount as amount, SI.InstallmentDate as Idate
                FROM shareholder_shareholder AS S
                LEFT JOIN shareholder_shareholderinstallment AS SI ON SI.shareHolder_id = S.ID
                WHERE MONTH(SI.InstallmentDate) = {var1}
                AND YEAR(SI.InstallmentDate) = {var2}
                UNION
                SELECT S.* , 'Unpaid' as amount, '' as Idate
                FROM shareholder_shareholder AS S
                WHERE ID NOT IN (
                    SELECT SI.shareholder_id
                    FROM shareholder_shareholderinstallment AS SI
                        WHERE MONTH(SI.InstallmentDate) = {var1}
                            AND YEAR(SI.InstallmentDate) = {var2}
                            )
                ORDER BY Idate DESC
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

        ShareHolderList = myquery(Months, Year)
        month_name = calendar.month_name[int(Months)]

        return render(
            request,
            "SISearchResult.html",
            {"ShareHolderList": ShareHolderList, "month_name": month_name},
        )
    else:
        return render(request, SISearch)
