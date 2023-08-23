import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.


class ShareHolder(models.Model):
    userName = models.CharField(max_length=50, verbose_name="User Name")
    firstName = models.CharField(
        max_length=80, blank=True, null=True, verbose_name="First Name"
    )
    lastName = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Last Name"
    )
    mobile = models.CharField(max_length=20, verbose_name="Mobile Number")
    address = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Address"
    )
    password = models.CharField(max_length=100, blank=True, null=True, default="123456")
    isMember = models.BooleanField(default=True, verbose_name="Is Member")
    isActive = models.BooleanField(default=True, verbose_name="Is Active")
    profilePic = models.FileField(upload_to="images/", null=True, blank=True)
    CreatedBy = models.IntegerField(null=True, blank=True)
    DateCreated = models.DateTimeField(default=timezone.now)
    DateLastUpdated = models.DateTimeField(default=timezone.now)
    UpdatedBy = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.userName


class ShareHolderSetting(models.Model):
    shareHolder = models.ForeignKey(
        ShareHolder,
        on_delete=models.DO_NOTHING,
        null=False,
        blank=False,
        verbose_name="Share Holder",
    )
    shareNumber = models.IntegerField(default=1, verbose_name="Share Number")
    CreatedBy = models.IntegerField(null=True, blank=True)
    DateCreated = models.DateTimeField(default=timezone.now)
    DateLastUpdated = models.DateTimeField(default=timezone.now)
    UpdatedBy = models.IntegerField(null=True, blank=True)
    registrationAmount = models.IntegerField(
        default=1000, verbose_name="Registration Fee"
    )
    installmentAmount = models.IntegerField(
        default=500, verbose_name="Installment Amount"
    )

    def __str__(self):
        return self.shareHolder.userName


class ShareHolderInstallment(models.Model):
    shareHolder = models.ForeignKey(
        ShareHolder,
        on_delete=models.DO_NOTHING,
        null=False,
        blank=False,
        verbose_name="Share Holder",
    )
    InstallmentDate = models.DateField(
        default=timezone.now, verbose_name="Installment Date"
    )
    MarginDate = models.DateField(default=timezone.now, verbose_name="Margin Date")
    InstallmentAmount = models.IntegerField(null=False, blank=False)
    CreatedBy = models.IntegerField(null=True, blank=True)
    DateCreated = models.DateTimeField(default=timezone.now)
    DateLastUpdated = models.DateTimeField(default=timezone.now)
    UpdatedBy = models.IntegerField(null=True, blank=True)
    havePenalty = models.IntegerField(
        null=True, blank=True, default=0, verbose_name="Have Penalty"
    )
    haveDiscount = models.IntegerField(
        null=True, blank=True, default=0, verbose_name="Consider Discount"
    )
    # comments = models.TextField(null=True, blank=True)
    comments = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.shareHolder.userName
