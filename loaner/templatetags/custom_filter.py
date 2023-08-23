from django import template
import calendar

register = template.Library()


@register.simple_tag
def CalculateInterest(LoanAmount, Percent, multiMonth=1):
    MainPercentAmount = int(LoanAmount) * 3 / 100
    if multiMonth == 2:
        Amount = (
            int((LoanAmount * Percent) / 100)
            + int((LoanAmount * 4) / 100)
            + MainPercentAmount
        )
    else:
        Amount = int((LoanAmount * Percent) / 100) + int(MainPercentAmount) * multiMonth
    return int(Amount)


@register.simple_tag
def AddDays(MarginDate):
    Year = MarginDate.year
    Month = MarginDate.month
    NextMonth = calendar.month_name[Month + 1]
    Day = MarginDate.day
    return str(Day) + "-" + str(NextMonth) + "-" + str(Year)
