from django.contrib import admin
from .models import *
from django.utils import timezone
from django.contrib import messages


class LoanerAdmin(admin.ModelAdmin):
    fields = [
        ("userName", "password"),
        ("firstName", "lastName"),
        ("mobile", "address"),
        ("profilePic"),
    ]
    list_display = ("userName", "firstName", "mobile", "address")

    def save_model(self, request, obj, form, change):
        if change:
            existing_obj = Loaner.objects.get(pk=obj.pk)
            obj.DateCreated = existing_obj.DateCreated
            obj.DateLastUpdated = timezone.now()
            obj.CreatedBy = existing_obj.CreatedBy
            obj.UpdatedBy = request.user.id
            obj.save()
        else:
            if Loaner.objects.filter(userName=form.cleaned_data["userName"]).exists():
                return messages.error(
                    request, "The user name is already taken please choose another"
                )
            obj.CreatedBy = request.user.id
            obj.save()


admin.site.register(Loaner, LoanerAdmin)


class LoanAdmin(admin.ModelAdmin):
    fields = [
        ("Loaner", "LoanAmount"),
        ("LoanGivenDate", "InterestRate"),
        ("Reference1", "Reference2"),
        ("comments"),
    ]
    list_display = (
        "Loaner",
        "LoanAmount",
        "LoanGivenDate",
        "InterestRate",
        "Reference1",
        "Reference2",
        "InterestPay",
    )

    def save_model(self, request, obj, form, change):
        if change:
            existing_obj = Loan.objects.get(pk=obj.pk)
            obj.DateCreated = existing_obj.DateCreated
            obj.DateLastUpdated = timezone.now()
            obj.CreatedBy = existing_obj.CreatedBy
            obj.UpdatedBy = request.user.id
            obj.save()
        else:
            obj.CreatedBy = request.user.id
            obj.save()


admin.site.register(Loan, LoanAdmin)
