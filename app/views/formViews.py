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
            startDate = request.GET['startDate']
            endDate = request.GET['endDate']
        except Exception as e:
            print(e)
            startDate = datetime.date(datetime.date.today().year, 1, 1)
            endDate = datetime.date(datetime.date.today().year, 12, 31)


        data = {
            "asset": {
                "amount": Decimal(0),
                "groupAccount": [{
                    "name": None,
                    "amount": Decimal(0),
                    "subGroup": [{
                        "name": None,
                        "amount": 0
                    }]
                }]
            },

            "liabilities": {
                "amount": Decimal(0),
                "groupAccount": [{
                    "name": None,
                    "amount": Decimal(0),
                    "subGroup": [{
                        "name": None,
                        "amount": 0
                    }]
                }]
            },

            "equity": {
                "amount": Decimal(0),
                "groupAccount": [{
                    "name": None,
                    "amount": Decimal(0),
                    "subGroup": [{
                        "name": None,
                        "amount": 0
                    }]
                }]
            }
        }

        """FETCH JOURNALS AND DO FOR LOOP BELOW"""
        

        
        """                END                 """
        

        context = {
            'startDate': startDate,
            'endDate': endDate,
        }
        return render(request, 'balance-sheet.html', context)