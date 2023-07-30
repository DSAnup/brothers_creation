from django.contrib import admin
from .models import *
from django.utils import timezone
from django.contrib import messages
from .admin import *

# Register your models here.


class ExpenseAdmin(admin.ModelAdmin):
    fields = [
        ("ShareHolder", "ExpensePurpose"),
        ("ExpenseDate", "ExpenseAmount"),
        ("Comments"),
    ]
    list_display = (
        "ShareHolder",
        "ExpensePurpose",
        "ExpenseDate",
        "ExpenseAmount",
        "Comments",
    )
    list_filter = ["ExpenseDate"]
    search_fields = [
        "ShareHolder__userName",
        "ExpensePurpose",
    ]
    list_per_page = 30
    autocomplete_fields = ["ShareHolder"]

    def save_model(self, request, obj, form, change):
        if change:
            existing_obj = Expense.objects.get(pk=obj.pk)
            obj.DateCreated = existing_obj.DateCreated
            obj.DateLastUpdated = timezone.now()
            obj.CreatedBy = existing_obj.CreatedBy
            obj.UpdatedBy = request.user.id
            obj.save()
        else:
            obj.CreatedBy = request.user.id
            obj.save()


admin.site.register(Expense, ExpenseAdmin)
