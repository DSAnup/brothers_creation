from django.contrib import admin
from .models import *
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages

# Register your models here.


class ShareHolderAdmin(admin.ModelAdmin):
    fields = [
        ("userName", "password"),
        ("firstName", "lastName"),
        ("mobile", "isMember"),
        ("address", "profilePic"),
    ]
    list_display = ("userName", "firstName", "mobile")

    def save_model(self, request, obj, form, change):
        # Check if the change is being made to an existing object
        if change:
            # Get the existing object from the database
            existing_obj = ShareHolder.objects.get(pk=obj.pk)
            obj.DateCreated = existing_obj.DateCreated
            obj.DateLastUpdated = timezone.now()
            obj.CreatedBy = existing_obj.CreatedBy
            obj.UpdatedBy = request.user.id

            # Save the updated object
            obj.save()
        else:
            # Save the new object as usual
            if ShareHolder.objects.filter(
                userName=form.cleaned_data["userName"]
            ).exists():
                # Cancel object creation
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
        # Check if the change is being made to an existing object
        if change:
            # Get the existing object from the database
            existing_obj = ShareHolderSetting.objects.get(pk=obj.pk)
            obj.DateCreated = existing_obj.DateCreated
            obj.DateLastUpdated = timezone.now()
            obj.CreatedBy = existing_obj.CreatedBy
            obj.UpdatedBy = request.user.id

            # Save the updated object
            obj.save()
        else:
            # Save the new object as usual
            if ShareHolderSetting.objects.filter(shareHolder=obj.shareHolder).exists():
                # Cancel object creation
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
        if change:
            existing_obj = ShareHolderInstallment.objects.get(pk=obj.pk)
            obj.DateCreated = existing_obj.DateCreated
            obj.DateLastUpdated = timezone.now()
            obj.CreatedBy = existing_obj.CreatedBy
            obj.UpdatedBy = request.user.id
            obj.save()
        else:
            current_datetime = timezone.now()
            current_year = current_datetime.year
            curent_month = current_datetime.month
            shareholderget = ShareHolder.objects.get(
                userName=form.cleaned_data["shareHolder"]
            )
            setting = ShareHolderSetting.objects.get(shareHolder_id=shareholderget.pk)

            cleaneddata = form.cleaned_data["InstallmentDate"]
            year = cleaneddata.year
            month = cleaneddata.month
            day = cleaneddata.day

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
