from rest_framework.views import APIView
from app.models import MerchandiseInventory
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
        a.length = request.data['length']
        a.width = request.data['width']
        a.thickness = request.data['thickness']
        a.purchasingPrice = request.data['purchasingPrice']
        a.sellingPrice = request.data['sellingPrice']
        a.qtyT = 0
        a.qtyR = 0
        a.qtyA = 0
        a.um = "Per Piece"
        a.totalCost = 0.0
        a.save()
        for warehouse in request.data['warehouse']:
            a.warehouse.add(warehouse)

        request.user.branch.merchInventory.add(a)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)