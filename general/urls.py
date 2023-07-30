from django.urls import path

from . import views
from .admin import LoanerModelAutocomplete

urlpatterns = [
    path(
        "expenseList/",
        views.expenseList,
        name="expenseList",
    )
]
