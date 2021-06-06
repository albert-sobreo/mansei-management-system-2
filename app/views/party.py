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

        # child = AccountChild()
        # child.code
        # child.name

        # child.accountSubGroup = AccountSubGroup.objects.get(name=)

        # child.me
        # child.contra
        # child.amount 
        # child.description

        party = Party()
        

        # party.accountChild = AccountChild.objects.get(name=jsonParty['accountChild'])
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
        # try:
        #     party.me = Party.objects.get(pk=jsonParty['me'])
        # except Exception as e:
        #     print(e)

        party.save()

        request.user.branch.party.add(party)

        sweetify.sweetalert(request, icon='success', title='Success!', text='{} has been added as {}'.format(party.name, party.type), persistent='Dismiss')
        return JsonResponse(0, safe=False)
