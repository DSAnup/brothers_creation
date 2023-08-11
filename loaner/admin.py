from django.contrib import admin
from .models import *
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum
from django.utils.dateformat import DateFormat
from django.shortcuts import get_object_or_404
from dal import autocomplete


class LoanerModelAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Loaner.objects.all()

        if self.q:
            qs = qs.filter(firstName__istartswith=self.q)

        return qs


class LoanerAdmin(admin.ModelAdmin):
    fields = [
        ("userName", "password"),
        ("firstName", "lastName"),
        ("mobile", "address"),
        ("profilePic"),
    ]
    list_display = ("userName", "firstName", "mobile", "address")
    list_filter = ["userName"]
    search_fields = ["userName", "mobile"]
    list_per_page = 30

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
        "isClosed",
    )

    ordering = ["LoanNumber"]
    list_filter = ["Loaner", "LoanGivenDate"]
    search_fields = ["Loaner__userName", "Reference1__userName", "Reference2__userName"]
    list_per_page = 30
    autocomplete_fields = ["Loaner"]

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
    list_filter = ["Loan", "ReturnDate"]
    search_fields = ["Loan__LoanNumber", "Loan__Loaner__userName"]
    list_per_page = 30
    autocomplete_fields = ["Loan"]

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

            if PreviousAmount == AmountCheck:
                LoanObject = get_object_or_404(Loan, pk=CurrentLoanID)
                LoanObject.isClosed = 1
                LoanObject.save()

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

            if PreviousAmount == AmountCheck:
                LoanObject = get_object_or_404(Loan, pk=CurrentLoanID)
                LoanObject.isClosed = 1
                LoanObject.save()

            obj.CreatedBy = request.user.id
            obj.save()


admin.site.register(LoanReturn, LoanReturnAdmin)


class LoanMonthlyInstallmentAdmin(admin.ModelAdmin):
    fields = [
        ("Loan", "InstallmentMonth"),
        ("InstallmentDate", "InstallmentPenalty", "AnyDiscount"),
        ("Comments"),
    ]
    list_display = (
        "Loan",
        "Loan_Amount",
        "InstallmentAmount",
        "interest_month",
        "InstallmentDate",
        "InstallmentPenalty",
        "AnyDiscount",
        "Comments",
    )
    list_filter = ["Loan", "InstallmentDate"]
    search_fields = ["Loan__LoanNumber", "Loan__Loaner__userName"]
    list_per_page = 30
    autocomplete_fields = ["Loan"]

    def interest_month(self, obj):
        return obj.InstallmentMonth.strftime("%B")

    interest_month.short_description = "Interest Month"

    def save_model(self, request, obj, form, change):
        Cleaneddate = form.cleaned_data["InstallmentMonth"]
        Year = Cleaneddate.year
        Month = Cleaneddate.month

        InstallmentDate = form.cleaned_data["InstallmentDate"]
        InstallmentDay = InstallmentDate.day
        LoanGivenDate = form.cleaned_data["Loan"].LoanGivenDate
        Reference1 = form.cleaned_data["Loan"].Reference1
        Reference2 = form.cleaned_data["Loan"].Reference2
        MarginDay = LoanGivenDate.day

        CurrentLoanID = form.cleaned_data["Loan"].pk
        AmountCheck = form.cleaned_data["Loan"].LoanAmount
        InterestRate = form.cleaned_data["Loan"].InterestRate

        if change:
            existing_obj = LoanMonthlyInstallment.objects.get(pk=obj.pk)

            PreviousReturnAmount = LoanReturn.objects.filter(
                Loan_id=CurrentLoanID
            ).aggregate(Sum("ReturnAmount"))["ReturnAmount__sum"]

            if PreviousReturnAmount is None:
                RemainAmount = AmountCheck
            else:
                RemainAmount = AmountCheck - PreviousReturnAmount

            if RemainAmount == 0:
                LoanObject = get_object_or_404(Loan, pk=CurrentLoanID)
                LoanObject.isClosed = 1
                LoanObject.save()
                return messages.success(request, "You have no pending Installment")

            if InstallmentDay > MarginDay:
                CalculateInterest = (
                    (RemainAmount / 100)
                    * (InterestRate + form.cleaned_data["InstallmentPenalty"])
                ) - form.cleaned_data["AnyDiscount"]
            else:
                CalculateInterest = (
                    (RemainAmount / 100) * InterestRate
                ) - form.cleaned_data["AnyDiscount"]

            obj.InstallmentAmount = CalculateInterest
            obj.DateCreated = existing_obj.DateCreated
            obj.DateLastUpdated = timezone.now()
            obj.CreatedBy = existing_obj.CreatedBy
            obj.UpdatedBy = request.user.id
            obj.save()

            if Reference1 or Reference2:
                if ReferenceBonus.objects.filter(
                    Loan=CurrentLoanID, PaidMonth__month=Month
                ).exists():
                    return
                secondary_obj = ReferenceBonus.objects.create()
                CalculateBonus = (RemainAmount / 100) * 0.5

                if Reference1 and Reference2:
                    DivideBonus = CalculateBonus / 2
                    reminder = CalculateBonus % 2
                    if reminder == 1:
                        secondary_obj.BonusAmount1 = DivideBonus + reminder
                    else:
                        secondary_obj.BonusAmount1 = DivideBonus
                    secondary_obj.BonusAmount2 = DivideBonus
                elif Reference1:
                    secondary_obj.BonusAmount1 = CalculateBonus
                else:
                    secondary_obj.BonusAmount2 = CalculateBonus

                secondary_obj.Reference1 = Reference1
                secondary_obj.Reference2 = Reference2
                secondary_obj.CreatedBy = request.user.id
                secondary_obj.Loan = form.cleaned_data["Loan"]
                secondary_obj.PaidMonth = Cleaneddate
                secondary_obj.save()

        else:
            if LoanMonthlyInstallment.objects.filter(
                Loan=CurrentLoanID,
                InstallmentMonth__month=Month,
                InstallmentMonth__year=Year,
            ).exists():
                return messages.error(request, "You already paid this month")

            PreviousReturnAmount = LoanReturn.objects.filter(
                Loan_id=CurrentLoanID
            ).aggregate(Sum("ReturnAmount"))["ReturnAmount__sum"]

            if PreviousReturnAmount is None:
                RemainAmount = AmountCheck
            else:
                RemainAmount = AmountCheck - PreviousReturnAmount

            if RemainAmount == 0:
                LoanObject = get_object_or_404(Loan, pk=CurrentLoanID)
                LoanObject.isClosed = 1
                LoanObject.save()
                return messages.success(request, "You have no pending Installment")

            if InstallmentDay > MarginDay:
                CalculateInterest = (
                    (RemainAmount / 100)
                    * (InterestRate + form.cleaned_data["InstallmentPenalty"])
                ) - form.cleaned_data["AnyDiscount"]
            else:
                CalculateInterest = (
                    (RemainAmount / 100) * InterestRate
                ) - form.cleaned_data["AnyDiscount"]

            obj.InstallmentAmount = CalculateInterest
            obj.CreatedBy = request.user.id
            obj.save()

            if Reference1 or Reference2:
                if ReferenceBonus.objects.filter(
                    Loan=CurrentLoanID, PaidMonth__month=Month
                ).exists():
                    return
                secondary_obj = ReferenceBonus.objects.create()
                CalculateBonus = (RemainAmount / 100) * 0.5

                if Reference1 and Reference2:
                    DivideBonus = CalculateBonus / 2
                    secondary_obj.BonusAmount1 = DivideBonus
                    secondary_obj.BonusAmount2 = DivideBonus
                elif Reference1:
                    secondary_obj.BonusAmount1 = CalculateBonus
                else:
                    secondary_obj.BonusAmount2 = CalculateBonus

                secondary_obj.Reference1 = Reference1
                secondary_obj.Reference2 = Reference2
                secondary_obj.CreatedBy = request.user.id
                secondary_obj.Loan = form.cleaned_data["Loan"]
                secondary_obj.PaidMonth = Cleaneddate
                secondary_obj.save()


admin.site.register(LoanMonthlyInstallment, LoanMonthlyInstallmentAdmin)


class ReferenceBonusAdmin(admin.ModelAdmin):
    readonly_fields = (
        "Loan",
        "Reference1",
        "Reference2",
        "BonusAmount1",
        "BonusAmount2",
        "PaidMonth",
    )
    fields = [
        readonly_fields,
        ("BonusGivenDate", "isPaid"),
    ]

    list_display = (
        "Loan",
        "Reference1",
        "BonusAmount1",
        "Reference2",
        "BonusAmount2",
        "BonusGivenDate",
        "Paymonth",
        "isPaid",
    )
    list_filter = ["Loan"]
    search_fields = [
        "Loan__LoanNumber",
        "Loan__Loaner__userName",
        "Reference1__userName",
        "Reference2__userName",
    ]
    list_per_page = 30
    autocomplete_fields = ["Loan"]

    def Paymonth(self, obj):
        return DateFormat(obj.PaidMonth).format("F")


admin.site.register(ReferenceBonus, ReferenceBonusAdmin)
