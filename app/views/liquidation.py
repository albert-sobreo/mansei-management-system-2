from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from datetime import date as now
from ..forms import *
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
import sweetify
import pandas as pd
import json
from decimal import Decimal
import datetime
from .petty_cash_api import *
from .journalAPI import *

class LiquidationView(View):
    def get(self, request):
        user = request.user

        try:
            lqd = user.branch.liquidation.latest('pk')

            listed_code = lqd.code.split('-')
            listed_date=  str(now.today()).split('-')

            current_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                current_code += 1
                new_code = 'LQD-{}-{}-{}'.format(listed_date[0], listed_date[1], str(current_code).zfill(4))
            else:
                new_code = 'LQD-{}-{}-0001'.format(listed_date[0], listed_date[1])
        
        except Exception as e:
            print(e)
            listed_date = str(now.today()).split('-')
            new_code = 'LQD-{}-{}-0001'.format(listed_date[0], listed_date[1])

        context = {
            'administrative': request.user.branch.accountGroup.filter(name__regex=r"[Aa]dministrative"),
            'operational': request.user.branch.accountGroup.filter(name__regex=r"[Oo]perational"),
            'new_code': new_code,
            'vendors': request.user.branch.party.filter(type="Vendor")
        }
        return render(request, 'liquidation-form.html', context)

class LiquidationListView(View):
    def get(self, request):
        context = {
            
        }

        return render(request, 'liquidation-list.html', context)

class SaveLiquidationForm(View):
    def post(self, request):
        data = json.loads(request.POST['POSTDATA'])
        files = request.FILES

        lqd = Liquidation()
        lqd.code = data['code']
        try:
            lqd.transactedBy = User.objects.get(pk=data['transactedBy'])
        except Exception as e:
            print(e)
            pass

        lqd.totalAmount = data['totalAmount']

        try: 
            lqd.advancement = AdvancementThruPettyCash.objects.get(pk=data['advancement'])
        except Exception as e:
            print(e)
            pass

        lqd.change = data['change']
        lqd.payable = data['payable']
        lqd.createdBy = request.user
        lqd.datetimeCreated = datetime.datetime.now()

        lqd.save()
        request.user.branch.liquidation.add(lqd)

        for index, entry in enumerate(data['liquidationentries']):
            l = LiquidationEntries()
            l.liquidation = lqd
            l.orNo = entry['orNo']
            try:
                l.expense = AccountChild.objects.get(pk=entry['expense'])
            except Exception as e:
                print(e)
                pass
            try:
                l.vendor = Party.objects.get(pk=entry['party'])
            except Exception as e:
                print(e)
                pass
            l.amount = entry['amount']
            try:
                l.photo = files['orPhoto{}'.format(index)]
            except Exception as e:
                print(e)

            l.save()
            request.user.branch.liquidationEntries.add(l)
        
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)