from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
import sweetify
from datetime import date as now
import datetime
from django.core.exceptions import PermissionDenied
from .notificationCreate import *
import json

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

class InventorySummaryView(View):
    def get(self, request):
        startDate = datetime.date.today().replace(day=1)
        try:
            nextMonth = datetime.date.today().replace(month=startDate.month+1, day=1)
        except Exception as e:
            print(e)
            nextMonth = datetime.date.today().replace(month=1, day=1)
        endDate = nextMonth - datetime.timedelta(days=1)
        context = {
            'startDate': startDate,
            'endDate': endDate
        }
        return render(request, 'inventory-summary.html', context)

class InventorySummaryAPI(APIView):
    def get(self, request):
        startDate = request.GET['startDate']
        endDate = request.GET['endDate']

        # request.user.branch.journal.filter(journalDate__range=[startDate, endDate]).order_by('pk').reverse(),

        salesContracts = request.user.branch.salesContract.filter(dateSold__range=[startDate, endDate], approved=True).order_by('pk')

        lst = []

        for sc in salesContracts:
            for scitems in sc.scitemsmerch.all():
                try:
                    lstIndex = lst.index(list(filter(lambda x: x['name']==scitems.merchInventory.name , lst))[0])
                    try:
                        itemIndex = lst[lstIndex]['items'].index(list(filter(lambda x: x['barcode']==scitems.merchInventory.code, lst[lstIndex]['items']))[0])
                        lst[lstIndex]['items'][itemIndex]['qtyEnd'] = scitems.remaining - scitems.qty
                        lst[lstIndex]['items'][itemIndex]['qtySold'] += scitems.qty
                        lst[lstIndex]['items'][itemIndex]['vol'] += scitems.merchInventory.vol * scitems.qty
                    except Exception as e:
                        print(e)
                        lst[lstIndex]['items'].append({
                            'barcode': scitems.merchInventory.code,
                            'length': scitems.merchInventory.length,
                            'width': scitems.merchInventory.width,
                            'thickness': scitems.merchInventory.thickness,
                            'vol': scitems.merchInventory.vol * scitems.qty,
                            'qtyBeg': scitems.remaining,
                            'qtyEnd': scitems.remaining - scitems.qty,
                            'purchasingPrice': scitems.merchInventory.purchasingPrice,
                            'qtySold': scitems.qty,
                        })
                except Exception as e:
                    print(e)
                    lst.append({
                        'name': scitems.merchInventory.name,
                        'classification': scitems.merchInventory.classification,
                        'items': [
                            {
                                'barcode': scitems.merchInventory.code,
                                'length': scitems.merchInventory.length,
                                'width': scitems.merchInventory.width,
                                'thickness': scitems.merchInventory.thickness,
                                'vol': scitems.merchInventory.vol * scitems.qty,
                                'qtyBeg': scitems.remaining,
                                'qtyEnd': scitems.remaining - scitems.qty,
                                'purchasingPrice': scitems.merchInventory.purchasingPrice,
                                'qtySold': scitems.qty,
                            }
                        ]
                    })

        return JsonResponse(lst, safe=False)
