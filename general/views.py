from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *

# Create your views here.


def expenseList(request):
    ExpenseList = Expense.objects.all()
    template = loader.get_template("ExpenseList.html")
    context = {
        "ExpenseList": ExpenseList,
    }
    return HttpResponse(template.render(context, request))
