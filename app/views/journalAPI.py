
from urllib import request
from venv import create

from h11 import Request
from ..models import *
import datetime
from django.http.response import HttpResponseServerError

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


class JournalAPI:
    # CLASS ATTRIBUTES
    journal = {
        'Debit': {
            'accounts': []
        },
        'Credit': {
            'accounts': []
        }
    }

    request = None
    code: str = None
    createdBy: str = None
    journalDate  = None

    # END ATTRIBUTES

    # INIT

    def __init__(self, request, code, createdBy, journalDate) -> None:
        self.request = request
        self.code = code
        self.createdBy = createdBy
        self.journalDate = journalDate

    def addJE(self, normally, account, amount):
        self.journal[normally]['accounts'].append({'name': account, 'amount': amount})
    
    def checker(self):
        sumDebit = sum(i['amount'] for i in self.journal['Debit']['accounts'])
        sumCredit = sum(i['amount'] for i in self.journal['Credit']['accounts'])

        if not round(sumDebit, 3) == round(sumCredit, 3):
            return 0
        else:
            return 1

    def reset(self):
        self.journal = {
            'Debit': {
                'accounts': []
            },
            'Credit': {
                'accounts': []
            }
        }

        self.request = None
        self.code = None
        self.createdBy = None
        self.journalDate  = None

    def save(self):
        if not self.checker(): raise Exception("Journal did not balance.")

        j = Journal()
        j.code = self.code
        j.datetimeCreated = datetime.datetime.now()
        j.createdBy = self.createdBy
        j.journalDate = self.journalDate
        j.save()
        self.request.user.branch.journal.add(j)

        for account in self.journal['Debit']['accounts']:
            jeAPI(self.request, j, 'Debit', account['name'], account['amount'])

        for account in self.journal['Credit']['accounts']:
            jeAPI(self.request, j, 'Credit', account['name'], account['amount'])

        self.reset()