from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from shareholder.models import ShareHolder

# Create your models here.


class Expense(models.Model):
    ExpensePurpose = models.CharField(max_length=250, verbose_name="Expense Purpose")
    ShareHolder = models.ForeignKey(
        ShareHolder,
        on_delete=models.DO_NOTHING,
        null=False,
        blank=False,
        verbose_name="Expense By",
    )
    ExpenseDate = models.DateField(default=timezone.now, verbose_name="Expense Date")
    ExpenseAmount = models.IntegerField(
        null=False, blank=False, verbose_name="Expense Amount"
    )
    Comments = RichTextField(null=True, blank=True)
    CreatedBy = models.IntegerField(null=True, blank=True)
    DateCreated = models.DateTimeField(default=timezone.now)
    DateLastUpdated = models.DateTimeField(default=timezone.now)
    UpdatedBy = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.ExpensePurposeclass


class Rules(models.Model):
    Rules = RichTextField(null=False, blank=False)
    CreatedBy = models.IntegerField(null=True, blank=True)
    DateCreated = models.DateTimeField(default=timezone.now)
    DateLastUpdated = models.DateTimeField(default=timezone.now)
    UpdatedBy = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "Update Rules"
