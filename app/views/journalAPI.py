
from ..models import *
import datetime

def jeAPI(request, journal, normally, accountChild, amount):
    if not amount:
        return
        
    je = JournalEntries()

    je.journal = journal
    je.normally = normally
    je.accountChild = accountChild
    je.amount = amount

    if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
        je.accountChild.amount += je.amount
        je.accountChild.accountSubGroup.amount += je.amount
        je.accountChild.accountSubGroup.accountGroup.amount += je.amount
        je.accountChild.save()
        je.accountChild.accountSubGroup.save()
        je.accountChild.accountSubGroup.accountGroup.save()
        je.balance = je.accountChild.amount
        if je.accountChild.me:
            je.accountChild.me.amount += je.amount
            je.accountChild.me.save()
    else:
        je.accountChild.amount -= je.amount
        je.accountChild.accountSubGroup.amount -= je.amount
        je.accountChild.accountSubGroup.accountGroup.amount -= je.amount
        je.accountChild.save()
        je.accountChild.accountSubGroup.save()
        je.accountChild.accountSubGroup.accountGroup.save()
        je.balance = je.accountChild.amount
        if je.accountChild.me:
            je.accountChild.me.amount -= je.amount
            je.accountChild.me.save()

        if 'cash'.lower() in je.accountChild.accountSubGroup.name.lower():
            currentMonth = datetime.date.today().month
            currentYear = datetime.date.today().year
            try:
                monthEx = MonthlyExpense.objects.get(year = currentYear, date = datetime.date(currentYear, currentMonth, 1))
                if monthEx:
                    monthEx.amount += je.amount
                monthEx.save()
            except:
                monthEx = MonthlyExpense()
                monthEx.year = currentYear
                monthEx.date = datetime.date(currentYear, currentMonth, 1)
                monthEx.amount = je.amount
                monthEx.save()
                request.user.branch.monthlyExpense.add(monthEx)
            
    je.save()

    request.user.branch.journalEntries.add(je)

def voidJournal(request, journal):
    for je in journal.journalentries.all():

        # I REVERESED THE PLUS AND MINUS FROM ABOVE #
        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
            je.accountChild.amount -= je.amount
            je.accountChild.accountSubGroup.amount -= je.amount
            je.accountChild.accountSubGroup.accountGroup.amount -= je.amount
            je.accountChild.save()
            je.accountChild.accountSubGroup.save()
            je.accountChild.accountSubGroup.accountGroup.save()
            if je.accountChild.me:
                je.accountChild.me.amount -= je.amount
                je.accountChild.me.save()
        else:
            je.accountChild.amount += je.amount
            je.accountChild.accountSubGroup.amount += je.amount
            je.accountChild.accountSubGroup.accountGroup.amount += je.amount
            je.accountChild.save()
            je.accountChild.accountSubGroup.save()
            je.accountChild.accountSubGroup.accountGroup.save()
            if je.accountChild.me:
                je.accountChild.me.amount += je.amount
                je.accountChild.me.save()
        print(journal.pk)

    journal.delete()