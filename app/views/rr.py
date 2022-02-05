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
from .notificationCreate import *

class ReceivingReportView(View):
    def get(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()

        user = request.user

        try:
            rr = user.branch.receivingReport.latest('pk')

            listed_code = rr.code.split('-')
            listed_date = str(now.today()).split('-')

            cuprent_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                cuprent_code += 1
                new_code = 'RR-{}-{}-{}'.format(listed_date[0], listed_date[1], str(cuprent_code).zfill(4))
            else:
                new_code = 'RR-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            listed_date = str(now.today()).split('-')
            new_code = 'RR-{}-{}-0001'.format(listed_date[0], listed_date[1])

        context = {
            'new_code': new_code,
            'pos': request.user.branch.purchaseOrder.filter(approved=True, fullyReceived=False)
        }
        return render(request, 'receiving-report.html', context)

class RRListView(View):
    def get(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        return render(request, 'rr-list.html')

class SaveReceivingReport(APIView):
    def post(self, request, format = None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        receivingReport = request.data

        rr = ReceivingReport()

        for key, value in receivingReport.items() :
            print (key, value)

        rr.code = receivingReport['code']
        rr.datetimeCreated = datetime.now()

        if receivingReport['retroactive']:
            rr.dateReceived = receivingReport['retroactive']
        else:
            rr.dateReceived = receivingReport['datePurchased']

        rr.party = Party.objects.get(pk=receivingReport['vendor'])

        atc = RRatc()
        
        rr.amountDue = Decimal(receivingReport['amountDue'])
        rr.amountTotal = Decimal(receivingReport['amountTotal'])
        rr.taxType = receivingReport['taxType']
        rr.taxRate = Decimal(receivingReport['taxRate'])
        rr.taxPeso = Decimal(receivingReport['taxPeso'])
        rr.chequeNo = receivingReport['chequeNo']
        rr.dueDate = receivingReport['dueDate']
        rr.bank = receivingReport['bank']
        rr.remarks = receivingReport['remarks']
        rr.purchaseOrder = PurchaseOrder.objects.get(pk=receivingReport['po'])
        rr.wep = Decimal(receivingReport['withholdingTax'])
        rr.purchaseOrder.save()
        
        if request.user.is_authenticated:
            rr.createdBy = request.user

        rr.save()
        request.user.branch.receivingReport.add(rr)

        for jsonatc in receivingReport['atc']:
            print(jsonatc)
            atc.code = ATC.objects.get(pk=jsonatc['code'])
            atc.amountWithheld = jsonatc['amountWithheld']
            atc.receivingReport = rr
            atc.save()
            request.user.branch.rratc.add(atc)

        for item in receivingReport['items']:
            if item['type'] == 'Merchandise':
                rritemsmerch = RRItemsMerch()
                rritemsmerch.receivingReport = rr
                rritemsmerch.poitemsmerch = POItemsMerch.objects.get(pk=item['poID'])
                rritemsmerch.merchInventory = MerchandiseInventory.objects.get(pk=item['code'])
                rritemsmerch.remaining = item['remaining']
                rritemsmerch.qty = item['quantity']
                rritemsmerch.purchasingPrice = Decimal(item['vatable'])
                rritemsmerch.totalPrice = Decimal(item['totalCost'])

                rritemsmerch.save()
                request.user.branch.rritemsMerch.add(rritemsmerch)

            else: 
                rritemsother = RRItemsOther()
                rritemsother.receivingReport = rr
                rritemsother.type = item['type']
                rritemsother.poitemsother = POItemsOther.objects.get(pk=item['poID'])
                try:
                    rritemsother.otherInventory = OtherInventory.objects.get(name=item['other'])
                except:
                    otherInv = OtherInventory()
                    otherInv.name = item['other']
                    otherInv.qty = 0
                    otherInv.purchasingPrice = Decimal(0.0)
                    otherInv.accountChild = AccountChild.objects.get(pk=item['type'])
                    otherInv.save()
                    request.user.branch.otherInventory.add(otherInv)
                    rritemsother.otherInventory = otherInv

                rritemsother.remaining = item['remaining']
                rritemsother.qty = item['quantity']
                rritemsother.purchasingPrice = Decimal(item['vatable'])
                rritemsother.totalPrice = Decimal(item['totalCost'])

                rritemsother.save()
                request.user.branch.rrItemsOther.add(rritemsother)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)