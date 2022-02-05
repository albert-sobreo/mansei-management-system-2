from rest_framework.views import APIView
from ..models import *
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from decimal import Decimal
import pandas as pd
import json
from datetime import datetime
from django.core.exceptions import PermissionDenied
from .notificationCreate import *

class MerchInventoryView(View):
    def get(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        return render(request, 'merchinventory.html')

class AddMerchInventoryAPI(APIView):
    def post(self, request, format = None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        print(request.data)
        
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount
        a = MerchandiseInventory()

        a.code = request.data['code']
        a.name = (request.data['name']).upper()
        a.classification = (request.data['classification']).upper()
        a.type = request.data['type']
        a.length = Decimal(request.data['length'])
        a.width = Decimal(request.data['width'])
        a.thickness = Decimal(request.data['thickness'])
        a.purchasingPrice = request.data['purchasingPrice']
        a.sellingPrice = request.data['sellingPrice']
        a.pricePerCubic = request.data['pricePerCubic']
        a.inventoryDate = request.data['inventoryDate']
        a.qtyT = 0
        a.qtyR = 0
        a.qtyA = 0
        a.um = "Per Piece"
        a.vol = (a.width / 1000) * (a.length / 1000) * (a.thickness / 1000)
        a.totalCost = 0.0
        # PUT CHART OF ACCOUNT CODE HERE
        # ACCOUNT INVENTORY

        a.invAccounts(request, a.name, a.classification)
        # END
        a.save()
        
        w = Warehouse.objects.get(pk=request.data['warehouse'])

        wi = WarehouseItems()

        wi.merchInventory = a
        wi.warehouse = w
        wi.initQty(a.qtyT, a.qtyR, a.qtyA)
        wi.save()

        request.user.branch.warehouseItems.add(wi)
        request.user.branch.merchInventory.add(a)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class ImportMerchandiseInventory(View):
    def post(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
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

            item['Unit-Cost'] = str(item['Unit-Cost']).replace('₱', '')
            item['Unit-Cost'] = item['Unit-Cost'].replace(',', '')
            merch.purchasingPrice = item['Unit-Cost']

            item['Selling-Price'] = str(item['Selling-Price']).replace('₱', '')
            item['Selling-Price'] = item['Selling-Price'].replace(',', '')
            merch.sellingPrice = item['Selling-Price']

            merch.vol = (merch.width / 1000) * (merch.length / 1000) * (merch.thickness / 1000)

            item['Price-Per-Cubic'] = str(item['Price-Per-Cubic']).replace('₱', '')
            item['Price-Per-Cubic'] = item['Price-Per-Cubic'].replace(',', '')
            merch.pricePerCubic = item['Price-Per-Cubic']
            merch.qtyT = int(item['QtyT'])
            merch.qtyR = int(item['QtyR'])
            merch.qtyA = merch.qtyT - merch.qtyR
            merch.um = item['U/M']
            merch.description = item['Description']
            merch.totalCost = item['Total-Cost']
            merch.inventoryDate = datetime.fromtimestamp((item['Inventory-Date'])/1000)

            merch.invAccounts(request, merch.name, merch.classification)

            merch.save()
            
            wi = WarehouseItems()
            wi.merchInventory = merch
            try:
                wi.warehouse = Warehouse.objects.get(name=item['Warehouse'])

            except:
                w = Warehouse()
                w.name = item['Warehouse']
                w.address = '---'
                w.save()
                request.user.branch.warehouse.add(w)
                wi.warehouse = w

            wi.initQty(merch.qtyT, merch.qtyR, merch.qtyA)
            wi.save()
            request.user.branch.warehouseItems.add(wi)
            request.user.branch.merchInventory.add(merch)

        sweetify.sweetalert(request, icon="success", title="Success!", persistent="Dismiss")
        return redirect('/merchinventory/')



class EditInventory(APIView):
    def put(self, request, pk, format = None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        
        merch = MerchandiseInventory.objects.get(pk=pk)

        edit = request.data

        merch.code = edit['code']
        merch.name = edit['name']
        merch.classification = edit['classification']
        merch.type = edit['type']
        merch.pricePerCubic = edit['pricePerCubic']
        merch.um = edit['um']
        merch.inventoryDate = edit['inventoryDate']

        merch.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)


class OtherInventoryView(View):
    def get(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        return render(request, 'otherinventory.html')


class DeleteMerchInventory(APIView):
    def delete(self, request, pk):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        inv = MerchandiseInventory.objects.get(pk=pk)
        for item in inv.warehouseitems.all():
            item.delete()
        inv.delete()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)