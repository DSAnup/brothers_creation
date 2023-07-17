from django.contrib import admin
from .models import *
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum


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
        ("Reference1", "Reference2", "isClosed"),
        ("Comments"),
    ]
    list_display = (
        "LoanNumberPretify",
        "Loaner",
        "LoanAmount",
        "LoanGivenDate",
        "InterestRate",
        "Reference1",
        "Reference2",
        "InterestPay",
    )

    ordering = ["LoanNumber"]

    def LoanNumberPretify(self, obj):
        return f"000{obj.LoanNumber}"

    def save_model(self, request, obj, form, change):
        if change:
            existing_obj = Loan.objects.get(pk=obj.pk)

            InterestPayPerMonth = (
                form.cleaned_data["LoanAmount"] / 100
            ) * form.cleaned_data["InterestRate"]

            obj.InterestPay = InterestPayPerMonth
            obj.DateCreated = existing_obj.DateCreated
            obj.DateLastUpdated = timezone.now()
            obj.CreatedBy = existing_obj.CreatedBy
            obj.UpdatedBy = request.user.id
            obj.save()
        else:
            try:
                latest_record = Loan.objects.latest("LoanNumber")
                SetLoanNumber = latest_record.LoanNumber + 1
            except Loan.DoesNotExist:
                SetLoanNumber = 1
                pass
            obj.LoanNumber = SetLoanNumber

            InterestPayPerMonth = (
                form.cleaned_data["LoanAmount"] / 100
            ) * form.cleaned_data["InterestRate"]

            obj.InterestPay = InterestPayPerMonth
            obj.CreatedBy = request.user.id
            obj.save()


admin.site.register(Loan, LoanAdmin)


class LoanReturnAdmin(admin.ModelAdmin):
    fields = [
        ("Loan"),
        ("ReturnDate", "ReturnAmount"),
    ]
    list_display = ("Loan", "ReturnAmount", "ReturnDate")

    def save_model(self, request, obj, form, change):
        if change:
            existing_obj = LoanReturn.objects.get(pk=obj.pk)
            AmountCheck = form.cleaned_data["Loan"].LoanAmount
            CurrentLoanID = form.cleaned_data["Loan"].pk
            PreviousReturnAmount = LoanReturn.objects.filter(
                Loan_id=CurrentLoanID
            ).aggregate(Sum("ReturnAmount"))["ReturnAmount__sum"]

            if PreviousReturnAmount is None:
                PreviousAmount = form.cleaned_data["ReturnAmount"]
                RemainReturn = AmountCheck
                ReturnAmount = 0
            else:
                PreviousAmount = (
                    form.cleaned_data["ReturnAmount"] + PreviousReturnAmount
                )
                RemainReturn = AmountCheck - PreviousReturnAmount
                ReturnAmount = PreviousReturnAmount

            if PreviousAmount > AmountCheck:
                return messages.error(
                    request,
                    f"The Loaner already paid {ReturnAmount}, Remaining Amount {RemainReturn}",
                )
            obj.DateCreated = existing_obj.DateCreated
            obj.DateLastUpdated = timezone.now()
            obj.CreatedBy = existing_obj.CreatedBy
            obj.UpdatedBy = request.user.id
            obj.save()
        else:
            AmountCheck = form.cleaned_data["Loan"].LoanAmount
            CurrentLoanID = form.cleaned_data["Loan"].pk
            PreviousReturnAmount = LoanReturn.objects.filter(
                Loan_id=CurrentLoanID
            ).aggregate(Sum("ReturnAmount"))["ReturnAmount__sum"]

            if PreviousReturnAmount is None:
                PreviousAmount = form.cleaned_data["ReturnAmount"]
                RemainReturn = AmountCheck
                ReturnAmount = 0
            else:
                PreviousAmount = (
                    form.cleaned_data["ReturnAmount"] + PreviousReturnAmount
                )
                RemainReturn = AmountCheck - PreviousReturnAmount
                ReturnAmount = PreviousReturnAmount

            if PreviousAmount > AmountCheck:
                return messages.error(
                    request,
                    f"The Loaner already paid {ReturnAmount}, Remaining Amount {RemainReturn}",
                )
            obj.CreatedBy = request.user.id
            obj.save()


admin.site.register(LoanReturn, LoanReturnAdmin)
