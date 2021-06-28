from rest_framework.views import APIView
from ..models import MerchandiseInventory, Warehouse
from django import views
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models import query
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
import sweetify
from decimal import Decimal
import pandas as pd
import json

class MerchInventoryView(View):
    def get(self, request, format=None):
        return render(request, 'merchinventory.html')

class AddMerchInventoryAPI(APIView):
    def post(self, request, format = None):
        print(request.data)
        
        a = MerchandiseInventory()

        a.code = request.data['code']
        a.classification = request.data['classification']
        a.type = request.data['type']
        a.length = Decimal(request.data['length'])
        a.width = Decimal(request.data['width'])
        a.thickness = Decimal(request.data['thickness'])
        a.purchasingPrice = request.data['purchasingPrice']
        a.sellingPrice = request.data['sellingPrice']
        a.pricePerCubic = request.data['pricePerCubic']
        a.qtyT = 0
        a.qtyR = 0
        a.qtyA = 0
        a.um = "Per Piece"
        a.vol = (a.width / 1000) * (a.length / 1000) * (a.thickness / 1000)
        a.totalCost = 0.0
        a.save()
        for warehouse in request.data['warehouse']:
            a.warehouse.add(warehouse)

        request.user.branch.merchInventory.add(a)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class ImportMerchandiseInventory(View):
    def post(self, request, format=None):
        df = pd.read_excel(request.FILES['excel'])
        jsonDF = json.loads(df.to_json(orient='records'))
        
        for item in jsonDF:
            merch = MerchandiseInventory()

            if MerchandiseInventory.objects.filter(code=item['Code']):
                print('it exists')
                continue
            merch.code = item['Code']
            merch.name = item['Name']
            merch.classification = item['Classification']
            merch.type = item['Type']
            merch.length = item['Length']
            merch.width = item['Width']
            merch.thickness = item['Thickness']

            item['Purchasing-Price'] = str(item['Purchasing-Price']).replace('₱', '')
            item['Purchasing-Price'] = item['Purchasing-Price'].replace(',', '')
            merch.purchasingPrice = item['Purchasing-Price']

            item['Selling-Price'] = str(item['Selling-Price']).replace('₱', '')
            item['Selling-Price'] = item['Selling-Price'].replace(',', '')
            merch.sellingPrice = item['Selling-Price']
            merch.vol = item['Volume']

            item['Price-Per-Cubic'] = str(item['Price-Per-Cubic']).replace('₱', '')
            item['Price-Per-Cubic'] = item['Price-Per-Cubic'].replace(',', '')
            merch.pricePerCubic = item['Price-Per-Cubic']
            merch.qtyT = item['QtyT']
            merch.qtyR = item['QtyR']
            merch.qtyA = item['QtyA']
            merch.um = item['U/M']
            merch.description = item['Description']
            merch.totalCost = item['Total-Cost']

            print(merch.code, merch.name, merch.classification, merch.type, merch.length, merch.width, merch.thickness, merch.purchasingPrice, merch.sellingPrice, merch.vol, merch.pricePerCubic, merch.qtyA, merch.qtyR, merch.qtyT, merch.um, merch.description, merch.totalCost)

            merch.save()
            try:
                merch.warehouse.add(Warehouse.objects.get(name=item['Warehouse']))
            except:
                w = Warehouse()
                w.name = item['Warehouse']
                w.address = '---'
                w.save()
                request.user.branch.warehouse.add(w)
                merch.warehouse.add(w)
            request.user.branch.merchInventory.add(merch)
        
        return redirect('/merchinventory/')