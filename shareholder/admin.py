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
        ("address", "photo"),
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
            obj.save()


admin.site.register(ShareHolder, ShareHolderAdmin)
