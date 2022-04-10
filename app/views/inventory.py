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
from .journalAPI import jeAPI, JournalAPI, getNewJournalCode

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

        j = JournalAPI(request, getNewJournalCode(request), request.user, datetime.now(), 'Inventory Initialization')
        journalCounter = Decimal(0)

        equity = request.user.branch.accountGroup.get(name='Equity')
        if request.user.branch.subGroup.filter(name="Temporary Capital").exists():
            subtempCap = request.user.branch.subGroup.get(name="Temporary Capital")
        else:
            subtempCap = AccountSubGroup()
            subtempCap.code = "##"
            subtempCap.name = 'Temporary Capital'
            subtempCap.accountGroup = equity
            subtempCap.description = ''
            subtempCap.amount = Decimal(0)
            subtempCap.save()
            request.user.branch.subGroup.add(subtempCap)

        if request.user.branch.accountChild.filter(name="Temporary Capital").exists():
             tempCap = request.user.branch.accountChild.get(name="Temporary Capital")
        else:
            tempCap = AccountChild()
            tempCap.code = "##"
            tempCap.name = 'Temporary Capital'
            tempCap.accountSubGroup = subtempCap
            tempCap.description = ''
            tempCap.amount = Decimal(0)
            tempCap.save()
            request.user.branch.accountChild.add(tempCap)

        # INIT TEMPORARY DEBIT SIDE
        debit = {}
        
        for item in jsonDF:
            merch = MerchandiseInventory()
            print(item)
            if request.user.branch.merchInventory.filter(code=item['Code']):
                
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
            try:
                debit[merch.childAccountInventory] += merch.totalCost
            except:
                debit[merch.childAccountInventory] = merch.totalCost
            journalCounter += Decimal(merch.totalCost)
            
            wi = WarehouseItems()
            wi.merchInventory = merch
            try:
                wi.warehouse = request.user.branch.warehouse.get(name=item['Warehouse'])
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

        for key, val in debit.items():
            j.addJE('Debit', key, val)

        j.addJE('Credit', tempCap, journalCounter)
        j.save()

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
        merch.sellingPrice = edit['sellingPrice']

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

class ManuInventoryView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()

        return render(request, 'manuInventory.html')

class SaveEditManuInventoryAPI(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()

        data = request.data

        manu = ManufacturingInventory.objects.get(pk=data['id'])
        manu.code = data['code']
        manu.name = data['name']
        manu.sellingPrice = data['sellingPrice']
        manu.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)