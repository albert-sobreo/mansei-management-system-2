from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from datetime import date as now
from ..forms import *
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
import sweetify
import pandas as pd
import json
from decimal import Decimal
import datetime
from .petty_cash_api import *
from .journalAPI import *
from django.core.exceptions import PermissionDenied
from .notificationCreate import *

class GAS_AdvancementsView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        user = request.user

        try:
            adv = user.branch.advancementThruPettyCash.latest('pk')

            listed_code = adv.code.split('-')
            listed_date = str(now.today()).split('-')

            current_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                current_code += 1
                new_code = 'ADV-{}-{}-{}'.format(listed_date[0], listed_date[1], str(current_code).zfill(4))
            else:
                new_code = 'ADV-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            print(e)
            listed_date = str(now.today()).split('-')
            new_code = 'ADV-{}-{}-0001'.format(listed_date[0], listed_date[1])

        context = {
            'new_code': new_code,
            'adv': request.user.branch.advancementThruPettyCash.filter(approved=True)
        }

        return render(request, 'advancements.html', context)

class SaveAdvancement(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()

        if not pCashChecker(request, request.data['amount']):
            sweetify.sweetalert(request, icon='warning', title='Petty Cash Fund is insufficient!', persistent='Dismiss')
            return JsonResponse(0, safe=False)
        
        adv = AdvancementThruPettyCash()

        adv.code = request.data['code']
        adv.requestor = User.objects.get(pk=request.data['requestor'])
        adv.amount = request.data['amount']
        adv.balance = adv.amount
        adv.datetimeCreated = datetime.datetime.now()
        adv.reason = request.data['reason']

        if request.user.is_authenticated:
            adv.issuer = request.user

        adv.save()
        request.user.branch.advancementThruPettyCash.add(adv)

        notify(request, 'New Advancement Request', adv.code, '/adv-nonapproved/', 1)
    
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class PettyCashView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        context = {
            'activeAdv': request.user.branch.advancementThruPettyCash.filter(closed=False, approved=True)
        }
        return render(request, 'petty-cash.html', context)

class PettyCashReplenish(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()

        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount
        currentAmount = dChildAccount.pettyCash.amount
        normalAmount = request.user.branch.pettyCashReplenish
        paymentMethod = AccountChild.objects.get(pk=request.data['id'])

        j = Journal()

        j.code = 'Petty-Cash-01-0001'
        j.datetimeCreated = datetime.datetime.now()
        j.createdBy = request.user
        j.journalDate = datetime.datetime.now()
        j.save()
        request.user.branch.journal.add(j)

        jeAPI(request, j, "Debit", dChildAccount.pettyCash, normalAmount - currentAmount)
        jeAPI(request, j, "Credit", paymentMethod, normalAmount - currentAmount)

        notify(request, 'Petty Cash', "Petty cash has been replenished", '/petty-cash/', 1)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class SaveDefaultPettyCash(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        request.user.branch.pettyCashReplenish = request.data['amount']
        request.user.branch.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class ReturnAdvancement(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        data = request.data

        adv = AdvancementThruPettyCash.objects.get(pk=data['id'])

        adv.balance -= Decimal(data['returnAmount'])
        if adv.balance >= 0:
            adv.closed = True
        
        adv.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class ReimbursementView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        context = {
            'liquidation': request.user.branch.liquidation.filter(payable__gt=Decimal(0))
        }
        return render(request, 'reimbursement.html', context)