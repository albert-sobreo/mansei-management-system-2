from django import views
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
from datetime import datetime

class PurchaseRequestView(View):
    def get(self, request, format=None):

        user = request.user

        try:
            pr = user.branch.purchaseRequest.latest('pk')

            listed_code = pr.code.split('-')
            listed_date = str(now.today()).split('-')

            cuprent_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                cuprent_code += 1
                new_code = 'PR-{}-{}-{}'.format(listed_date[0], listed_date[1], str(cuprent_code).zfill(4))
            else:
                new_code = 'PR-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            print(e)
            listed_date = str(now.today()).split('-')
            new_code = 'PR-{}-{}-0001'.format(listed_date[0], listed_date[1])

        context = {
            'new_code': new_code,
        }
        return render(request, 'purchase-request.html', context)

class PRListView(View):
    def get(self, request, format=None):
        return render(request, 'pr-list.html')

class SavePurchaseRequest(APIView):
    def post(self, request, format = None):
        purchaseRequest = request.data['0']
        vendorQuotes = request.data['1']

        pr = PurchaseRequest()

        pr.code = purchaseRequest['code']
        pr.datetimeCreated = datetime.now
        pr.dateRequested = purchaseRequest['date']

        pr.dateNeeded = purchaseRequest['dateNeeded']
        pr.department = purchaseRequest['department']
        pr.intendedFor = purchaseRequest['intendedFor']        
        if request.user.is_authenticated:
            pr.createdBy = request.user

        pr.save()
        request.user.branch.purchaseRequest.add(pr)

    
        for item in purchaseRequest['items']:
            pritemsmerch = PRItemsMerch()
            pritemsmerch.purchaseRequest = pr
            pritemsmerch.merchInventory = MerchandiseInventory.objects.get(pk=item['code'])
            pritemsmerch.remaining = item['remaining']
            pritemsmerch.qty = item['qty']

            
            pritemsmerch.save()
            request.user.branch.pritemsMerch.add(pritemsmerch)


        for item in vendorQuotes:
            if item['type'] == 'Merchandise':
                vqmerch  = VendorQuotesMerch()
                vqmerch.purchaseRequest = pr
                vqmerch.merchInventory = MerchandiseInventory.objects.get(pk=item['item'])

                vqmerch.save()
                request.user.branch.vendorQuotesMerch.add(vqmerch)
                for info in item['info']:
                    if info['purchasingPrice']:
                        vqitemsmerch = VendorQuotesItemsMerch()
                        vqitemsmerch.vendorquotesmerch = vqmerch
                        vqitemsmerch.price = info['purchasingPrice']
                        vqitemsmerch.party = Party.objects.get(name=info['name'])

                        vqitemsmerch.save()
                        request.user.branch.vendorQuotesItemsMerch.add(vqitemsmerch)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class VendorQuotes(APIView):
    def post(self, request, format = None):

        items = MerchandiseInventory.objects.get(pk = request.data['id'])
        jsonItems = [{
            'id': items.pk,
            'code': items.code,
            'classification': items.classification,
            'type': items.type
        }]
        
        for party in Party.objects.filter(type = 'Vendor'):
            element = items.poitemsmerch.filter(purchaseOrder__party = party.pk)
            if element.count():
                jsonItems.append({
                    'purchasingPrice': element.order_by('-pk')[0].purchasingPrice,
                    'vendor': party.name
                })
            if len(jsonItems) >= 3:
                break

        print(jsonItems)
        return JsonResponse(jsonItems, safe=False)
