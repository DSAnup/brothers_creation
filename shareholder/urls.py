from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("shareholder/", views.shareholder, name="shareholder"),
    path(
        "ShareholderInstallmentHistory/<int:id>",
        views.ShareholderInstallmentHistory,
        name="ShareholderInstallmentHistory",
    ),
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
    path(
        "loanerList/",
        views.loanerList,
        name="loanerList",
    ),
    path(
        "loanList/",
        views.loanList,
        name="loanList",
    ),
    path(
        "LoanHistory/<int:id>",
        views.LoanHistory,
        name="LoanHistory",
    ),
    path(
        "LoanInstallmentHistory/<int:id>",
        views.LoanInstallmentHistory,
        name="LoanInstallmentHistory",
    ),
]
