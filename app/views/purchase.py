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

class PurchaseOrderView(View):
    def get(self, request, format=None):

        user = request.user

        try:
            po = user.branch.purchaseOrder.latest('pk')

            listed_code = po.code.split('-')
            listed_date = str(now.today()).split('-')

            current_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                current_code += 1
                new_code = 'PO-{}-{}-{}'.format(listed_date[0], listed_date[1], str(current_code).zfill(4))
            else:
                new_code = 'PO-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            print(e)
            listed_date = str(now.today()).split('-')
            new_code = 'PO-{}-{}-0001'.format(listed_date[0], listed_date[1])

        context = {
            'new_code': new_code,
            'prs': request.user.branch.purchaseRequest.filter(approved=True, poed=False)
        }
        return render(request, 'purchase-order.html', context)

class POListView(View):
    def get(self, request, format=None):
        return render(request, 'po-list.html')

class SavePurchaseOrder(APIView):
    def post(self, request, format = None):
        purchaseOrder = request.data

        po = PurchaseOrder()

        for key, value in purchaseOrder.items() :
            print (key, value)

        po.code = purchaseOrder['code']
        po.datetimeCreated = datetime.now()

        if purchaseOrder['retroactive']:
            po.datePurchased = purchaseOrder['retroactive']
        else:
            po.datePurchased = purchaseOrder['date']

        po.party = Party.objects.get(pk=purchaseOrder['vendor'])

        atc = POatc()

        po.amountDue = Decimal(purchaseOrder['amountDue'])
        po.amountTotal = Decimal(purchaseOrder['amountTotal'])
        po.runningBalance = Decimal(purchaseOrder['amountTotal'])
        po.taxType = purchaseOrder['taxType']
        po.taxRate = Decimal(purchaseOrder['taxRate'])
        po.taxPeso = Decimal(purchaseOrder['taxPeso'])
        po.chequeNo = purchaseOrder['chequeNo']
        po.dueDate = purchaseOrder['dueDate']
        po.bank = purchaseOrder['bank']
        po.remarks = purchaseOrder['remarks']
        po.wep = Decimal(purchaseOrder['withholdingTax'])

        po.needsRR = not purchaseOrder['notNeedRR']

        try:
            po.purchaseRequest = PurchaseRequest.objects.get(pk=purchaseOrder['pr'])
            po.purchaseRequest.poed = True
            po.purchaseRequest.save()
        except:
            pass
        
        
        if request.user.is_authenticated:
            po.createdBy = request.user

        po.save()
        request.user.branch.purchaseOrder.add(po)

        for jsonatc in purchaseOrder['atc']:
            print(jsonatc)
            atc.code = ATC.objects.get(pk=jsonatc['code'])
            atc.amountWithheld = jsonatc['amountWithheld']
            atc.purchaseOrder = po
            atc.save()
            request.user.branch.poatc.add(atc)

        for item in purchaseOrder['items']:
            if item['type'] == 'Merchandise':
                poitemsmerch = POItemsMerch()
                poitemsmerch.purchaseOrder = po
                poitemsmerch.merchInventory = MerchandiseInventory.objects.get(pk=item['code'])
                poitemsmerch.remaining = item['remaining']
                poitemsmerch.qty = item['quantity']
                poitemsmerch.purchasingPrice = Decimal(item['vatable'])
                poitemsmerch.totalPrice = Decimal(item['totalCost'])
                poitemsmerch.unit = item['unitCtr']

                poitemsmerch.save()
                request.user.branch.poitemsMerch.add(poitemsmerch)
            else:
                poitemsother = POItemsOther()
                poitemsother.purchaseOrder = po
                poitemsother.type = item['type']

                try: 
                    poitemsother.otherInventory = OtherInventory.objects.get(name=item['other'])
                except:
                    otherInv = OtherInventory()
                    otherInv.name = item['other']
                    otherInv.qty = 0
                    otherInv.purchasingPrice = Decimal(0.0)
                    otherInv.accountChild = AccountChild.objects.get(pk=item['type'])
                    otherInv.save()
                    request.user.branch.otherInventory.add(otherInv)
                    poitemsother.otherInventory = otherInv
                
                poitemsother.remaining = item['remaining']
                poitemsother.qty = item['quantity']
                poitemsother.purchasingPrice = Decimal(item['vatable'])
                poitemsother.totalPrice = Decimal(item['totalCost'])
                poitemsother.unit = item['unitCtr']

                poitemsother.save()
                request.user.branch.poItemsOther.add(poitemsother)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)