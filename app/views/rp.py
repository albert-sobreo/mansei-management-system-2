from django import views
from django.db.models import query
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from rest_framework.views import APIView
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from ..serializers import *
from ..models import *
import sweetify
from datetime import date as now
from decimal import Decimal
from datetime import datetime
from datetime import date
from .journalAPI import jeAPI
import re

class ReceivedPaymentView(View):
    def get(self, request, format=None):

        try:
            rp = request.user.branch.receivePayment.latest('pk')

            listed_code = rp.code.split('-')
            listed_date = str(now.today()).split('-')

            current_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                current_code += 1
                new_code = 'RP-{}-{}-{}'.format(listed_date[0], listed_date[1], str(current_code).zfill(4))
            else:
                new_code = 'RP-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            print(e)
            listed_date = str(now.today()).split('-')
            new_code = 'RP-{}-{}-0001'.format(listed_date[0], listed_date[1])

        context = {
            'new_code': new_code,
            'sc': request.user.branch.salesContract.filter(approved=True, fullyPaid=False),
        }
        return render(request, 'received-payment.html', context)

class SaveReceivePayment(APIView):
    def post(self, request, formay = None):
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount
        receivePayment = request.data

        rp = ReceivePayment()
        rp.code = receivePayment['code']
        rp.datetimeCreated = datetime.now()
        rp.remarks = receivePayment['description']
        if receivePayment['retroactive']:
            rp.paymentDate = receivePayment['retroactive']
        else:
            rp.paymentDate = receivePayment['date']
        if request.user.is_authenticated:
            rp.createdBy = request.user
        rp.salesContract = SalesContract.objects.get(pk=receivePayment['sc']['code'])
        rp.paymentMethod = receivePayment['paymentMethod']
        rp.paymentPeriod = receivePayment['paymentPeriod']
        
        rp.wep = Decimal(receivePayment['wep'])
        rp.amountPaid = Decimal(receivePayment['amountPaid']) - rp.wep
        rp.salesContract.wep += rp.wep
        rp.salesContract.save()
        rp.save()
        request.user.branch.receivePayment.add(rp)

        j = Journal()

        j.code = rp.code
        j.datetimeCreated = rp.datetimeCreated
        j.createdBy = rp.createdBy
        j.journalDate = datetime.now()
        j.save()
        request.user.branch.journal.add(j)

        ################# CREDIT SIDE #################
        jeAPI(request, j, 'Credit', rp.salesContract.party.accountChild.get(name__regex=r"[Rr]eceivable"), (rp.amountPaid + rp.wep))

        ################# DEBIT SIDE #################
        if rp.wep!= 0.0:
            jeAPI(request, j, 'Debit', dChildAccount.ewp, rp.wep)

        if rp.paymentMethod == dChildAccount.cashOnHand.name:
            jeAPI(request, j, 'Debit', dChildAccount.cashOnHand, rp.amountPaid)
        elif re.search('[Cc]ash [Ii]n [Bb]ank', rp.paymentMethod):
            jeAPI(request, j, 'Debit', dChildAccount.cashInBank.get(name=rp.paymentMethod), rp.amountPaid)
        
        rp.salesContract.runningBalance -= rp.amountPaid
        if rp.salesContract.runningBalance == 0:
            rp.salesContract.fullyPaid == True
        rp.salesContract.save()
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)