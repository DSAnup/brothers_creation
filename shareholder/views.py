from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import loader
from .models import *
from django.db.models import Sum

from django.utils import timezone
from datetime import date

from django.db import connection

current_month = timezone.now().month
current_year = timezone.now().year


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
    margin_time = date(current_year, current_month, 10)
    if timezone.now().date() > margin_time:
        total_receivable_amount = (
            (500 * totalShareNo)
            + (50 * (totalShareNo - total_recieable_shareholder_installment_count))
        ) - current_month_received_shareholder_installment
    else:
        total_receivable_amount = (
            current_month_received_shareholder_installment * totalShareNo
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
