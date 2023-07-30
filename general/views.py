from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def expenseList(request):
    content = "This is a custom admin view."
    return HttpResponse(content, content_type="text/plain")
