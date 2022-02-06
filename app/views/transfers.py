from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
import sweetify
from datetime import date as now
from datetime import datetime
from django.core.exceptions import PermissionDenied
from .notificationCreate import *

class TransferView(View):
    def get(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()

        user = request.user

        try:
            tr = user.branch.transfer.latest('pk')

            listed_code = tr.code.split('-')
            listed_date = str(now.today()).split('-')

            current_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                current_code += 1
                new_code = 'TR-{}-{}-{}'.format(listed_date[0], listed_date[1], str(current_code).zfill(4))
            else:
                new_code = 'TR-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            print(e)
            listed_date = str(now.today()).split('-')
            new_code = 'TR-{}-{}-0001'.format(listed_date[0], listed_date[1])

        context = {
            'new_code': new_code,
        }
        return render(request, 'inventory-transfer.html', context)

class TransferList(View):
    def get(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        return render(request, 'transfer-list.html')

class SaveTransfer(APIView):
    def post(self, request, format = None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        transfer = request.data

        tr = Transfer()

        tr.code = transfer['code']
        tr.datetimeCreated = datetime.now()
        tr.remarks = transfer['remarks']
        tr.newWarehouse = Warehouse.objects.get(pk=transfer['newWarehouse'])
        tr.totalCost = transfer['totalCost']

        if request.user.is_authenticated:
            tr.createdBy = request.user

        tr.save()
        request.user.branch.transfer.add(tr)

        for item in transfer['items']:
            tritem = TransferItems()
            tritem.transfer = tr
            tritem.merchInventory = MerchandiseInventory.objects.get(pk=item['code'])
            tritem.qtyTransfered = item['qty']
            tritem.oldWarehouse = Warehouse.objects.get(pk=item['oldWarehouse'])
            
            tritem.save()
            request.user.branch.transferItems.add(tritem)

        notify(request, 'New Transfer Request', tr.code, '/tr-nonapproved/', 1)
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

