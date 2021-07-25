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
import pandas as pd
import json

class VendorView(View):
    def get(self, request):
        context = {
            'vendors': request.user.branch.party.filter(type='Vendor')
        }
        return render(request, 'vendors.html', context)

class CustomerView(View):
    def get(self, request):
        context = {
            'customers': request.user.branch.party.filter(type='Customer')
        }
        return render(request, 'customers.html', context)

class SaveParty(APIView):
    def post(self, request, format=None):
        jsonParty = request.data
        
        childAR = AccountChild()
        childAP = AccountChild()

        user = request.user

        try:
            subGroupAR = request.user.branch.subGroup.get(name="Accounts Receivable")
            ARcode = subGroupAR.accountchild.latest('pk')
            current_AR = int(ARcode.code)
            current_AR += 1
            new_AR = str(current_AR).zfill(3)

        except Exception as e:
            print(e)
            new_AR = '001'

        try:
            subGroupAP = request.user.branch.subGroup.get(name="Accounts Payables")
            APcode = subGroupAP.accountchild.latest('pk')
            current_AP = int(APcode.code)
            current_AP += 1
            new_AP = str(current_AP).zfill(3)

        except Exception as e:
            print(e)
            new_AP = '001'

        childAR.code = new_AR 
        childAR.name = 'Trade Receivable - ' + jsonParty['name']
        childAR.accountSubGroup = AccountSubGroup.objects.get(name='Accounts Receivable')
        childAR.me = AccountChild.objects.get(name='Trade Receivable')
        childAR.amount = 0.0
        childAR.description = " "
        childAR.save()

        childAP.code = new_AP
        childAP.name = 'Trade Payables - ' + jsonParty['name']
        childAP.accountSubGroup = AccountSubGroup.objects.get(name='Accounts Payables')
        childAP.me = AccountChild.objects.get(name='Trade Payables')
        childAP.amount = 0.0
        childAP.description = ""
        childAP.save()

        party = Party()
        
        party.name = jsonParty['name']
        party.type = jsonParty['type']
        party.shippingAddress = jsonParty['shippingAddress']
        party.officeAddress = jsonParty['officeAddress']
        party.landline = jsonParty['landline']
        party.mobile = jsonParty['mobile']
        party.email = jsonParty['email']
        party.contactPerson = jsonParty['contactPerson']
        party.bank = jsonParty['bank']
        party.bankNo = jsonParty['bankNo']
        party.tin = jsonParty['tin']
        party.crte = jsonParty['crte']
        party.prefferedPayment = jsonParty['prefferedPayment']

        party.save()

        request.user.branch.accountChild.add(childAR)
        request.user.branch.accountChild.add(childAP)
        party.accountChild.add(childAR)
        party.accountChild.add(childAP)

        request.user.branch.party.add(party)

        sweetify.sweetalert(request, icon='success', title='Success!', text='{} has been added as {}'.format(party.name, party.type), persistent='Dismiss')
        return JsonResponse(0, safe=False)

class ImportCustomerVendor(View):
    def post(self, request, format=None):
        df = pd.read_excel(request.FILES['excel'])
        jsonDF = json.loads(df.to_json(orient='records'))

        existing = []

        for item in jsonDF:
            childAR = AccountChild()
            childAP = AccountChild()

            user = request.user

            try:
                subGroupAR = request.user.branch.subGroup.get(name="Accounts Receivable")
                ARcode = subGroupAR.accountchild.latest('pk')
                current_AR = int(ARcode.code)
                current_AR += 1
                new_AR = str(current_AR).zfill(3)

            except Exception as e:
                print(e)
                new_AR = '001'

            try:
                subGroupAP = request.user.branch.subGroup.get(name="Accounts Payables")
                APcode = subGroupAP.accountchild.latest('pk')
                current_AP = int(APcode.code)
                current_AP += 1
                new_AP = str(current_AP).zfill(3)

            except Exception as e:
                print(e)
                new_AP = '001'

            childAR.code = new_AR 
            childAR.name = 'Trade Receivable - ' + item['Name']
            childAR.accountSubGroup = AccountSubGroup.objects.get(name='Accounts Receivable')
            childAR.me = AccountChild.objects.get(name='Trade Receivable')
            childAR.amount = 0.0
            childAR.description = " "
            childAR.save()

            childAP.code = new_AP
            childAP.name = 'Trade Payables - ' + item['Name']
            childAP.accountSubGroup = AccountSubGroup.objects.get(name='Accounts Payables')
            childAP.me = AccountChild.objects.get(name='Trade Payables')
            childAP.amount = 0.0
            childAP.description = ""
            childAP.save()

            party = Party()

            if Party.objects.filter(name=item['Name']):
                existing.append(item['Name'])
                continue
            
            party.name = item['Name']
            party.type = item['Type']
            party.shippingAddress = item['Shipping-Address']
            party.officeAddress = item['Office-Address']
            party.landline = item['Landline']
            party.mobile =item['Mobile']
            party.email = item['Email']
            party.contactPerson = item['Contact-Person']
            party.bank = item['Bank']
            party.bankNo = item['Bank-Number']
            party.tin = item['TIN']
            party.crte = item['CRTE']
            party.prefferedPayment = item['Preffered-Payment-Method']

            party.save()


            party.accountChild.add(childAR)
            party.accountChild.add(childAP)

            request.user.branch.accountChild.add(childAR)
            request.user.branch.accountChild.add(childAP)
            request.user.branch.party.add(party)
        if len(existing) != 0:
            separator = '<br>'
            sweetify.sweetalert(request, icon='warning', title="Some aren't added to the database.", html='These customers/vendors already exist: {}'.format(separator.join(existing)), persistent="Dismiss")
        else: 
            sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')

        return redirect('/customers/')

class EditParty(APIView):
    def put(self, request, pk, format = None):
        party = Party.objects.get(pk=pk)
        edit = request.data

        party.shippingAddress = edit['shippingAddress']
        party.officeAddress = edit['officeAddress']
        party.landline = edit['landline']
        party.mobile = edit['mobile']
        party.email = edit['email']
        party.contactPerson = edit['contactPerson']
        party.bank = edit['bank']
        party.bankNo = edit['bankNo']
        party.tin = edit['tin']
        party.crte = edit['crte']
        party.prefferedPayment = edit['prefferedPayment']

        party.save()
        sweetify.sweetalert(request, icon='success', title='Success!',  persistent='Dismiss')
        return JsonResponse(0, safe=False)