
from ..models import *

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
            je.accountChild.me.amount += je.amount
            je.accountChild.me.save()
    je.save()

    request.user.branch.journalEntries.add(je)