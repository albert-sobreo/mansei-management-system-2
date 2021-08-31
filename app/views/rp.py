from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
import sweetify
from datetime import date as now
from decimal import Decimal
from datetime import datetime
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
    def post(self, request, format = None):
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

        if rp.paymentMethod != "Cheque":
            j = Journal()

            j.code = rp.code
            j.datetimeCreated = rp.datetimeCreated
            j.createdBy = rp.createdBy
            j.journalDate = datetime.now()
            j.save()
            rp.journal = j
            rp.save()
            request.user.branch.journal.add(j)

            ################# CREDIT SIDE #################
            jeAPI(request, j, 'Credit', rp.salesContract.party.accountChild.get(name__regex=r"[Rr]eceivable"), (rp.amountPaid + rp.wep))

            ################# DEBIT SIDE #################
            if rp.wep!= 0.0:
                jeAPI(request, j, 'Debit', dChildAccount.cwit, rp.wep)

            if rp.paymentMethod == dChildAccount.cashOnHand.name:
                jeAPI(request, j, 'Debit', dChildAccount.cashOnHand, rp.amountPaid)
            elif re.search('[Cc]ash [Ii]n [Bb]ank', rp.paymentMethod):
                jeAPI(request, j, 'Debit', dChildAccount.cashInBank.get(name=rp.paymentMethod), rp.amountPaid)
            
            rp.salesContract.runningBalance -= (rp.amountPaid + rp.wep)
            if rp.salesContract.runningBalance == 0:
                rp.salesContract.fullyPaid = True
            rp.salesContract.save()
        else:
            cheque = Cheques()
            cheque.chequeNo = receivePayment['chequeNo']
            cheque.accountChild = AccountChild.objects.get(pk=receivePayment['bank'])
            print(receivePayment['bank'])
            cheque.dueDate = receivePayment['dueDate']
            cheque.save()
            request.user.branch.cheque.add(cheque)

            rp.cheque = cheque
            rp.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class RPVoid(APIView):
    def put(self, request, pk, format = None):
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount
        
        rp = ReceivedPayment.objects.get(pk=pk)
        rp.voided = True
        rp.datetimeVoided = datetime.now()
        rp.voidedBy = request.user

        
        j = Journal()
        j.code = rp.code
        j.datetimeCreated = rp.datetimeCreated
        j.createdBy = rp.createdBy
        j.journalDate = datetime.now()
        j.save()
        rp.journal = j
        rp.save()
        request.user.branch.journal.add(j)
        ################# DEBIT SIDE #################
        jeAPI(request, j, 'Debit', rp.salesContract.party.accountChild.get(name__regex=r"[Rr]eceivable"), (rp.amountPaid + rp.wep))
        ################# CREDIT SIDE #################
        if rp.wep!= 0.0:
            jeAPI(request, j, 'Credit', dChildAccount.cwit, rp.wep)
        if rp.paymentMethod == dChildAccount.cashOnHand.name:
            jeAPI(request, j, 'Credit', dChildAccount.cashOnHand, rp.amountPaid)
        elif re.search('[Cc]ash [Ii]n [Bb]ank', rp.paymentMethod):
            jeAPI(request, j, 'Credit', dChildAccount.cashInBank.get(name=rp.paymentMethod), rp.amountPaid)
        elif rp.paymentMethod == "Cheque":
            jeAPI(request, j, 'Credit', rp.cheque.accountChild, rp.amountPaid)
        
        rp.salesContract.runningBalance += (rp.amountPaid + rp.wep)
        if rp.salesContract.runningBalance == 0:
            rp.salesContract.fullyPaid = True
        rp.salesContract.save()

        if rp.paymentMethod == "Cheque":
            rp.cheque.receivePayment = None
            rp.cheque.receivePayment.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)
        
