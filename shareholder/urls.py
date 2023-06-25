from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("shareholder/", views.shareholder, name="shareholder"),
    path(
        "sMonthlyPaid/",
        views.sMonthlyPaid,
        name="sMonthlyPaid",
    ),
    path(
        "sMonthlyUnPaid/",
        views.sMonthlyUnPaid,
        name="sMonthlyUnPaid",
    ),
]
