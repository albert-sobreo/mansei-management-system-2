from django import views
from django.core.exceptions import NON_FIELD_ERRORS
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
        }
        return render(request, 'purchase-order.html', context)

class POListView(View):
    def get(self, request, format=None):
        return render(request, 'po-list.html')

class SavePurchaseOrder(APIView):
    def post(self, request, format = None):
        purchaseOrder = request.data

        po = PurchaseOrder()

        po.code = purchaseOrder['code']
        po.datetimeCreated = purchaseOrder['dateTimeCreated']

        if purchaseOrder['retroactive']:
            po.datePurchased = purchaseOrder['retroactive']
        else:
            po.datePurchased = purchaseOrder['date']

        po.party = Party.objects.get(pk=purchaseOrder['vendor'])
        
        for atc in purchaseOrder['atc']:
            po.atcCode = atc['code']
            po.amountWithheld = atc['amountWithheld']
        
        po.amountPaid = Decimal(purchaseOrder['amountPaid'])
        po.amountDue = Decimal(purchaseOrder['amountDue'])
        
        po.paymentMethod = purchaseOrder['paymentMethod']
        po.paymentPeriod = purchaseOrder['paymentPeriod']
        po.chequeNo = purchaseOrder['chequeNo']
        po.dueDate = purchaseOrder['dueDate']
        po.bank = purchaseOrder['bank']
        po.remarks = purchaseOrder['remarks']
        
        if request.user.is_authenticated:
            po.createdBy = request.user

        po.save()
        request.user.branch.purchaseOrder.add(po)

        for item in purchaseOrder['items']:
            poitemsmerch = POItemsMerch()
            poitemsmerch.purchaseOrder = po
            poitemsmerch.merchInventory = MerchandiseInventory.objects.get(pk=item['code'])
            poitemsmerch.remaining = item['remaining']
            poitemsmerch.qty = item['quantity']
            poitemsmerch.purchasingPrice = Decimal(item['vatable'])
            poitemsmerch.totalPrice = Decimal(item['totalCost'])
            poitemsmerch.inputVat = Decimal(item['inputVAT'])

            print(poitemsmerch.purchasingPrice, poitemsmerch.totalPrice, poitemsmerch.inputVat)
            
            poitemsmerch.save()
            request.user.branch.poitemsMerch.add(poitemsmerch)
        return JsonResponse(0, safe=False)