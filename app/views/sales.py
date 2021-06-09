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

class SalesContractView(View):
    def get(self, request, format=None):

        user = request.user

        try:
            sc = user.branch.salesContract.latest('pk')

            listed_code = sc.code.split('-')
            listed_date = str(now.today()).split('-')

            current_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                current_code += 1
                new_code = 'SC-{}-{}-{}'.format(listed_date[0], listed_date[1], str(current_code).zfill(4))
            else:
                new_code = 'SC-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            print(e)
            listed_date = str(now.today()).split('-')
            new_code = 'SC-{}-{}-0001'.format(listed_date[0], listed_date[1])

        context = {
            'new_code': new_code,
        }
        return render(request, 'sales-contract.html', context)

class SCListView(View):
    def get(self, request, format=None):
        return render(request, 'sc-list.html')

class SaveSalesContract(APIView):
    def post(self, request, format = None):
        salesContract = request.data

        sc = TempSalesContract()

        sc.code = salesContract['code']
        sc.datetimeCreated = salesContract['dateTimeCreated']
        sc.dateSold = salesContract['date']

        sc.party = Party.objects.get(pk=salesContract['customer'])
        
        # for atc in salesContract['atc']:
        #     sc.atcCode = atc['code']
        #     sc.amountWithheld = atc['amountWithheld']
        
        sc.subTotal = salesContract['subTotal']
        if salesContract['discountType'] == 'percent':
            sc.discountPercent = salesContract['totalDiscount']
        elif salesContract['discountType'] == 'peso':
            sc.discountPeso = salesContract['totalDiscount']

        sc.taxPeso = salesContract['tax']
        sc.totalCost = salesContract['total']
        
        # sc.paymentMethod = salesContract['paymentMethod']
        # sc.paymentPeriod = salesContract['paymentPeriod']
        # sc.chequeNo = salesContract['chequeNo']
        # sc.dueDate = salesContract['dueDate']
        # sc.bank = salesContract['bank']
        # sc.remarks = salesContract['remarks']
        
        if request.user.is_authenticated:
            sc.createdBy = request.user

        sc.save()
        request.user.branch.salesContract.add(sc)

        for item in salesContract['items']:
            scitemsmerch = TempSCItemsMerch()
            scitemsmerch.salesContract = sc
            scitemsmerch.merchInventory = MerchandiseInventory.objects.get(pk=item['code'])
            scitemsmerch.remaining = item['remaining']
            scitemsmerch.qty = item['quantity']
            scitemsmerch.totalCost = Decimal(item['total'])

            print(scitemsmerch.totalCost)
            
            scitemsmerch.save()
            request.user.branch.scitemsMerch.add(scitemsmerch)

        for fee in salesContract['otherFees']:
            f = TempSCOtherFees()
            f.salesContract = sc
            f.fee = fee['fee']
            f.description = fee['description']
            f.save()
            request.user.branch.tempSCOtherFees.add(f)
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)