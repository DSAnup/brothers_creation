from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

# Create your views here.


def index(request):
    allowed_hosts = settings.ALLOWED_HOSTS
    print(request.get_host())
    return HttpResponse("hello")
