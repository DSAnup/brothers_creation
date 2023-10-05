from typing import Any
from django.contrib import admin
from django.http.request import HttpRequest
from .models import *
from django.utils import timezone
from django.contrib import messages

from dal import autocomplete


class ShareHolderModelAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ShareHolder.objects.all()

        if self.q:
            qs = qs.filter(firstName__istartswith=self.q)

        return qs


class ShareHolderAdmin(admin.ModelAdmin):
    fields = [
        ("userName", "password"),
        ("firstName", "lastName"),
        ("mobile", "isMember", "isActive"),
        ("address", "profilePic"),
    ]
    list_display = ("userName", "firstName", "mobile")
    list_filter = ["userName"]
    search_fields = [
        "userName",
        "lastName",
        "mobile",
        "firstName",
    ]
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if change:
            existing_obj = ShareHolder.objects.get(pk=obj.pk)
            obj.DateCreated = existing_obj.DateCreated
            obj.DateLastUpdated = timezone.now()
            obj.CreatedBy = existing_obj.CreatedBy
            obj.UpdatedBy = request.user.id
            obj.save()
        else:
            if ShareHolder.objects.filter(
                userName=form.cleaned_data["userName"]
            ).exists():
                return messages.error(
                    request, "The user name is already taken please choose another"
                )
            obj.CreatedBy = request.user.id
            obj.save()


admin.site.register(ShareHolder, ShareHolderAdmin)


class ShareHolderSettingAdmin(admin.ModelAdmin):
    fields = [
        ("shareHolder", "shareNumber"),
    ]
    list_display = (
        "shareHolder",
        "shareNumber",
        "installmentAmount",
        "registrationAmount",
    )
    list_filter = ["shareHolder"]
    search_fields = [
        "shareHolder__userName",
        "shareHolder__lastName",
        "shareHolder__mobile",
        "shareHolder__firstName",
    ]
    list_per_page = 30
    autocomplete_fields = ["shareHolder"]

    def save_model(self, request, obj, form, change):
        if change:
            existing_obj = ShareHolderSetting.objects.get(pk=obj.pk)
            obj.registrationAmount = form.cleaned_data["shareNumber"] * 1000
            obj.installmentAmount = form.cleaned_data["shareNumber"] * 500
            obj.DateCreated = existing_obj.DateCreated
            obj.DateLastUpdated = timezone.now()
            obj.CreatedBy = existing_obj.CreatedBy
            obj.UpdatedBy = request.user.id
            obj.save()
        else:
            if ShareHolderSetting.objects.filter(shareHolder=obj.shareHolder).exists():
                return messages.error(
                    request, "The user name is already taken please choose another"
                )
            obj.CreatedBy = request.user.id
            obj.registrationAmount = form.cleaned_data["shareNumber"] * 1000
            obj.installmentAmount = form.cleaned_data["shareNumber"] * 500
            obj.save()


admin.site.register(ShareHolderSetting, ShareHolderSettingAdmin)


class ShareHolderInstallmentAdmin(admin.ModelAdmin):
    fields = [
        ("shareHolder", "InstallmentDate"),
        ("havePenalty", "haveDiscount"),
        ("comments"),
    ]
    list_display = (
        "shareHolder",
        "InstallmentDate",
        "InstallmentAmount",
        "havePenalty",
        "haveDiscount",
        "MarginDate",
        "comments",
    )
    list_filter = ["shareHolder", "InstallmentDate"]
    search_fields = [
        "shareHolder__userName",
        "shareHolder__lastName",
        "shareHolder__mobile",
        "shareHolder__firstName",
    ]
    list_per_page = 30
    autocomplete_fields = ["shareHolder"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "shareHolder":
            kwargs["queryset"] = ShareHolder.objects.filter(isActive=1)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        current_datetime = timezone.now()
        current_year = current_datetime.year
        curent_month = current_datetime.month

        cleaneddata = form.cleaned_data["InstallmentDate"]
        year = cleaneddata.year
        month = cleaneddata.month
        day = cleaneddata.day

        shareholderget = ShareHolder.objects.get(
            userName=form.cleaned_data["shareHolder"]
        )
        setting = ShareHolderSetting.objects.get(shareHolder_id=shareholderget.pk)

        if change:
            existing_obj = ShareHolderInstallment.objects.get(pk=obj.pk)
            if year == current_year and month == month and day > 10:
                installmentAmount = (
                    (setting.installmentAmount)
                    + (50 * setting.shareNumber)
                    + form.cleaned_data["havePenalty"]
                    - form.cleaned_data["haveDiscount"]
                )
            else:
                installmentAmount = (
                    setting.installmentAmount
                    + form.cleaned_data["havePenalty"]
                    - form.cleaned_data["haveDiscount"]
                )
            obj.InstallmentAmount = installmentAmount
            obj.DateCreated = existing_obj.DateCreated
            obj.DateLastUpdated = timezone.now()
            obj.CreatedBy = existing_obj.CreatedBy
            obj.UpdatedBy = request.user.id
            obj.MarginDate = str(year) + "-" + str(month) + "-10"
            obj.save()
        else:
            if ShareHolderInstallment.objects.filter(
                shareHolder=obj.shareHolder,
                InstallmentDate__month=month,
                InstallmentDate__year=year,
            ).exists():
                return messages.error(request, "You already paid this month")
            if year == current_year and month == month and day > 10:
                installmentAmount = (
                    (setting.installmentAmount)
                    + (50 * setting.shareNumber)
                    + form.cleaned_data["havePenalty"]
                    - form.cleaned_data["haveDiscount"]
                )
            else:
                installmentAmount = (
                    setting.installmentAmount
                    + form.cleaned_data["havePenalty"]
                    - form.cleaned_data["haveDiscount"]
                )
            obj.DateCreated = timezone.now()
            obj.CreatedBy = request.user.id
            obj.InstallmentAmount = installmentAmount
            obj.InstallmentDate = form.cleaned_data["InstallmentDate"]
            obj.MarginDate = str(year) + "-" + str(month) + "-10"
            obj.save()


admin.site.register(ShareHolderInstallment, ShareHolderInstallmentAdmin)


class ShareHolderExtraInvestmentAdmin(admin.ModelAdmin):
    fields = [
        ("ShareHolder", "InvestmentAmount"),
        ("InvestmentDate", "InvestmentNote"),
    ]
    list_display = (
        "ShareHolder",
        "InvestmentAmount",
        "InvestmentDate",
        "InvestmentNote",
    )
    list_filter = ["ShareHolder", "InvestmentDate"]
    search_fields = [
        "ShareHolder__userName",
        "ShareHolder__lastName",
        "ShareHolder__mobile",
        "ShareHolder__firstName",
    ]
    readonly_fields = ["InvestmentAmount"]
    list_per_page = 30
    autocomplete_fields = ["ShareHolder"]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        else:
            return ()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "ShareHolder":
            kwargs["queryset"] = ShareHolder.objects.filter(isActive=1)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        cleaneddata = form.cleaned_data["InvestmentDate"]
        year = cleaneddata.year
        month = cleaneddata.month

        shareholderget = ShareHolder.objects.get(
            userName=form.cleaned_data["ShareHolder"]
        )
        setting = ShareHolderSetting.objects.get(shareHolder_id=shareholderget.pk)

        if change:
            existing_obj = ShareHolderExtraInvestment.objects.get(pk=obj.pk)
            obj.InvestmentAmount = (
                form.cleaned_data["InvestmentAmount"] * setting.shareNumber
            )
            obj.DateCreated = existing_obj.DateCreated
            obj.DateLastUpdated = timezone.now()
            obj.CreatedBy = existing_obj.CreatedBy
            obj.UpdatedBy = request.user.id
            obj.save()
        else:
            if ShareHolderExtraInvestment.objects.filter(
                ShareHolder=obj.ShareHolder,
                InvestmentDate__month=month,
                InvestmentDate__year=year,
            ).exists():
                return messages.error(request, "You already paid")
            obj.DateCreated = timezone.now()
            obj.CreatedBy = request.user.id
            obj.InvestmentAmount = (
                form.cleaned_data["InvestmentAmount"] * setting.shareNumber
            )
            obj.InvestmentDate = form.cleaned_data["InvestmentDate"]
            obj.save()


admin.site.register(ShareHolderExtraInvestment, ShareHolderExtraInvestmentAdmin)
