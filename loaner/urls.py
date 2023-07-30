from django.urls import path

from . import views
from .admin import LoanerModelAutocomplete

urlpatterns = [
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
    path(
        "ReferenceBonusList/",
        views.ReferenceBonusList,
        name="ReferenceBonusList",
    ),
    path(
        "autocomplete/",
        LoanerModelAutocomplete.as_view(),
        name="shareHolder-autocomplete",
    ),
]
