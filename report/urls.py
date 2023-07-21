from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="indexReport"),
    path("SISearch/", views.SISearch, name="SISearch"),
    path("SISearchResult/", views.SISearchResult, name="SISearchResult"),
]
