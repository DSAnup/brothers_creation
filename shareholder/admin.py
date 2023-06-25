from django.contrib import admin
from .models import *
from django.utils import timezone
from django.contrib import messages


class ShareHolderAdmin(admin.ModelAdmin):
    fields = [
        ("userName", "password"),
        ("firstName", "lastName"),
        ("mobile", "isMember"),
        ("address", "profilePic"),
    ]
    list_display = ("userName", "firstName", "mobile")

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
        ("registrationAmount", "installmentAmount"),
    ]
    list_display = (
        "shareHolder",
        "shareNumber",
        "installmentAmount",
        "registrationAmount",
    )

    def save_model(self, request, obj, form, change):
        if change:
            existing_obj = ShareHolderSetting.objects.get(pk=obj.pk)
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
            obj.save()


admin.site.register(ShareHolderSetting, ShareHolderSettingAdmin)


class ShareHolderInstallmentAdmin(admin.ModelAdmin):
    fields = [
        ("shareHolder", "InstallmentDate"),
    ]
    list_display = ("shareHolder", "InstallmentDate", "InstallmentAmount")

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
            if year == current_year and month == curent_month and day > 10:
                installmentAmount = (
                    setting.installmentAmount * setting.shareNumber
                ) + (50 * setting.shareNumber)
            else:
                installmentAmount = setting.installmentAmount * setting.shareNumber
            obj.InstallmentAmount = installmentAmount
            obj.DateCreated = existing_obj.DateCreated
            obj.DateLastUpdated = timezone.now()
            obj.CreatedBy = existing_obj.CreatedBy
            obj.UpdatedBy = request.user.id
            obj.save()
        else:
            if ShareHolderInstallment.objects.filter(
                shareHolder=obj.shareHolder, InstallmentDate__month=month
            ).exists():
                return messages.error(request, "You already paid this month")
            if year == current_year and month == curent_month and day > 10:
                installmentAmount = (
                    setting.installmentAmount * setting.shareNumber
                ) + (50 * setting.shareNumber)
            else:
                installmentAmount = setting.installmentAmount * setting.shareNumber
            obj.DateCreated = timezone.now()
            obj.CreatedBy = request.user.id
            obj.InstallmentAmount = installmentAmount
            obj.InstallmentDate = form.cleaned_data["InstallmentDate"]
            obj.save()


admin.site.register(ShareHolderInstallment, ShareHolderInstallmentAdmin)
