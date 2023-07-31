from django.contrib import admin
from .models import *
from django.utils import timezone
from django.contrib import messages
from shareholder.admin import *
from django.utils.safestring import mark_safe

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


class RulesAdmin(admin.ModelAdmin):
    fields = [
        ("Rules"),
    ]
    list_display = ["content_preview"]

    def content_preview(self, obj):
        return mark_safe(obj.Rules[:20])  # Adjust the character limit as needed

    # content_preview.short_description = "Content"

    def save_model(self, request, obj, form, change):
        if change:
            existing_obj = Rules.objects.get(pk=obj.pk)
            obj.DateCreated = existing_obj.DateCreated
            obj.DateLastUpdated = timezone.now()
            obj.CreatedBy = existing_obj.CreatedBy
            obj.UpdatedBy = request.user.id
            obj.save()
        else:
            if Rules.objects.all().count():
                return messages.error(request, "Only update is allowed")
            obj.CreatedBy = request.user.id
            obj.save()


admin.site.register(Rules, RulesAdmin)
