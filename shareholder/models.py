import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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
    profilePic = models.FileField(
        upload_to="images/", blank=True, null=True, verbose_name="Profile Picture"
    )
    CreatedBy = models.IntegerField(null=True, blank=True)
    DateCreated = models.DateTimeField(default=timezone.now)
    DateLastUpdated = models.DateTimeField(default=timezone.now)
    UpdatedBy = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.userName
