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

class AdjustmentsView(View):
    def get(self, request, format=None):

        user = request.user

        if user.authLevel == '2':
            raise PermissionDenied()
        try:
            ad = user.branch.adjustments.latest('pk')

            listed_code = ad.code.split('-')
            listed_date = str(now.today()).split('-')

            current_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                current_code += 1
                new_code = 'AD-{}-{}-{}'.format(listed_date[0], listed_date[1], str(current_code).zfill(4))
            else:
                new_code = 'AD-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            print(e)
            listed_date = str(now.today()).split('-')
            new_code = 'AD-{}-{}-0001'.format(listed_date[0], listed_date[1])

        context = {
            'new_code': new_code,
        }
        return render(request, 'inventory-adjustments.html', context)

class AdjustmentList(View):
    def get(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        return render(request, 'ad-list.html')

class SaveAdjustments(APIView):
    def post(self, request, format = None):
        adjust = request.data

        ad = Adjustments()

        ad.code = adjust['code']
        ad.datetimeCreated = datetime.now()
        ad.totalLost = adjust['totalLost']
        ad.type = adjust['type']

        if request.user.is_authenticated:
            ad.createdBy = request.user

        ad.save()
        request.user.branch.adjustments.add(ad)

        for item in adjust['items']:
            aditem = AdjustmentsItems()
            aditem.adjustments = ad
            aditem.merchInventory = MerchandiseInventory.objects.get(pk=item['code'])
            aditem.qtyAdjusted = item['qty']
            aditem.remaining = item['remaining']
            aditem.unitCost = item['purchasingPrice']
            aditem.totalCost = item['totalLost']
            aditem.oldWarehouse = Warehouse.objects.get(pk=item['oldWarehouse'])
            
            aditem.save()
            request.user.branch.adjustmentItems.add(aditem)
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

