from rest_framework.views import APIView
from ..models import *
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from decimal import Decimal
from datetime import datetime
import re
from .journalAPI import jeAPI
from .petty_cash_api import *
from django.core.exceptions import PermissionDenied
from dateutil import parser

class BIR2307View(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        return render(request, '2307.html')

class BIR0619EView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        return render(request, '0619-E.html')

class BIR1601CView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        return render(request, '1601-C.html')

class BIR1702QView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        return render(request, '1702Q.html')

class BIR1601EQView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        return render(request, '1601-EQ.html')

class BIR2316View(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        return render(request, '2316.html')

class BalanceSheetView(APIView):
    def get(self, request):
        try:
            startDate = parser.parse(request.GET['startDate'])
            endDate = parser.parse(request.GET['endDate'])
        except Exception as e:
            startDate = datetime.date(datetime.date.today().year, 1, 1)
            endDate = datetime.date(datetime.date.today().year, 12, 31)        

        context = {
            'startDate': startDate,
            'endDate': endDate,
        }
        return render(request, 'balance-sheet.html', context)

class BalanceSheetRequest(APIView):
    def get(self, request):
        try:
            startDate = request.GET['startDate']
            endDate = request.GET['endDate']
        except Exception as e:
            startDate = datetime.date(datetime.date.today().year, 1, 1)
            endDate = datetime.date(datetime.date.today().year, 12, 31)     


        data = {
            "asset": {
                "amount": Decimal(0),
            },

            "liabilities": {
                "amount": Decimal(0),
            },

            "equity": {
                "amount": Decimal(0),
            },
            "retainedEarnings":{
                "amount": Decimal(0)
            }
        }

        """FETCH JOURNALS AND DO FOR LOOP BELOW"""

        
        journal = request.user.branch.journal.filter(journalDate__range=[startDate, endDate])
        for j in journal:
            for je in j.journalentries.all().iterator():
                # je.accountChild.accountSubGroup.accountGroup.name
                if re.search('[Aa]sset', je.accountChild.accountSubGroup.accountGroup.name):
                    if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                        data['asset']['amount'] += je.amount
                    else:
                        data['asset']['amount'] -= je.amount



                    try:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['asset'][je.accountChild.accountSubGroup.accountGroup.name]['amount'] += je.amount
                        else:
                            data['asset'][je.accountChild.accountSubGroup.accountGroup.name]['amount'] -= je.amount
                        
                    except:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['asset'][je.accountChild.accountSubGroup.accountGroup.name] = {'amount': je.amount}
                        else:
                            data['asset'][je.accountChild.accountSubGroup.accountGroup.name] = {'amount': -je.amount}
                        
                    

                    try:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['asset'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name]['amount'] += je.amount
                        else:
                            data['asset'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name]['amount'] -= je.amount
                        
                    except:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['asset'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name] = {'amount': je.amount}
                        else:
                            data['asset'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name] = {'amount': -je.amount}
                        
                
                elif re.search('[Ll]iabilit',  je.accountChild.accountSubGroup.accountGroup.name):
                    if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                        data['liabilities']['amount'] += je.amount
                    else:
                        data['liabilities']['amount'] -= je.amount
                    try:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['liabilities'][je.accountChild.accountSubGroup.accountGroup.name]['amount'] += je.amount
                        else:
                            data['liabilities'][je.accountChild.accountSubGroup.accountGroup.name]['amount'] -= je.amount
                        
                    except:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['liabilities'][je.accountChild.accountSubGroup.accountGroup.name] = {'amount': je.amount}
                        else:
                            data['liabilities'][je.accountChild.accountSubGroup.accountGroup.name] = {'amount': -je.amount}
                    

                    try:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['liabilities'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name]['amount'] += je.amount
                        else:
                            data['liabilities'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name]['amount'] -= je.amount
                        
                    except:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['liabilities'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name] = {'amount': je.amount}
                        else:
                            data['liabilities'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name] = {'amount': -je.amount}
                        

                elif re.search('[Ee]quity',  je.accountChild.accountSubGroup.accountGroup.name):
                    if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                        data['equity']['amount'] += je.amount
                    else:
                        data['equity']['amount'] -= je.amount
                    try:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['equity'][je.accountChild.accountSubGroup.accountGroup.name]['amount'] += je.amount
                        else:
                            data['equity'][je.accountChild.accountSubGroup.accountGroup.name]['amount'] -= je.amount
                        
                    except:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['equity'][je.accountChild.accountSubGroup.accountGroup.name] = {'amount': je.amount}
                        else:
                            data['equity'][je.accountChild.accountSubGroup.accountGroup.name] = {'amount': -je.amount}
                        

                    try:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['equity'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name]['amount'] += je.amount
                        else:
                            data['equity'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name]['amount'] -= je.amount
                        
                    except:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['equity'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name] = {'amount': je.amount}
                        else:
                            data['equity'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name] = {'amount': -je.amount}

                elif re.search('[Ee]xpense', je.accountChild.accountSubGroup.accountGroup.name) or re.search('[Rr]evenue', je.accountChild.accountSubGroup.accountGroup.name) or re.search('[Ii]ncome', je.accountChild.accountSubGroup.accountGroup.name) or re.search('[Ss]ale', je.accountChild.accountSubGroup.accountGroup.name):
                    if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                        data['retainedEarnings']['amount'] += je.amount
                    else:
                        data['retainedEarnings']['amount'] -= je.amount
                        

        """                END                 """
        return JsonResponse(data, safe=False)

class IncomeStatementView(APIView):
    def get(self, request):
        try:
            startDate = parser.parse(request.GET['startDate'])
            endDate = parser.parse(request.GET['endDate'])
        except Exception as e:
            startDate = datetime.date(datetime.date.today().year, 1, 1)
            endDate = datetime.date(datetime.date.today().year, 12, 31)

        context = {
            'startDate': startDate,
            'endDate': endDate,
        }
        return render(request, 'income-statement.html', context)

class IncomeStatementRequest(APIView):
    def get(self, request):
        try:
            startDate = request.GET['startDate']
            endDate = request.GET['endDate']
        except Exception as e:
            startDate = datetime.date(datetime.date.today().year, 1, 1)
            endDate = datetime.date(datetime.date.today().year, 12, 31)
        
        data = {} 

        journal = request.user.branch.journal.filter(journalDate__range=[startDate, endDate])
        for j in journal:
            for je in j.journalentries.all().iterator():

                if re.search('[Ee]xpense', je.accountChild.accountSubGroup.accountGroup.name) or re.search('[Rr]evenue', je.accountChild.accountSubGroup.accountGroup.name) or re.search('[Ii]ncome', je.accountChild.accountSubGroup.accountGroup.name) or re.search('[Ss]ale', je.accountChild.accountSubGroup.accountGroup.name):
                    try:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data[je.accountChild.accountSubGroup.accountGroup.name]['amount'] += je.amount
                        else:
                            data[je.accountChild.accountSubGroup.accountGroup.name]['amount'] -= je.amount
                    except Exception as e:
                        print(e)
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data[je.accountChild.accountSubGroup.accountGroup.name] = {'amount': je.amount}
                        else:
                            data[je.accountChild.accountSubGroup.accountGroup.name] = {'amount': -je.amount}

        return JsonResponse(data, safe=False)

class CashFlowView(APIView):
    def get(self, request):
        try:
            startDate = parser.parse(request.GET['startDate'])
            endDate = parser.parse(request.GET['endDate'])
        except Exception as e:
            startDate = datetime.date(datetime.date.today().year, 1, 1)
            endDate = datetime.date(datetime.date.today().year, 12, 31)        

        context = {
            'startDate': startDate,
            'endDate': endDate,
        }
        return render(request, 'cash-flow.html', context)

class CashFlowRequest(APIView):
    def get(self, request):
        try:
            startDate = request.GET['startDate']
            endDate = request.GET['endDate']
        except Exception as e:
            startDate = datetime.date(datetime.date.today().year, 1, 1)
            endDate = datetime.date(datetime.date.today().year, 12, 31)     


        data = {
            'retainedEarnings': {
                'amount': Decimal(0)
            },
            "operating": {},
            "financing": {},
            "investing": {},
        }

        """FETCH JOURNALS AND DO FOR LOOP BELOW"""

        
        journal = request.user.branch.journal.filter(journalDate__range=[startDate, endDate])
        for j in journal:
            for je in j.journalentries.all().iterator():
                # je.accountChild.accountSubGroup.accountGroup.name
                if re.search('^[Cc]urrent', je.accountChild.accountSubGroup.accountGroup.name):
                    try:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['operating'][je.accountChild.accountSubGroup.accountGroup.name]['amount'] += je.amount
                        else:
                            data['operating'][je.accountChild.accountSubGroup.accountGroup.name]['amount'] -= je.amount
                        
                    except:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['operating'][je.accountChild.accountSubGroup.accountGroup.name] = {'amount': je.amount}
                        else:
                            data['operating'][je.accountChild.accountSubGroup.accountGroup.name] = {'amount': -je.amount}
                        
                    

                    try:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['operating'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name]['amount'] += je.amount
                        else:
                            data['operating'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name]['amount'] -= je.amount
                        
                    except:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['operating'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name] = {'amount': je.amount}
                        else:
                            data['operating'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name] = {'amount': -je.amount}
                        
                
                elif re.search('(^[Nn]on)|([Aa]sset$)',  je.accountChild.accountSubGroup.accountGroup.name):
                    try:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['investing'][je.accountChild.accountSubGroup.accountGroup.name]['amount'] += je.amount
                        else:
                            data['investing'][je.accountChild.accountSubGroup.accountGroup.name]['amount'] -= je.amount
                        
                    except:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['investing'][je.accountChild.accountSubGroup.accountGroup.name] = {'amount': je.amount}
                        else:
                            data['investing'][je.accountChild.accountSubGroup.accountGroup.name] = {'amount': -je.amount}
                    

                    try:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['investing'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name]['amount'] += je.amount
                        else:
                            data['investing'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name]['amount'] -= je.amount
                        
                    except:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                            data['investing'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name] = {'amount': je.amount}
                        else:
                            data['investing'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name] = {'amount': -je.amount}
                        

                elif re.search('(^[Nn]on)|([Ll]iabilities$)', je.accountChild.accountSubGroup.accountGroup.name) or re.search('[Ee]quity',  je.accountChild.accountSubGroup.accountGroup.name):
                    try:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally or not re.search('[Rr]etain', je.accountChild.accountSubGroup.name):
                            data['financing'][je.accountChild.accountSubGroup.accountGroup.name]['amount'] += je.amount
                        else:
                            data['financing'][je.accountChild.accountSubGroup.accountGroup.name]['amount'] -= je.amount
                        
                    except:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally or not re.search('[Rr]etain', je.accountChild.accountSubGroup.name):
                            data['financing'][je.accountChild.accountSubGroup.accountGroup.name] = {'amount': je.amount}
                        else:
                            data['financing'][je.accountChild.accountSubGroup.accountGroup.name] = {'amount': -je.amount}
                        

                    try:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally or not re.search('[Rr]etain', je.accountChild.accountSubGroup.name):
                            data['financing'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name]['amount'] += je.amount
                        else:
                            data['financing'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name]['amount'] -= je.amount
                        
                    except:
                        if je.normally == je.accountChild.accountSubGroup.accountGroup.normally or not re.search('[Rr]etain', je.accountChild.accountSubGroup.name):
                            data['financing'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name] = {'amount': je.amount}
                        else:
                            data['financing'][je.accountChild.accountSubGroup.accountGroup.name][je.accountChild.accountSubGroup.name] = {'amount': -je.amount}
                
                elif re.search('[Ee]xpense', je.accountChild.accountSubGroup.accountGroup.name) or re.search('[Rr]evenue', je.accountChild.accountSubGroup.accountGroup.name) or re.search('[Ii]ncome', je.accountChild.accountSubGroup.accountGroup.name) or re.search('[Ss]ale', je.accountChild.accountSubGroup.accountGroup.name):
                    if je.normally == je.accountChild.accountSubGroup.accountGroup.normally:
                        data['retainedEarnings']['amount'] += je.amount
                    else:
                        data['retainedEarnings']['amount'] -= je.amount
                        
        return JsonResponse(data, safe=False)