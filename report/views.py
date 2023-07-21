from django.shortcuts import render
from django.http import HttpResponse
import calendar
import datetime
from loaner.models import *
from shareholder.models import *

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

        return render(
            request, "SISearchResult.html", {"ShareHolderList": ShareHolderList}
        )
    else:
        return render(request, SISearch)
