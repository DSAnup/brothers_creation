from django.urls import path

from . import views
from .admin import ShareHolderModelAutocomplete

urlpatterns = [
    path(
        "expenseList/",
        views.expenseList,
        name="expenseList",
    ),
    path(
        "autocomplete/",
        ShareHolderModelAutocomplete.as_view(),
        name="shareHolder-autocomplete",
    ),
    path(
        "RuleDisplay/",
        views.RuleDisplay,
        name="RuleDisplay",
    ),
]
