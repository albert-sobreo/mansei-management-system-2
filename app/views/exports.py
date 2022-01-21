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
from django.core.exceptions import PermissionDenied
from .journalAPI import jeAPI
import re

########## EXPORTS ##########
class ExportsView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()

        user = request.user

        try:
            exports = user.branch.exports.latest('pk')

            listed_code = exports.code.split('-')
            listed_date = str(now.today()).split('-')

            current_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                current_code += 1
                new_code = 'EXP-{}-{}-{}'.format(listed_date[0], listed_date[1], str(current_code).zfill(4))
            else:
                new_code = 'EXP-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            print(e)
            listed_date = str(now.today()).split('-')
            new_code = 'EXP-{}-{}-0001'.format(listed_date[0], listed_date[1])

        context = {
            'new_code': new_code,
        }
        return render(request, 'exports.html', context)

class ExportsListView(View):
    def get(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        return render(request, 'exports-list.html')

class SaveExports(APIView):
    def post(self, request, format = None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        export = request.data

        exp = Exports()

        exp.code = export['code']
        exp.datetimeCreated = datetime.now()

        if export['retroactive']:
            exp.dateSold = export['retroactive']
        else:
            exp.dateSold = export['date']

        exp.party = Party.objects.get(pk=export['customer'])
        
        exp.amountDue = Decimal(export['amountDue'])
        exp.amountTotal = Decimal(export['amountTotal'])
        exp.runningBalance = exp.amountTotal
        exp.chequeNo = export['chequeNo']
        exp.dueDate = export['dueDate']
        exp.bank = export['bank']
        exp.remarks = export['remarks']
        exp.forex = export['exchangeRate']

        if request.user.is_authenticated:
            exp.createdBy = request.user

        if export['discountType'] == 'percent':
            exp.discountPercent = export['totalDiscount']
        elif export['discountType'] == 'peso':
            exp.discountPeso = export['totalDiscount']

        exp.save()
        request.user.branch.exports.add(exp)

        

        for item in export['items']:
            exportitemsmerch = ExportItemsMerch()
            exportitemsmerch.export = exp
            exportitemsmerch.merchInventory = MerchandiseInventory.objects.get(pk=item['code'])
            exportitemsmerch.remaining = item['remaining']
            exportitemsmerch.qty = item['quantity']
            exportitemsmerch.pallet = item['pallet']
            exportitemsmerch.cbm = item['cbm']
            exportitemsmerch.vol = item['vol']
            exportitemsmerch.pricePerCubic = Decimal(item['pricePerCubic'])
            exportitemsmerch.totalCost = Decimal(item['totalCost'])

            print(item['pricePerCubic'], item['totalCost'])
            
            exportitemsmerch.save()
            request.user.branch.exportItemsMerch.add(exportitemsmerch)

        for fee in export['otherFees']:
            f = ExportOtherFees()
            f.export = exp
            f.fee = fee['fee']
            f.description = fee['description']
            f.save()
            request.user.branch.exportOtherFees.add(f)
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)


class ReceivedPaymentsUSDView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        
        try:
            rp = request.user.branch.receivePayment.latest('pk')

            listed_code = rp.code.split('-')
            listed_date = str(now.today()).split('-')

            current_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                current_code += 1
                new_code = 'RP/USD-{}-{}-{}'.format(listed_date[0], listed_date[1], str(current_code).zfill(4))
            else:
                new_code = 'RP/USD-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            print(e)
            listed_date = str(now.today()).split('-')
            new_code = 'RP/USD-{}-{}-0001'.format(listed_date[0], listed_date[1])

        context = {
            'new_code': new_code,
            'exports': request.user.branch.exports.filter(approved=True, fullyPaid=False).exclude(runningBalance=Decimal(0)),
            'customers': request.user.branch.party.filter(type="Customer")
        }
        return render(request, 'received-payments-usd.html', context)

class SaveReceivePaymentsUSD(APIView):
    def post(self, request, format = None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount
        receivePaymentUSD = request.data


        ##### RECEIVED PAYMENT DEFAULT #####
        if receivePaymentUSD['rpType'] == 'Default':

            rp = ReceivePaymentUSD()
            rp.code = receivePaymentUSD['code']
            rp.datetimeCreated = datetime.now()
            rp.remarks = receivePaymentUSD['description']
            if receivePaymentUSD['retroactive']:
                rp.paymentDate = receivePaymentUSD['retroactive']
            else:
                rp.paymentDate = receivePaymentUSD['date']
            if request.user.is_authenticated:
                rp.createdBy = request.user
            rp.exports = Exports.objects.get(pk=receivePaymentUSD['sc']['code'])
            rp.paymentMethod = receivePaymentUSD['paymentMethod']
            rp.paymentPeriod = receivePaymentUSD['paymentPeriod']
            rp.forex = Decimal(receivePaymentUSD['exchangeRate'])

            rp.amountPaid = Decimal(receivePaymentUSD['amountPaid'])
            rp.save()
            request.user.branch.receivepaymentsUSD.add(rp)

            if rp.paymentMethod == "Cheque":
                cheque = Cheques()
                cheque.chequeNo = receivePaymentUSD['chequeNo']
                cheque.accountChild = AccountChild.objects.get(pk=receivePaymentUSD['bank'])
                print(receivePaymentUSD['bank'])
                cheque.dueDate = receivePaymentUSD['dueDate']
                cheque.save()
                request.user.branch.cheque.add(cheque)

                rp.cheque = cheque
                rp.save()

                sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
                return JsonResponse(0, safe=False)
                
            rp.exports.runningBalance -= (rp.amountPaid)
            if rp.exports.runningBalance == 0:
                rp.exports.fullyPaid = True
            rp.exports.save()

        #     j = Journal()
        #     j.code = rp.code
        #     j.datetimeCreated = rp.datetimeCreated
        #     j.createdBy = rp.createdBy
        #     j.journalDate = datetime.now()
        #     j.save()
        #     rp.journal = j
        #     rp.save()
        #     request.user.branch.journal.add(j)
        #     ################# CREDIT SIDE #################
        #     # jeAPI(request, j, 'Credit', rp.salesContract.party.accountChild.get(name__regex=r"[Rr]eceivable"), (rp.amountPaid + rp.wep))
        #     ################# DEBIT SIDE #################
        #     if rp.paymentMethod == dChildAccount.cashOnHand.name:
        #         jeAPI(request, j, 'Credit', rp.exports.party.accountChild.get(name__regex=r"[Rr]eceivable"), (rp.amountPaid))
        #         jeAPI(request, j, 'Debit', dChildAccount.cashOnHand, rp.amountPaid)
        #     elif re.search('[Cc]ash [Ii]n [Bb]ank', rp.paymentMethod):
        #         jeAPI(request, j, 'Credit', rp.salesContract.party.accountChild.get(name__regex=r"[Rr]eceivable"), (rp.amountPaid))
        #         jeAPI(request, j, 'Debit', dChildAccount.cashInBank.get(name=rp.paymentMethod), rp.amountPaid)
            
        #     rp.exports.runningBalance -= (rp.amountPaid)
        #     if rp.exports.runningBalance == 0:
        #         rp.exports.fullyPaid = True
        #     rp.exports.save()

        # ##### END OF RECEIVED PAYMENT DEFAULT #####
        # elif receivePaymentUSD['rpType'] == 'Custom':
        #     rp = receivePaymentUSD()
        #     rp.code = receivePaymentUSD['code']
        #     rp.datetimeCreated = datetime.now()
        #     rp.remarks = receivePaymentUSD['remarks']
        #     if receivePaymentUSD['retroactive']:
        #         rp.paymentDate = receivePaymentUSD['retroactive']
        #     else:
        #         rp.paymentDate = receivePaymentUSD['date']

        #     if request.user.is_authenticated:
        #         rp.createdBy = request.user

        #     rp.party = Party.objects.get(pk=receivePaymentUSD['party'])

        #     rp.save()

        #     for item in receivePaymentUSD['debit']:
        #         crpe = CustomRPEntries()
        #         crpe.receivePaymentUSD = rp
        #         crpe.normally = item['normally']
        #         crpe.accountChild = AccountChild.objects.get(pk=item['accountChild'])
        #         crpe.amount = item['amount']
        #         crpe.save()
                
        #         request.user.branch.customRPEntries.add(crpe)

        #     for item in receivePaymentUSD['credit']:
        #         crpe = CustomRPEntries()
        #         crpe.receivePaymentUSD = rp
        #         crpe.normally = item['normally']
        #         crpe.accountChild = AccountChild.objects.get(pk=item['accountChild'])
        #         crpe.amount = item['amount']
        #         crpe.save()
                
        #         request.user.branch.customRPEntries.add(crpe)

        #     ##### CUSTOME RP NEEDS JOURNAL ENTRIES #####


        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)