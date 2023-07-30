from django.urls import path

from . import views
from .admin import ShareHolderModelAutocomplete

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
        "autocomplete/",
        ShareHolderModelAutocomplete.as_view(),
        name="shareHolder-autocomplete",
    ),
]
