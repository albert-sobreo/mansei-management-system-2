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
from datetime import datetime
from decimal import Decimal
import pandas as pd
import json

class InwardView(View):
    def get(self, request, format=None):
        return render(request, 'inward-inventory.html')

class InwardAdjustmentsView(View):
    def get(self, request, format=None):
        context = {
            'ii': request.user.branch.inwardInventory.filter()
        }
        return render(request, 'inward-adjustment.html', context)

class ImportInwardInventory(View):
    def post(self, request, format= None):

        try:
            ii = request.user.branch.inwardInventory.latest('pk')

            listed_code = ii.code.split('-')
            listed_date = str(now.today()).split('-')

            current_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                current_code += 1
                new_code = 'II-{}-{}-{}'.format(listed_date[0], listed_date[1], str(current_code).zfill(4))
            else:
                new_code = 'II-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            print(e)
            listed_date = str(now.today()).split('-')
            new_code = 'II-{}-{}-0001'.format(listed_date[0], listed_date[1])

        df = pd.read_excel(request.FILES['excel'])
        jsonDF = json.loads(df.to_json(orient='records'))

        ii = InwardInventory()

        ii.code = new_code
        ii.datetimeCreated = datetime.now()
        ii.dateInward = datetime.now()
        ii.party = Party.objects.get(name='Juken Sangyo')
        
        total = 0
        if request.user.is_authenticated:
            ii.createdBy = request.user
        
        ii.save()

        for item in jsonDF:
            iiitemsMerch = IIItemsMerch()

            iiitemsMerch.inwardInventory = ii

            iiitemsMerch.code = item['barcode']
            iiitemsMerch.productMark = item['productMark']
            iiitemsMerch.length = item['length']
            iiitemsMerch.width = item['width']
            iiitemsMerch.thicc = item['thicc']
            iiitemsMerch.vol = item['vol']
            iiitemsMerch.qty = item['qty']

            item['amount'] = str(item['amount']).replace('₱', '')
            item['amount'] = item['amount'].replace(',', '')
            iiitemsMerch.amount = item['amount']

            item['totalCost'] = str(item['totalCost']).replace('₱', '')
            item['totalCost'] = item['totalCost'].replace(',', '')
            iiitemsMerch.totalCost = item['totalCost']
            total += Decimal(iiitemsMerch.totalCost)

            iiitemsMerch.save()
            request.user.branch.iiItemsMerch.add(iiitemsMerch)

        ii.amountTotal = total
        ii.save()
        request.user.branch.inwardInventory.add(ii)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return redirect('/inward-inventory/')

class InwardAdjustmentSave(APIView):
    def post(self, request, pk, format=None):
        inward = request.data
        
        for item in inward['items']:
            for item1 in item['adjusted']:
                print(item1)
                adjusted = IIAdjustedItems()
                adjusted.inwardInventory = InwardInventory.objects.get(pk=pk)
                adjusted.iiItemsMerch = IIItemsMerch.objects.get(pk=item['id'])
                adjusted.code = item1['code']
                adjusted.name = item1['name']
                adjusted.classfication = item1['classification']
                adjusted.type = item1['type']
                adjusted.length = item1['length']
                adjusted.width = item1['width']
                adjusted.thicc = item1['thickness']
                adjusted.vol = item1['vol']
                adjusted.qty = item1['qty']
                adjusted.amount = item1['amount']
                adjusted.totalCost = item1['amountTotal']
                adjusted.pricePerCubic = item1['pricePerCubic']
                adjusted.save()
                request.user.branch.iiAdjustedItems.add(adjusted)
        
        inwardInventory = InwardInventory.objects.get(pk=pk)
        inwardInventory.adjusted = True
        inwardInventory.amountTotal = inward['amountTotal']
        inwardInventory.runningBalance = inward['amountTotal']
        inwardInventory.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)
