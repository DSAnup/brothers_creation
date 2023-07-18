from django.db import models
from django.db import models
from django.utils import timezone
from shareholder.models import ShareHolder

# Create your models here.


class Loaner(models.Model):
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
    isActive = models.BooleanField(default=True, verbose_name="Is Active")
    profilePic = models.FileField(upload_to="images/loaner/", null=True, blank=True)
    CreatedBy = models.IntegerField(null=True, blank=True)
    DateCreated = models.DateTimeField(default=timezone.now)
    DateLastUpdated = models.DateTimeField(default=timezone.now)
    UpdatedBy = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.firstName + " " + self.lastName


class Loan(models.Model):
    Loaner = models.ForeignKey(
        Loaner,
        on_delete=models.DO_NOTHING,
        null=False,
        blank=False,
        verbose_name="Loaner",
    )
    LoanAmount = models.IntegerField(
        null=False, blank=False, verbose_name="Loan Amount"
    )
    LoanGivenDate = models.DateField(default=timezone.now, verbose_name="Loan Given")
    InterestRate = models.IntegerField(
        null=False, blank=False, default="3", verbose_name="Interest Rate"
    )
    InterestPay = models.IntegerField(null=True, blank=True)
    Reference1 = models.ForeignKey(
        ShareHolder,
        on_delete=models.DO_NOTHING,
        related_name="Reference_one",
        verbose_name="Reference One",
        null=True,
        blank=True,
    )
    Reference2 = models.ForeignKey(
        ShareHolder,
        on_delete=models.DO_NOTHING,
        related_name="Reference_two",
        verbose_name="Reference Two",
        null=True,
        blank=True,
    )
    LoanNumber = models.IntegerField(null=False, blank=False)
    Comments = models.TextField(null=True, blank=True)
    isClosed = models.BooleanField(default=False, verbose_name="Is Closed")
    CreatedBy = models.IntegerField(null=True, blank=True)
    DateCreated = models.DateTimeField(default=timezone.now)
    DateLastUpdated = models.DateTimeField(default=timezone.now)
    UpdatedBy = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.Loaner.userName + " - 000" + str(self.LoanNumber)

    class Meta:
        get_latest_by = "LoanNumber"


class LoanReturn(models.Model):
    Loan = models.ForeignKey(
        Loan, on_delete=models.DO_NOTHING, verbose_name="Loan Account"
    )
    ReturnAmount = models.IntegerField(
        null=False, blank=False, verbose_name="Return Amount"
    )
    ReturnDate = models.DateField(default=timezone.now, verbose_name="Return Date")
    Comments = models.TextField(null=True, blank=True)
    CreatedBy = models.IntegerField(null=True, blank=True)
    DateCreated = models.DateTimeField(default=timezone.now)
    DateLastUpdated = models.DateTimeField(default=timezone.now)
    UpdatedBy = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.Loan)


class LoanMonthlyInstallment(models.Model):
    Loan = models.ForeignKey(
        Loan, on_delete=models.DO_NOTHING, verbose_name="Loan Account"
    )
    InstallmentAmount = models.IntegerField(
        null=False, blank=False, verbose_name="Installment Amount"
    )
    InstallmentPenalty = models.IntegerField(
        null=False, blank=False, verbose_name="Installment Penalty Rate", default="0"
    )
    AnyDiscount = models.IntegerField(
        null=False, blank=False, verbose_name="Any Discount", default="0"
    )
    InstallmentDate = models.DateField(
        default=timezone.now, verbose_name="Installment Paid Date"
    )
    InstallmentMonth = models.DateField(
        default=timezone.now().replace(day=1), verbose_name="Installment Month"
    )
    Comments = models.TextField(null=True, blank=True)
    CreatedBy = models.IntegerField(null=True, blank=True)
    DateCreated = models.DateTimeField(default=timezone.now)
    DateLastUpdated = models.DateTimeField(default=timezone.now)
    UpdatedBy = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.Loan)


class ReferenceBonus(models.Model):
    Loan = models.ForeignKey(
        Loan,
        on_delete=models.DO_NOTHING,
        verbose_name="Loan Account",
        null=True,
        blank=True,
    )
    BonusAmount1 = models.IntegerField(
        null=True, blank=True, verbose_name="Bonus Amount 1"
    )
    BonusAmount2 = models.IntegerField(
        null=True, blank=True, verbose_name="Bonus Amount 2"
    )
    Reference1 = models.ForeignKey(
        ShareHolder,
        on_delete=models.DO_NOTHING,
        related_name="Reference_Bonus_One",
        verbose_name="Reference One",
        null=True,
        blank=True,
    )
    Reference2 = models.ForeignKey(
        ShareHolder,
        on_delete=models.DO_NOTHING,
        related_name="Reference_Bonus_Two",
        verbose_name="Reference Two",
        null=True,
        blank=True,
    )
    BonusGivenDate = models.DateField(
        default=timezone.now, verbose_name="Bonus Given Date"
    )
    PaidMonth = models.DateField(
        default=timezone.now().replace(day=1), verbose_name="Paid Month"
    )
    isPaid = models.BooleanField(default=False, verbose_name="Is Paid")
    Comments = models.TextField(null=True, blank=True)
    CreatedBy = models.IntegerField(null=True, blank=True)
    DateCreated = models.DateTimeField(default=timezone.now)
    DateLastUpdated = models.DateTimeField(default=timezone.now)
    UpdatedBy = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.Loan)
